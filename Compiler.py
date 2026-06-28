from llvmlite import ir
import os

from AST import Statement, Expression, Program, Node, NodeType
from AST import ExpressionStatement, LetStatement, BlockStatement, FunctionStatement, ReturnStatement, AssignStatement, IfStatement, WhileStatement, ImportStatement
from AST import InfixExpression, CallExpression, StringExpression, SuffixExpression
from AST import IntegerLiteral, FloatLiteral, IdentifierLiteral, BooleanLiteral, StringLiteral
from AST import FunctionParameter

from Environment import Environment

from Lexer import Lexer
from Parser_RPN import Parser


class Compiler:
    def __init__(self, main_file_path: str) -> None:
        self.type_map: dict[str, ir.Type] = {
            'akatanami': ir.IntType(32),
            'vadriuka': ir.FloatType(),
            'zuruva': ir.IntType(1),
            'lana': ir.PointerType(ir.IntType(8)),
            'tidimaba': ir.VoidType()
        }
        
        self.module: ir.Module = ir.Module('akamuri')
        
        self.builder: ir.IRBuilder = ir.IRBuilder()
        
        self.env: Environment = Environment()
        
        self.counter: int = 0
        
        # Error tracking for now
        self.errors: list[str] = []
        
        self.__initialise_builtins()
        
        self.working_directory: str = os.path.dirname(main_file_path)
        self.global_parsed_pallets: dict[str, Program] = {}
        
        self.string_constants = {}
        
    def __initialise_builtins(self) -> None:
        def __init_print() -> ir.Function:
            fnty: ir.FunctionType = ir.FunctionType(
                self.type_map['akatanami'],
                [ir.IntType(8).as_pointer()],
                var_arg=True
            )
            return ir.Function(self.module, fnty, 'printf')
        
        def __init_booleans() -> tuple[ir.GlobalVariable, ir.GlobalVariable]:
            bool_type: ir.Type = self.type_map['zuruva']
            
            true_var = ir.GlobalVariable(self.module, bool_type, 'true')
            true_var.initializer = ir.Constant(bool_type, 1)
            true_var.global_constant = True
            
            false_var = ir.GlobalVariable(self.module, bool_type, 'false')
            false_var.initializer = ir.Constant(bool_type, 0)
            false_var.global_constant = True
            
            return true_var, false_var
        
        # Internal builtins
        # int snprintf(char *str, size_t size, const char *format, ...);
        self.snprintf = ir.Function(
            self.module,
            ir.FunctionType(
                ir.IntType(32),
                [ir.IntType(8).as_pointer(), ir.IntType(32), ir.IntType(8).as_pointer()],
                var_arg=True
            ),
            name="_snprintf"
        )
        
        # int _scprintf(const char *format, ...);
        self.scprintf = ir.Function(
            self.module,
            ir.FunctionType(
                ir.IntType(32),
                [ir.IntType(8).as_pointer()],
                var_arg=True
            ),
            name="_scprintf"
        )
        
        # void* malloc(size_t size);
        self.malloc = ir.Function(
            self.module,
            ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(64)]),
            name="malloc"
        )
        
        # free
        self.free = ir.Function(
            self.module,
            ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer()]),
            name="free"
        )
        
        # Exposed builtins
        self.env.define('lia', __init_print(), ir.IntType(32))
        
        true_var, false_var = __init_booleans()
        self.env.define('wogi', true_var, true_var.type)
        self.env.define('muda', false_var, false_var.type)
        
    def compile(self, node: Node) -> None:
        match node.type():
            case NodeType.Program:
                self.__visit_program(node)
            
            # Statements
            case NodeType.ExpressionStatement:
                self.__visit_expression_statement(node)
            case NodeType.LetStatement:
                self.__visit_let_statement(node)
            case NodeType.FunctionStatement:
                self.__visit_function_statement(node)
            case NodeType.BlockStatement:
                self.__visit_block_statement(node)
            case NodeType.ReturnStatement:
                self.__visit_return_statement(node)
            case NodeType.AssignStatement:
                self.__visit_assign_statement(node)
            case NodeType.IfStatement:
                self.__visit_if_statement(node)
            case NodeType.WhileStatement:
                self.__visit_while_statement(node)
            case NodeType.ImportStatement:
                self.__visit_import_statement(node)
                
            # Expressions
            case NodeType.InfixExpression:
                self.__visit_infix_expression(node)
            case NodeType.CallExpression:
                self.__visit_call_expression(node)
            # case NodeType.StringExpression:
            #     self.__visit_string_expression(node)
                
    # region Visit Methods
    def __visit_program(self, node: Program) -> None:
        for stmt in node.statements:
            self.compile(stmt)
        
    # region Statements
    def __visit_expression_statement(self, node: ExpressionStatement) -> None:
        self.compile(node.expr)
        
    def __visit_let_statement(self, node: LetStatement) -> None:
        name: str = node.name.value
        value: Expression = node.value
        value_type: str = node.value_type # TODO: Implement
        
        value, Type = self.__resolve_value(node=value)
        
        if self.env.lookup(name) is None:
            # Define and allocate variable
            ptr = self.builder.alloca(Type)
            
            # Storing value
            self.builder.store(value, ptr)
            
            # Add var to env
            self.env.define(name, ptr, Type)
        else:
            ptr, _ = self.env.lookup(name)
            self.builder.store(value, ptr)
            
    def __visit_block_statement(self, node: BlockStatement) -> None:
        for stmt in node.statements:
            self.compile(stmt)
            
    def __visit_return_statement(self, node: ReturnStatement) -> None:
        value: Expression = node.return_value
        value, Type = self.__resolve_value(value)
        
        self.builder.ret(value)
        
    def __visit_function_statement(self, node: FunctionStatement) -> None:
        name: str = node.name.value
        body: BlockStatement = node.body
        params: list[FunctionParameter] = node.parameters
        
        param_names: list[str] = [p.name for p in params]
        
        param_types: list[ir.Type] = [self.type_map[p.value_type] for p in params]
        
        return_type: ir.Type = self.type_map[node.return_type]
        
        fnty: ir.FunctionType = ir.FunctionType(return_type, param_types)
        func: ir.Function = ir.Function(self.module, fnty, name=name)
        
        block: ir.Block = func.append_basic_block(f"{name}_entry")
        
        previous_builder = self.builder

        self.builder = ir.IRBuilder(block)
        
        # Store pointers to the params
        params_ptr = []
        for i, typ in enumerate(param_types):
            ptr = self.builder.alloca(typ)
            self.builder.store(func.args[i], ptr)
            params_ptr.append(ptr)
        
        # Adding params to env
        previous_env = self.env
        self.env = Environment(parent=previous_env)
        for i, x in enumerate(zip(param_types, param_names)):
            typ = param_types[i]
            ptr = params_ptr[i]
            
            self.env.define(x[1], ptr, typ)
        
        self.env.define(name, func, return_type)
        
        self.compile(body)
        
        self.env = previous_env
        self.env.define(name, func, return_type)
        
        self.builder = previous_builder
        
    def __visit_assign_statement(self, node: AssignStatement) -> None:
        name: str = node.ident.value
        value: Expression = node.right_value
        
        value, Type = self.__resolve_value(value)
        
        if self.env.lookup(name) is None:
            self.errors.append(f"COMPILE ERROR: Identifier {name} has not been declared before it was re-assigned.")
        else:
            ptr, _ = self.env.lookup(name)
            self.builder.store(value, ptr)

    def __visit_if_statement(self, node: IfStatement) -> None:
        condition = node.condition
        consequence = node.consequence
        alternative = node.alternative
        
        test, _ = self.__resolve_value(condition)
        
        if alternative is None:
            with self.builder.if_then(test):
                self.compile(consequence)
        else:
            with self.builder.if_else(test) as (true, otherwise):
                with true:
                    self.compile(consequence)
                with otherwise:
                    self.compile(alternative)
                    
    def __visit_while_statement(self, node: WhileStatement) -> None:
        condition: Expression = node.condition
        body: BlockStatement = node.body
        
        test, _ = self.__resolve_value(condition)
        
        while_loop_entry = self.builder.append_basic_block(f"while_loop_entry_{self.__increment_counter()}")
        
        while_loop_otherwise = self.builder.append_basic_block(f"while_loop_otherwise_{self.counter}")
        
        self.builder.cbranch(test, while_loop_entry, while_loop_otherwise)
        
        self.builder.position_at_start(while_loop_entry)
        
        self.compile(body)
        
        test, _ = self.__resolve_value(condition)
        
        self.builder.cbranch(test, while_loop_entry, while_loop_otherwise)
        self.builder.position_at_start(while_loop_otherwise)
    
    def __visit_import_statement(self, node: ImportStatement) -> None:
        file_path: str = node.file_path
        
        if self.global_parsed_pallets.get(file_path) is not None:
            self.errors.append(f"[KULIUKA WARNING]: `{file_path}` is already imported globally\n")
            return
        
        new_path: str = os.path.join(self.working_directory, file_path)
        # print(new_path)
        
        with open(new_path, "r") as f:
            pallet_code: str = f.read()
            
        l: Lexer = Lexer(source=pallet_code)
        p: Parser = Parser(lexer=l)
        
        program: Program = p.parse_program()
        if len(p.errors) > 0:
            print(f"Error with imported pallet: {file_path}")
            for err in p.errors:
                print(err)
            exit(1)
            
        self.compile(node=program)
        
        self.global_parsed_pallets[file_path] = program
    # endregion
    
    # region Expressions
    def __visit_infix_expression(self, node: InfixExpression) -> None:
        operator: str = node.operator
        left_value, left_type = self.__resolve_value(node.left_node)
        right_value, right_type = self.__resolve_value(node.right_node)
        
        value = None
        Type = None
        # Convert both sides to match types (Int with Int, Float with Float)
        if isinstance(right_type, ir.IntType) and isinstance(left_type, ir.FloatType):
            # Right converted to float
            right_value = self.builder.sitofp(right_value, ir.FloatType())
        elif isinstance(right_type, ir.FloatType) and isinstance(left_type, ir.IntType):
            # Left converted to float
            left_value = self.builder.sitofp(left_value, ir.FloatType())
            
        # Perform operations
        if isinstance(right_type, ir.IntType) and isinstance(left_type, ir.IntType):
            Type = self.type_map['akatanami'] # Int
            match operator:
                case 'tuthi':
                    value = self.builder.add(left_value, right_value)
                case 'kima':
                    value = self.builder.sub(left_value, right_value)
                case 'batidi':
                    value = self.builder.mul(left_value, right_value)
                case 'nauki':
                    value = self.builder.sdiv(left_value, right_value)
                    
                case 'ikuzu':
                    value = self.builder.icmp_signed('<', left_value, right_value)
                    Type = ir.IntType(1)
                case 'bufani':
                    value = self.builder.icmp_signed('>', left_value, right_value)
                    Type = ir.IntType(1)
                case 'nugiazu':
                    value = self.builder.icmp_signed('==', left_value, right_value)
                    Type = ir.IntType(1)
                
                    
        elif isinstance(right_type, ir.FloatType) and isinstance(left_type, ir.FloatType):
            Type = self.type_map['vadriuka'] # Float
            match operator:
                case 'tuthi':
                    value = self.builder.fadd(left_value, right_value)
                case 'kima':
                    value = self.builder.fsub(left_value, right_value)
                case 'batidi':
                    value = self.builder.fmul(left_value, right_value)
                case 'nauki':
                    value = self.builder.fdiv(left_value, right_value)
                    
                case 'ikuzu':
                    value = self.builder.fcmp_ordered('<', left_value, right_value)
                    Type = ir.IntType(1)
                case 'bufani':
                    value = self.builder.fcmp_ordered('>', left_value, right_value)
                    Type = ir.IntType(1)
                case 'nugiazu':
                    value = self.builder.fcmp_ordered('==', left_value, right_value)
                    Type = ir.IntType(1)
                    
        return value, Type
    
    def __visit_call_expression(self, node: CallExpression) -> tuple[ir.Instruction, ir.Type]:
        name: str = node.function.value
        params: list[Expression] = node.arguments
        
        args = []
        types = []
        if len(params) > 0:
            for x in params:
                p_val, p_type = self.__resolve_value(x)
                # print(p_val)
                args.append(p_val)
                types.append(p_type)
        
        match name:
            case 'lia':
                ret = self.builtin_printf(params=args, return_type=types[0])
                ret_type = self.type_map['akatanami']
            case _:
                func, ret_type = self.env.lookup(name)
                ret = self.builder.call(func, args)
                
        return ret, ret_type
            
    def __visit_string_expression(self, node: StringExpression) -> tuple[ir.Instruction, ir.Type]:
        # Basically the same as __convert_string() further down, but each of the contents in the StringExpression will be concatenated into one big formatted string
        
        fmt_parts = []
        args = []
        
        for part in node.contents:
            # print(part.value)
            if isinstance(part, StringLiteral):
                partstr = part.value.replace('%', '%%')
                fmt_parts.append(partstr)
            else:
                value, Type = self.__resolve_value(part)
                
                # convert to spec and c compat
                spec, arg = self.printf_spec_and_arg(value, Type)
                
                
                fmt_parts.append(spec)
                args.append(arg)

        string: str = "".join(fmt_parts)
        
        if not string.endswith("\0"):
            string += "\0"
        
        # print (string)
        # print (args)
        
        # Convert string to formatted string
        fmt_result = self.create_formatted_string(string, args=args)
        
        return fmt_result, fmt_result.type
    
    # region string helpers
    def create_formatted_string(self, fmt_text, args):
        zero = ir.Constant(ir.IntType(32), 0)
        
        # array_ty = ir.ArrayType(ir.IntType(8), 1024)
        # buffer_array = self.builder.alloca(array_ty, name="fmt_buffer")
        
        global_str, _ = self.__convert_string(fmt_text)
        fmt_ptr = self.builder.gep(global_str, [zero, zero], inbounds=True)
        
        # buffer_ptr = self.builder.gep(buffer_array, [zero, zero], inbounds=True)

        # 1. Ask snprintf how many characters are needed.
        needed_i32 = self.builder.call(
            self.scprintf,
            [fmt_ptr, *args],
            name="fmt_needed"
        )

        # 2. Add 1 for the null terminator.
        buffer_size_i32 = self.builder.add(
            needed_i32,
            ir.Constant(ir.IntType(32), 1),
            name="fmt_size_i32"
        )

        # 3. something ?
        buffer_size_i64 = self.builder.zext(buffer_size_i32, ir.IntType(64), name="fmt_size_i64")

        # 4. Allocate buffer.
        buffer = self.builder.call(self.malloc, [buffer_size_i64], name="fmt_heap_buffer")

        # 5. Write formatted string into buffer.
        self.builder.call(
            self.snprintf,
            [buffer, buffer_size_i32, fmt_ptr, *args],
            name="fmt_write"
        )

        # print(buffer)
        return buffer
    
    def printf_spec_and_arg(self, value, Type):
        
        if Type == ir.FloatType():
            return "%f", self.builder.fpext(value, ir.DoubleType())

        if Type == ir.DoubleType():
            return "%f", value

        if Type == ir.IntType(1):
            return "%d", self.builder.zext(value, ir.IntType(32))

        if isinstance(Type, ir.IntType):
            if Type.width < 32:
                return "%d", self.builder.sext(value, ir.IntType(32))
            if Type.width == 32:
                return "%d", value
            if Type.width == 64:
                return "%lld", value

        if Type == ir.IntType(8).as_pointer():
            return "%s", value

        raise TypeError(f"Cannot format value of type {Type}")
    # endregion
    
    def __visit_suffix_expression(self, node: SuffixExpression) -> tuple[ir.Value, ir.Type]:
        operator: str = node.operator
        left_node: Expression = node.left_node
        
        left_value, left_type = self.__resolve_value(left_node)
        
        Type = None
        value = None
        if isinstance(left_type, ir.FloatType):
            Type = ir.FloatType()
            match operator:
                case '-':
                    value = self.builder.fmul(left_value, ir.Constant(ir.FloatType(), -1.0))
                case 'maba':
                    value = ir.Constant(ir.IntType(1), 0)
        elif isinstance(left_type, ir.IntType):
            Type = ir.IntType(32)
            match operator:
                case '-':
                    value = self.builder.mul(left_value, ir.Constant(ir.IntType(32), -1))
                case 'maba':
                    value = self.builder.not_(left_value)
                    
        return value, Type
    # endregion
    # endregion
    
    # region Helper Methods
    def __increment_counter(self) -> int:
        self.counter += 1
        return self.counter
    
    def __resolve_value(self, node: Expression, ) -> tuple[ir.Value, ir.Type]:
        match node.type():
            case NodeType.IntegerLiteral:
                node: IntegerLiteral = node
                value, Type = node.value, self.type_map['akatanami']
                return ir.Constant(Type, value), Type
            case NodeType.FloatLiteral:
                node: FloatLiteral = node
                value, Type = node.value, self.type_map['vadriuka']
                return ir.Constant(Type, value), Type
            case NodeType.IdentifierLiteral:
                node: IdentifierLiteral = node
                ptr, Type = self.env.lookup(node.value)
                return self.builder.load(ptr), Type
            case NodeType.BooleanLiteral:
                node: BooleanLiteral = node
                return ir.Constant(ir.IntType(1), 1 if node.value else 0), ir.IntType(1)
            case NodeType.StringLiteral:
                node: StringLiteral = node
                string, Type = self.__convert_string(node.value)
                return string, Type
            
            # Expression Values
            case NodeType.InfixExpression:
                return self.__visit_infix_expression(node)
            case NodeType.CallExpression:
                return self.__visit_call_expression(node)
            case NodeType.StringExpression:
                return self.__visit_string_expression(node)
            case NodeType.SuffixExpression:
                return self.__visit_suffix_expression(node)
            
    def __convert_string(self, string: str) -> tuple[ir.Constant, ir.ArrayType]:
        
        if not string.endswith("\0"):
            string += "\0"
        
        fmt = f"{string}"
        # print(fmt)
        
        if string in self.string_constants:
            global_str = self.string_constants[string]
        else:
            data = bytearray(fmt.encode("utf8"))
            c_fmt: ir.Constant = ir.Constant(ir.ArrayType(ir.IntType(8), len(data)), data)
            
            global_str = ir.GlobalVariable(self.module, c_fmt.type, name=f'__str_{self.__increment_counter()}')
            global_str.linkage = 'internal'
            global_str.global_constant = True
            global_str.initializer = c_fmt
            
            self.string_constants[string] = global_str

        return global_str, global_str.type
    
    def builtin_printf(self, params: list[ir.Instruction], return_type: ir.Type) -> None:
        func, _ = self.env.lookup('lia')
        
        zero = ir.Constant(ir.IntType(32), 0)
        printer_s, _ = self.__convert_string("%s\n\0")
        printer_fmt = self.builder.gep(printer_s, [zero, zero], inbounds=True)
        
        c_fmt: ir.LoadInstr = printer_fmt
        fmt_arg = self.builder.bitcast(c_fmt, ir.IntType(8).as_pointer())
        self.builder.call(func, [fmt_arg, *params])
        
        self.builder.call(self.free, [params[0]])
        
        return 0
        
    # endregion