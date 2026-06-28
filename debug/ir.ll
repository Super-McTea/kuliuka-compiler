; ModuleID = "akamuri"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"_snprintf"(i8* %".1", i32 %".2", i8* %".3", ...)

declare i32 @"_scprintf"(i8* %".1", ...)

declare i8* @"malloc"(i64 %".1")

declare void @"free"(i8* %".1")

declare i32 @"printf"(i8* %".1", ...)

@"true" = constant i1 1
@"false" = constant i1 0
define i32 @"loco_adder"(i32 %".1")
{
loco_adder_entry:
  %".3" = alloca i32
  store i32 %".1", i32* %".3"
  %".5" = load i32, i32* %".3"
  %".6" = getelementptr inbounds [54 x i8], [54 x i8]* @"__str_1", i32 0, i32 0
  %"fmt_needed" = call i32 (i8*, ...) @"_scprintf"(i8* %".6", i32 %".5")
  %"fmt_size_i32" = add i32 %"fmt_needed", 1
  %"fmt_size_i64" = zext i32 %"fmt_size_i32" to i64
  %"fmt_heap_buffer" = call i8* @"malloc"(i64 %"fmt_size_i64")
  %"fmt_write" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer", i32 %"fmt_size_i32", i8* %".6", i32 %".5")
  %".7" = getelementptr inbounds [4 x i8], [4 x i8]* @"__str_2", i32 0, i32 0
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7", i8* %"fmt_heap_buffer")
  call void @"free"(i8* %"fmt_heap_buffer")
  %".10" = alloca i32
  store i32 0, i32* %".10"
  %".12" = load i32, i32* %".10"
  %".13" = mul i32 %".12", 64
  %".14" = load i32, i32* %".3"
  %".15" = icmp sgt i32 %".13", %".14"
  %".16" = xor i1 %".15", -1
  br i1 %".16", label %"while_loop_entry_3", label %"while_loop_otherwise_3"
while_loop_entry_3:
  %".18" = load i32, i32* %".10"
  %".19" = add i32 %".18", 1
  store i32 %".19", i32* %".10"
  %".21" = load i32, i32* %".10"
  %".22" = mul i32 %".21", 64
  %".23" = load i32, i32* %".3"
  %".24" = icmp sgt i32 %".22", %".23"
  %".25" = xor i1 %".24", -1
  br i1 %".25", label %"while_loop_entry_3", label %"while_loop_otherwise_3"
while_loop_otherwise_3:
  %".27" = load i32, i32* %".10"
  %".28" = sub i32 %".27", 1
  store i32 %".28", i32* %".10"
  %".30" = alloca i32
  store i32 0, i32* %".30"
  %".32" = load i32, i32* %".30"
  %".33" = mul i32 %".32", 8
  %".34" = load i32, i32* %".3"
  %".35" = icmp sgt i32 %".33", %".34"
  %".36" = xor i1 %".35", -1
  br i1 %".36", label %"while_loop_entry_4", label %"while_loop_otherwise_4"
while_loop_entry_4:
  %".38" = load i32, i32* %".30"
  %".39" = add i32 %".38", 1
  store i32 %".39", i32* %".30"
  %".41" = load i32, i32* %".30"
  %".42" = mul i32 %".41", 8
  %".43" = load i32, i32* %".3"
  %".44" = icmp sgt i32 %".42", %".43"
  %".45" = xor i1 %".44", -1
  br i1 %".45", label %"while_loop_entry_4", label %"while_loop_otherwise_4"
while_loop_otherwise_4:
  %".47" = load i32, i32* %".3"
  %".48" = load i32, i32* %".10"
  %".49" = load i32, i32* %".3"
  %".50" = load i32, i32* %".10"
  %".51" = mul i32 %".50", 64
  %".52" = sub i32 %".49", %".51"
  %".53" = getelementptr inbounds [45 x i8], [45 x i8]* @"__str_5", i32 0, i32 0
  %"fmt_needed.1" = call i32 (i8*, ...) @"_scprintf"(i8* %".53", i32 %".47", i32 %".48", i32 %".52")
  %"fmt_size_i32.1" = add i32 %"fmt_needed.1", 1
  %"fmt_size_i64.1" = zext i32 %"fmt_size_i32.1" to i64
  %"fmt_heap_buffer.1" = call i8* @"malloc"(i64 %"fmt_size_i64.1")
  %"fmt_write.1" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer.1", i32 %"fmt_size_i32.1", i8* %".53", i32 %".47", i32 %".48", i32 %".52")
  %".54" = getelementptr inbounds [4 x i8], [4 x i8]* @"__str_2", i32 0, i32 0
  %".55" = call i32 (i8*, ...) @"printf"(i8* %".54", i8* %"fmt_heap_buffer.1")
  call void @"free"(i8* %"fmt_heap_buffer.1")
  %".57" = load i32, i32* %".30"
  %".58" = mul i32 %".57", 8
  %".59" = load i32, i32* %".30"
  %".60" = load i32, i32* %".30"
  %".61" = mul i32 %".60", 8
  %".62" = load i32, i32* %".3"
  %".63" = sub i32 %".61", %".62"
  %".64" = getelementptr inbounds [58 x i8], [58 x i8]* @"__str_6", i32 0, i32 0
  %"fmt_needed.2" = call i32 (i8*, ...) @"_scprintf"(i8* %".64", i32 %".58", i32 %".59", i32 %".63")
  %"fmt_size_i32.2" = add i32 %"fmt_needed.2", 1
  %"fmt_size_i64.2" = zext i32 %"fmt_size_i32.2" to i64
  %"fmt_heap_buffer.2" = call i8* @"malloc"(i64 %"fmt_size_i64.2")
  %"fmt_write.2" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer.2", i32 %"fmt_size_i32.2", i8* %".64", i32 %".58", i32 %".59", i32 %".63")
  %".65" = getelementptr inbounds [4 x i8], [4 x i8]* @"__str_2", i32 0, i32 0
  %".66" = call i32 (i8*, ...) @"printf"(i8* %".65", i8* %"fmt_heap_buffer.2")
  call void @"free"(i8* %"fmt_heap_buffer.2")
  %".68" = load i32, i32* %".3"
  ret i32 %".68"
}

