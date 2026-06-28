import sys

class Kw:
    IS = "ki"
    SAY = "lia"
    WHEN = "kiia"
    AGAIN = "kika"
    IF = "nuliama"
    ELSE = "favu"
    END = "katiu"
    
    ADD = "tuthi"
    SUB = "kima"
    MUL = "batidi"
    DIV = "nauki"
    
    MORE = "bufani"
    LESS = "ikuzu"
    EQLS = "nugiazu"
    NOT = "maba"
    

class Ev:
    def ev(self, s):
        self.vars = {}
        lines = [x for x in s.split("\n") if x.rstrip() != "" and x.strip()[0:2] != "//"]
        self.pc = 0
        
        indent = self.count_indent(lines[0])
        
        while self.pc < len(lines):
            current_indent = self.count_indent(lines[self.pc])
            stripped_line = lines[self.pc].strip()
            # Strip trailing comments
            stripped_line = stripped_line.split("//")[0]
            line = stripped_line.split()
            
            # Match function keywords
            match self.clean_grammar_markings(line[-1]):
                case Kw.IS:
                    # Variable! First is the identifier, followed by the expression!
                    name = str(self.clean_grammar_markings(line[0]))
                    line.pop(0);
                    self.vars[name] = self.ev_expr(line)
                
                case Kw.SAY:
                    # Print line!
                    # print(line)
                    print(self.ev_expr(line))
                    
                case Kw.WHEN:
                    if self.ev_expr(line) == 1:
                        pass
                    else:
                        while Kw.ELSE not in lines[self.pc] and Kw.END not in lines[self.pc] and Kw.AGAIN not in lines[self.pc]:
                            self.pc += 1
                        # print(line, "jumping to", pc)
                
                case Kw.ELSE:
                    while Kw.END not in lines[self.pc]:
                        self.pc += 1
                
                case Kw.AGAIN:
                    while Kw.WHEN not in lines[self.pc]:
                        self.pc -= 1
                    # print(line, "jumping to", self.pc)
                    self.pc -= 1
                    
                case Kw.END:
                    pass
                
                case _:
                    print("Error! Unknown case!");
            # print(self.pc, self.vars, self.clean_grammar_markings(line[-1]))
        
            self.pc += 1
        print("\nInternal Variables:", self.vars,"\n")
        
    def ev_expr(self, s):
        stack = []
        string_mode = False
        string_buffer = ""
        string_value_mode = False
        string_value_holder = []
        for tok in s:
            # String Handler
            if len(tok) >= 1 and not string_mode and tok[0] == "(":
                tok = tok[1:]
                string_mode = True
            
            if len(tok) >= 1 and not string_value_mode and tok[0] == "[":
                tok = tok[1:]
                string_value_mode = True
            
            if string_value_mode:
                if len(tok) >= 1:
                    if tok[-1] == "]":
                        string_value_holder.append(tok[:-1])
                        string_buffer += str(self.ev_expr(string_value_holder)) + " "
                        string_value_holder.clear()
                        string_value_mode = False
                        continue
                    elif tok[-2:] == "])":
                        string_value_holder.append(tok[:-2])
                        string_buffer += str(self.ev_expr(string_value_holder)) + " "
                        string_value_holder.clear()
                        string_value_mode = False
                        tok = ")"
                    else:
                        string_value_holder.append(tok)
                        continue
                
            
            if string_mode:
                if len(tok) >= 1:
                    if tok[-1] == ")":
                        tok = tok[:-1]
                        string_buffer += tok
                        stack.append(string_buffer)
                        string_buffer = ""
                        string_mode = False
                    else:
                        string_buffer += tok + " "
                continue
            
            
            # Remove grammar markings m n ng / b d g
            tok = self.clean_grammar_markings(tok)
            # Remove copula
            if tok == Kw.IS: continue
            
            # Values
            if tok.isdigit():
                stack.append(int(tok))
            elif tok in self.vars:
                # print("Found", tok, "with a value of", self.vars[tok])
                stack.append(self.vars[tok])
                
            # Not
            elif tok == Kw.NOT:
                old_value = stack.pop()
                stack.append(1 - old_value)
            elif len(stack) >= 2:
                
                # Operations
                rhs = stack.pop()
                lhs = stack.pop()
                
                if tok == Kw.ADD:
                    if isinstance(rhs, str) or isinstance(lhs, str):
                        stack.append(str(lhs) + str(rhs))
                    else:
                        stack.append(lhs + rhs);
                elif not isinstance(rhs, str) and not isinstance(lhs, str):
                    if tok == Kw.SUB:
                        stack.append(lhs - rhs);
                    elif tok == Kw.MUL:
                        stack.append(lhs * rhs);
                    elif tok == Kw.DIV:
                        stack.append(rhs / lhs);
                    
                    # Binary Operations
                    elif tok == Kw.MORE:
                        if lhs > rhs:
                            stack.append(1)
                        else:
                            stack.append(0)
                    elif tok == Kw.LESS:
                        if lhs < rhs:
                            stack.append(1)
                        else:
                            stack.append(0)
                    elif tok == Kw.EQLS:
                        if lhs == rhs:
                            stack.append(1)
                        else:
                            stack.append(0)
        if string_mode or string_value_mode:
            # Cannot still be in string mode at the end of a line!
            print("Error! Unclosed string in line", self.pc+1)
            return 0
        return stack[0]
    
    def clean_grammar_markings(self, s):
        if s[-2:] in ['ng'] and len(s) > 2:
            return s[:-2]
        elif s[-1] in ['m', 'n', 'b', 'd', 'g'] and len(s) > 1:
            return s[:-1]
        return s
    
    def count_indent(self, s):
        return len(s) - len(s.lstrip(" "))
    
Ev().ev(open(sys.argv[1]).read())