@"__str_1" = internal constant [54 x i8] c" == Calculating materials for painting %d blocks == \0a\00"
@"__str_2" = internal constant [4 x i8] c"%s\0a\00"
@"__str_5" = internal constant [45 x i8] c"Total of %d, contains %d stacks and %d extra\00"
@"__str_6" = internal constant [58 x i8] c"Can paint %d, using %d dyes and clay with %d extra blocks\00"
define i32 @"factorial"(i32 %".1")
{
factorial_entry:
  %".3" = alloca i32
  store i32 %".1", i32* %".3"
  %".5" = load i32, i32* %".3"
  %".6" = icmp slt i32 %".5", 0
  br i1 %".6", label %"factorial_entry.if", label %"factorial_entry.endif"
factorial_entry.if:
  ret i32 0
factorial_entry.endif:
  %".9" = alloca i32
  store i32 1, i32* %".9"
  %".11" = load i32, i32* %".3"
  %".12" = alloca i32
  store i32 %".11", i32* %".12"
  %".14" = load i32, i32* %".12"
  %".15" = icmp sgt i32 %".14", 0
  br i1 %".15", label %"while_loop_entry_7", label %"while_loop_otherwise_7"
while_loop_entry_7:
  %".17" = load i32, i32* %".9"
  %".18" = load i32, i32* %".12"
  %".19" = mul i32 %".17", %".18"
  store i32 %".19", i32* %".9"
  %".21" = load i32, i32* %".12"
  %".22" = sub i32 %".21", 1
  store i32 %".22", i32* %".12"
  %".24" = load i32, i32* %".12"
  %".25" = icmp sgt i32 %".24", 0
  br i1 %".25", label %"while_loop_entry_7", label %"while_loop_otherwise_7"
while_loop_otherwise_7:
  %".27" = load i32, i32* %".9"
  ret i32 %".27"
}

define i32 @"fibonacci"(i32 %".1")
{
fibonacci_entry:
  %".3" = alloca i32
  store i32 %".1", i32* %".3"
  %".5" = getelementptr inbounds [3 x i8], [3 x i8]* @"__str_8", i32 0, i32 0
  %"fmt_needed" = call i32 (i8*, ...) @"_scprintf"(i8* %".5")
  %"fmt_size_i32" = add i32 %"fmt_needed", 1
  %"fmt_size_i64" = zext i32 %"fmt_size_i32" to i64
  %"fmt_heap_buffer" = call i8* @"malloc"(i64 %"fmt_size_i64")
  %"fmt_write" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer", i32 %"fmt_size_i32", i8* %".5")
  %".6" = alloca i8*
  store i8* %"fmt_heap_buffer", i8** %".6"
  %".8" = load i32, i32* %".3"
  %".9" = icmp eq i32 %".8", 1
  br i1 %".9", label %"fibonacci_entry.if", label %"fibonacci_entry.else"
fibonacci_entry.if:
  %".11" = getelementptr inbounds [3 x i8], [3 x i8]* @"__str_9", i32 0, i32 0
  %"fmt_needed.1" = call i32 (i8*, ...) @"_scprintf"(i8* %".11")
  %"fmt_size_i32.1" = add i32 %"fmt_needed.1", 1
  %"fmt_size_i64.1" = zext i32 %"fmt_size_i32.1" to i64
  %"fmt_heap_buffer.1" = call i8* @"malloc"(i64 %"fmt_size_i64.1")
  %"fmt_write.1" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer.1", i32 %"fmt_size_i32.1", i8* %".11")
  store i8* %"fmt_heap_buffer.1", i8** %".6"
  br label %"fibonacci_entry.endif"
fibonacci_entry.else:
  %".14" = load i32, i32* %".3"
  %".15" = icmp eq i32 %".14", 2
  br i1 %".15", label %"fibonacci_entry.else.if", label %"fibonacci_entry.else.else"
fibonacci_entry.endif:
  %".28" = load i32, i32* %".3"
  %".29" = load i8*, i8** %".6"
  %".30" = getelementptr inbounds [39 x i8], [39 x i8]* @"__str_12", i32 0, i32 0
  %"fmt_needed.4" = call i32 (i8*, ...) @"_scprintf"(i8* %".30", i32 %".28", i8* %".29")
  %"fmt_size_i32.4" = add i32 %"fmt_needed.4", 1
  %"fmt_size_i64.4" = zext i32 %"fmt_size_i32.4" to i64
  %"fmt_heap_buffer.4" = call i8* @"malloc"(i64 %"fmt_size_i64.4")
  %"fmt_write.4" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer.4", i32 %"fmt_size_i32.4", i8* %".30", i32 %".28", i8* %".29")
  %".31" = getelementptr inbounds [4 x i8], [4 x i8]* @"__str_2", i32 0, i32 0
  %".32" = call i32 (i8*, ...) @"printf"(i8* %".31", i8* %"fmt_heap_buffer.4")
  call void @"free"(i8* %"fmt_heap_buffer.4")
  %".34" = alloca i32
  store i32 0, i32* %".34"
  %".36" = alloca i32
  store i32 1, i32* %".36"
  %".38" = alloca i32
  store i32 0, i32* %".38"
  %".40" = alloca i32
  store i32 0, i32* %".40"
  %".42" = load i32, i32* %".3"
  %".43" = icmp sgt i32 %".42", 0
  %".44" = xor i1 %".43", -1
  br i1 %".44", label %"fibonacci_entry.endif.if", label %"fibonacci_entry.endif.endif"
fibonacci_entry.else.if:
  %".17" = getelementptr inbounds [3 x i8], [3 x i8]* @"__str_10", i32 0, i32 0
  %"fmt_needed.2" = call i32 (i8*, ...) @"_scprintf"(i8* %".17")
  %"fmt_size_i32.2" = add i32 %"fmt_needed.2", 1
  %"fmt_size_i64.2" = zext i32 %"fmt_size_i32.2" to i64
  %"fmt_heap_buffer.2" = call i8* @"malloc"(i64 %"fmt_size_i64.2")
  %"fmt_write.2" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer.2", i32 %"fmt_size_i32.2", i8* %".17")
  store i8* %"fmt_heap_buffer.2", i8** %".6"
  br label %"fibonacci_entry.else.endif"
fibonacci_entry.else.else:
  %".20" = load i32, i32* %".3"
  %".21" = icmp eq i32 %".20", 3
  br i1 %".21", label %"fibonacci_entry.else.else.if", label %"fibonacci_entry.else.else.endif"
fibonacci_entry.else.endif:
  br label %"fibonacci_entry.endif"
fibonacci_entry.else.else.if:
  %".23" = getelementptr inbounds [3 x i8], [3 x i8]* @"__str_11", i32 0, i32 0
  %"fmt_needed.3" = call i32 (i8*, ...) @"_scprintf"(i8* %".23")
  %"fmt_size_i32.3" = add i32 %"fmt_needed.3", 1
  %"fmt_size_i64.3" = zext i32 %"fmt_size_i32.3" to i64
  %"fmt_heap_buffer.3" = call i8* @"malloc"(i64 %"fmt_size_i64.3")
  %"fmt_write.3" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer.3", i32 %"fmt_size_i32.3", i8* %".23")
  store i8* %"fmt_heap_buffer.3", i8** %".6"
  br label %"fibonacci_entry.else.else.endif"
fibonacci_entry.else.else.endif:
  br label %"fibonacci_entry.else.endif"
fibonacci_entry.endif.if:
  %".46" = load i32, i32* %".34"
  %".47" = getelementptr inbounds [12 x i8], [12 x i8]* @"__str_13", i32 0, i32 0
  %"fmt_needed.5" = call i32 (i8*, ...) @"_scprintf"(i8* %".47", i32 0, i32 %".46")
  %"fmt_size_i32.5" = add i32 %"fmt_needed.5", 1
  %"fmt_size_i64.5" = zext i32 %"fmt_size_i32.5" to i64
  %"fmt_heap_buffer.5" = call i8* @"malloc"(i64 %"fmt_size_i64.5")
  %"fmt_write.5" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer.5", i32 %"fmt_size_i32.5", i8* %".47", i32 0, i32 %".46")
  %".48" = getelementptr inbounds [4 x i8], [4 x i8]* @"__str_2", i32 0, i32 0
  %".49" = call i32 (i8*, ...) @"printf"(i8* %".48", i8* %"fmt_heap_buffer.5")
  call void @"free"(i8* %"fmt_heap_buffer.5")
  %".51" = load i32, i32* %".34"
  ret i32 %".51"
fibonacci_entry.endif.endif:
  %".53" = load i32, i32* %".40"
  %".54" = load i32, i32* %".3"
  %".55" = icmp slt i32 %".53", %".54"
  br i1 %".55", label %"while_loop_entry_14", label %"while_loop_otherwise_14"
while_loop_entry_14:
  %".57" = load i32, i32* %".34"
  %".58" = load i32, i32* %".36"
  %".59" = add i32 %".57", %".58"
  store i32 %".59", i32* %".38"
  %".61" = load i32, i32* %".36"
  store i32 %".61", i32* %".34"
  %".63" = load i32, i32* %".38"
  store i32 %".63", i32* %".36"
  %".65" = load i32, i32* %".40"
  %".66" = add i32 %".65", 1
  store i32 %".66", i32* %".40"
  %".68" = load i32, i32* %".40"
  %".69" = load i32, i32* %".34"
  %".70" = getelementptr inbounds [12 x i8], [12 x i8]* @"__str_13", i32 0, i32 0
  %"fmt_needed.6" = call i32 (i8*, ...) @"_scprintf"(i8* %".70", i32 %".68", i32 %".69")
  %"fmt_size_i32.6" = add i32 %"fmt_needed.6", 1
  %"fmt_size_i64.6" = zext i32 %"fmt_size_i32.6" to i64
  %"fmt_heap_buffer.6" = call i8* @"malloc"(i64 %"fmt_size_i64.6")
  %"fmt_write.6" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer.6", i32 %"fmt_size_i32.6", i8* %".70", i32 %".68", i32 %".69")
  %".71" = getelementptr inbounds [4 x i8], [4 x i8]* @"__str_2", i32 0, i32 0
  %".72" = call i32 (i8*, ...) @"printf"(i8* %".71", i8* %"fmt_heap_buffer.6")
  call void @"free"(i8* %"fmt_heap_buffer.6")
  %".74" = load i32, i32* %".40"
  %".75" = load i32, i32* %".3"
  %".76" = icmp slt i32 %".74", %".75"
  br i1 %".76", label %"while_loop_entry_14", label %"while_loop_otherwise_14"
while_loop_otherwise_14:
  %".78" = load i32, i32* %".34"
  ret i32 %".78"
}

@"__str_8" = internal constant [3 x i8] c"th\00"
@"__str_9" = internal constant [3 x i8] c"st\00"
@"__str_10" = internal constant [3 x i8] c"nd\00"
@"__str_11" = internal constant [3 x i8] c"rd\00"
@"__str_12" = internal constant [39 x i8] c"Calculating the %d%s Fibonacci number\0a\00"
@"__str_13" = internal constant [12 x i8] c"%d | a = %d\00"
define i32 @"akamuri"()
{
akamuri_entry:
  %".2" = call i32 @"fibonacci"(i32 5)
  %".3" = alloca i32
  store i32 %".2", i32* %".3"
  %".5" = load i32, i32* %".3"
  %".6" = alloca i32
  store i32 %".5", i32* %".6"
  %".8" = load i32, i32* %".6"
  %".9" = getelementptr inbounds [29 x i8], [29 x i8]* @"__str_15", i32 0, i32 0
  %"fmt_needed" = call i32 (i8*, ...) @"_scprintf"(i8* %".9", i32 %".8")
  %"fmt_size_i32" = add i32 %"fmt_needed", 1
  %"fmt_size_i64" = zext i32 %"fmt_size_i32" to i64
  %"fmt_heap_buffer" = call i8* @"malloc"(i64 %"fmt_size_i64")
  %"fmt_write" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer", i32 %"fmt_size_i32", i8* %".9", i32 %".8")
  %".10" = getelementptr inbounds [4 x i8], [4 x i8]* @"__str_2", i32 0, i32 0
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".10", i8* %"fmt_heap_buffer")
  call void @"free"(i8* %"fmt_heap_buffer")
  %".13" = load i32, i32* %".6"
  %".14" = call i32 @"factorial"(i32 %".13")
  %".15" = alloca i32
  store i32 %".14", i32* %".15"
  %".17" = load i32, i32* %".6"
  %".18" = load i32, i32* %".15"
  %".19" = getelementptr inbounds [14 x i8], [14 x i8]* @"__str_16", i32 0, i32 0
  %"fmt_needed.1" = call i32 (i8*, ...) @"_scprintf"(i8* %".19", i32 %".17", i32 %".18")
  %"fmt_size_i32.1" = add i32 %"fmt_needed.1", 1
  %"fmt_size_i64.1" = zext i32 %"fmt_size_i32.1" to i64
  %"fmt_heap_buffer.1" = call i8* @"malloc"(i64 %"fmt_size_i64.1")
  %"fmt_write.1" = call i32 (i8*, i32, i8*, ...) @"_snprintf"(i8* %"fmt_heap_buffer.1", i32 %"fmt_size_i32.1", i8* %".19", i32 %".17", i32 %".18")
  %".20" = getelementptr inbounds [4 x i8], [4 x i8]* @"__str_2", i32 0, i32 0
  %".21" = call i32 (i8*, ...) @"printf"(i8* %".20", i8* %"fmt_heap_buffer.1")
  call void @"free"(i8* %"fmt_heap_buffer.1")
  %".23" = load i32, i32* %".15"
  %".24" = call i32 @"loco_adder"(i32 %".23")
  ret i32 %".24"
}

@"__str_15" = internal constant [29 x i8] c"\0aCalculating factorial of %d\00"
@"__str_16" = internal constant [14 x i8] c"   %d! is %d\0a\00"