# Georgios Kefalas
# Dimitrios Papadopoulos

# Python Version 3.10.0

import os
import sys

#====================================================
# Lexical Analyzer
ID = "id"
CONST = "number"
ADD = "addOperator"
MINUS = "addOperator"
MULTI = "mulOperator"
DIV = "mulOperator"
EQL = "relOperator"
LESS = "relOperator"
MORE = "relOperator"
MOREEQ = "relOperator"
LESSEQ = "relOperator"
ANGBR = "relOperator"
ASSIGN = "assignment"
COMMA = "delimeter"
QSTMARK = "delimeter"
LSQBRA = "groupOperator"
RSQBRA = "groupOperator"
LPAR = "groupOperator"
RPAR = "groupOperator"
PERC = "byreference"
ERROR = "error"
EOF="EOF"

RESERVED="keyword"
reserved_words = {
    "πρόγραμμα", "εάν", "επανάλαβε", "για", "διάβασε", "συνάρτηση",
    "είσοδος", "αρχή_συνάρτησης", "αρχή_διαδικασίας", "αρχή_προγράμματος",
    "ή", "δήλωση", "τότε", "μέχρι", "έως", "γράψε", "διαδικασία",
    "έξοδος", "και", "αλλιώς", "όσο", "με_βήμα", "διαπροσωπεία",
    "τέλος_συνάρτησης", "τέλος_διαδικασίας", "τέλος_προγράμματος",
    "όχι", "εκτέλεσε", "εάν_τέλος", "όσο_τέλος", "για_τέλος"
}

class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

    def __repr__(self):
        return f"Token({self.recognized_string}, {self.family}, {self.line_number})"


line_number=1

def lex():
    global line_number, file
    rem=False
    while True:
        char = file.read(1)

        if char == "\n":
            line_number += 1
            continue
        
        if rem:     # xeirismos sxoliwn
            if char=="}":
                rem=False
            elif char == "\n":
                line_number += 1
            elif char == "":    
                print(f"Lectical Error at line {line_number}: Expected closing comment bracket.")
                sys.exit(1)     # Sfalma an den kleinoun ta sxolia
            continue
        
        if char.isspace():  
            continue

        if char == "" or char=="�":
            return Token("eof", EOF,line_number)
           
        

        elif char.isalpha():
            token = char
            while True:
                char = file.read(1)
                if not (char.isalnum() or char == "_"):
                    file.seek(file.tell() - 1)
                    break
                token += char
            if token in reserved_words:
                return Token(token, RESERVED,line_number)
            else:
                if len(token) > 30:
                    print(f"Lectical Error at line {line_number}: word '{token}' exceeds 30 characters.")
                    sys.exit(1)     # Sfalma an leksh panw apo 30 xarakthres
                return Token(token, ID,line_number)      
        
        elif char.isdigit():        
            token = char
            current_line=line_number
            while True:
                char = file.read(1)
                if char.isdigit():
                    token += char
                else:
                    if not (-32767 <= int(token) <= 32767):
                        print(f"Lectical Error at line {line_number}: number {token} is out of range.")
                        sys.exit(1)     #sfalma gia noumero ektos eurous
                    elif char.isalpha():                
                        print(f"Lectical Error at line {line_number}: '{token + char}' is invalid.")
                        sys.exit(1)     # sfalma an ksekinaei apo noumero kai erxetai gramma
                    elif char=="\n":
                        line_number+=1
                    else:
                        file.seek(file.tell() - 1) 
                    return Token(token, CONST, current_line)  
        
        elif char == "+":
            return Token(char, ADD, line_number)
        elif char == "-":
            return Token(char, MINUS, line_number)
        
        elif char == "*":
            return Token(char, MULTI, line_number)
        elif char == "/":
            return Token(char, DIV, line_number)
        
        elif char == "=":
            return Token(char, EQL ,line_number)
            
        elif char == "<":
            token = char
            char = file.read(1)
            if char == "=":
                return Token(token + char, LESSEQ, line_number)
            elif char == ">":
                return Token(token + char, ANGBR, line_number)
            file.seek(file.tell() - 1)
            return Token(token, LESS, line_number)
        
        elif char == ">":
            token = char
            char = file.read(1)
            if char == "=":
                return Token(token + char, MOREEQ,line_number)
            file.seek(file.tell() - 1)
            return Token(token, MORE, line_number)
        
        elif char == ":":
            token = char
            char = file.read(1)     
            if char == "=":
                return Token(token + char, ASSIGN,line_number)
            file.seek(file.tell() - 1)  
            print(f"Lectical Error at line {line_number}:  '{token}' is an invalid expression. Expected ':='.")
            sys.exit(1)     #sfalma, perimename :=
        
        elif char == ",":
            return Token(char, COMMA,line_number)
        elif char == ";":
            return Token(char, QSTMARK, line_number)
        elif char == "(":
            return Token(char, LPAR, line_number)
        elif char == ")":
            return Token(char, RPAR, line_number)
        elif char == "[":
            return Token(char, LSQBRA, line_number)
        elif char == "]":
            return Token(char, RSQBRA, line_number)
        elif char == "%":
            return Token(char, PERC, line_number)
        elif char == "{":
            rem=True
            continue        # xeirismos sxoliwn
        elif char == "}":
            continue
        else:
            print(f"Lectical Error at line {line_number}: '{char}' doesn't belong as character in Greek++.")
            sys.exit(1)     #sfalma agnwstou xarakthra
            

# End of Lexical Analyzer
#====================================================


#====================================================
# Syntax Analyzer
# Intermediate Code Generation
# Symbol Table

class struct:
    def __init__(self):
        self.true_list=[]
        self.false_list=[]


def program():
    global token, line_number, prog_name, sym_table, check_inside_func, func_name

    if token.recognized_string == "πρόγραμμα":
        token = lex()
        if token.family == "id":
            prog_name=token.recognized_string
            token = lex()
            sym_table = SymbolTable()   #dhmiourgia pinaka simvolwn
            sym_table.add_scope()
            sym_table.create_sym_file()
            check_inside_func = 0
            func_name = ""

            programblock()

            if token.recognized_string == "eof":
                quad.writeQuadsToFile()
                #sym_table.print_table()
                sym_table.write_table_to_file()

                offset_of_main = sym_table.get_next_offset()
                generate_final_code(quad, last_emitted_index ,offset_of_main)
                
                sym_table.remove_scope()

                sym_table.write_table_to_file()
                sys.exit(1)     # epitixhs oloklhrwsh suntaktikou analuth
            else:
                print(f"Syntax Error at line {line_number}: Expected EOF")
                sys.exit(1)

        else:
            print(f"Syntax Error at line {line_number}: Expected the name of the program")
            sys.exit(1)
    else:
        print(f"Syntax Error at line {line_number}: All programs should start with the keyword 'πρόγραμμα'")
        sys.exit(1)

def programblock():
    global token,prog_name, check_inside_func

    declarations()
    subprograms()
    if token.recognized_string == "αρχή_προγράμματος":
        token = lex()
        quad.genQuad("begin_block",prog_name,"_","_")
        check_inside_func = 0
        sequence()

        if token.recognized_string == "τέλος_προγράμματος":
            quad.genQuad("halt","_","_","_")
            quad.genQuad("end_block",prog_name,"_","_")
            token = lex()

        else:
            print(f"Syntax Error at line {line_number}: Expected 'τέλος_προγράμματος'")
            sys.exit(1)
    else:
        print(f"Syntax Error at line {line_number}: Expected 'αρχή_προγράμματος'")
        sys.exit(1)    

def declarations():
    global token
    while token.recognized_string == "δήλωση":
        token = lex()
        varlist(0)

def varlist(functionality): # 0 se declaration, 1 gia parametro cv, 2 parametro ref
    global token
    if token.family == "id":
        if functionality ==0:
            sym_table.add_entry(Variable(token.recognized_string, "int", None))
        elif functionality == 1:
            sym_table.add_entry(Parameter(token.recognized_string, "cv", None))
        elif functionality == 2:
            sym_table.add_entry(Parameter(token.recognized_string, "ref", None))

        token = lex()

        while token.recognized_string ==",":
            token = lex()

            if token.family == "id":
                if functionality ==0:
                    sym_table.add_entry(Variable(token.recognized_string, "int", None))
                elif functionality == 1:
                    sym_table.add_entry(Parameter(token.recognized_string, "cv", None))
                elif functionality == 2:
                    sym_table.add_entry(Parameter(token.recognized_string, "ref", None))

                token = lex()
            else:
                print(f"Syntax Error at line {line_number}: Expected identifier")
                sys.exit(1)
    else:
        print(f"Syntax Error at line {line_number}: Expected identifier")
        sys.exit(1)

def subprograms():
    global token
    while token.recognized_string == "συνάρτηση" or token.recognized_string == "διαδικασία":
        if token.recognized_string == "συνάρτηση":
            func()
        else:
            proc()

def func():
    global token, func_table, func_name
    
    if token.recognized_string == "συνάρτηση":
        token = lex()
        func_name=token.recognized_string

        func_table = Function(func_name,"int",None,None,[])
        sym_table.add_entry(func_table)
        sym_table.add_scope()

        if token.family == "id":
            token = lex()

            if token.recognized_string == "(":
                token = lex()
                formalparlist()

                if token.recognized_string ==")":
                    token = lex()
                    funcblock()
                else:
                    print(f"Syntax Error at line {line_number}: Expected ')'")
                    sys.exit(1)

            else:
                print(f"Syntax Error at line {line_number}: Expected '('")
                sys.exit(1)

        else:
            print(f"Syntax Error at line {line_number}: Expected identifier")
            sys.exit(1)

    else:
        print(f"Syntax Error at line {line_number}: Expected 'συνάρτηση'")
        sys.exit(1)


def proc():
    global token, proc_table, proc_name

    if token.recognized_string == "διαδικασία":
        token = lex()
        proc_name=token.recognized_string

        proc_table = Procedure(proc_name,None,None,[])
        sym_table.add_entry(proc_table)
        sym_table.add_scope()

        if token.family == "id":
            token = lex()

            if token.recognized_string == "(":
                token = lex()
                formalparlist()
                if token.recognized_string == ")":
                    token = lex()
                    procblock()
                else:
                    print(f"Syntax Error at line {line_number}: Expected ')'")
                    sys.exit(1)
            else:
                print(f"Syntax Error at line {line_number}: Expected '('")
                sys.exit(1)
        else:
            print(f"Syntax Error at line {line_number}: Expected identifier")
            sys.exit(1)
    else:
        print(f"Syntax Error at line {line_number}: Expected 'διαδικασία'")
        sys.exit(1)

def formalparlist():
    global token
    if token.family == "id":
        varlist(None)
    #else: ε

def funcblock():
    global token, end_of_func, check_inside_func, last_emitted_index, func_name
    if token.recognized_string == "διαπροσωπεία":
        token = lex()

        funcinput(0)
        funcoutput(0)
        declarations()
        current_name = func_name
        subprograms()
        end_of_func = 0

        if token.recognized_string == "αρχή_συνάρτησης":
            check_inside_func = 1
            decl_func = quad.genQuad("begin_block",current_name,"_","_")
            start_of_func = decl_func
            sym_table.update_entry(current_name,startingQuad=start_of_func)  #arxh endiamsou kwdika sunartishs

            token = lex()
            sequence()
            if token.recognized_string=="τέλος_συνάρτησης":
                
                if (end_of_func == 0):
                    print(f"Semantic Error at line {line_number}: No return call ({func_table.name})")
                    sys.exit(1) #SIMASIOLOGIKH ANALISH 5 '''
                quad.genQuad("end_block",current_name,"_","_")
                #sym_table.print_table()
                sym_table.write_table_to_file()

                last_emitted_index = generate_final_code(quad, last_emitted_index ,None)
                sym_table.remove_scope()
                token = lex()
            else:
                print(f"Syntax Error at line {line_number}: Expected 'τέλος_συνάρτησης'")
                sys.exit(1)
        else:
            print(f"Syntax Error at line {line_number}: Expected 'αρχή_συνάρτησης'")
            sys.exit(1)

    else:
        print(f"Syntax Error at line {line_number}: Expected 'διαπροσωπεία'")
        sys.exit(1)

def procblock():
    global token, check_inside_func, last_emitted_index, proc_name
    if token.recognized_string == "διαπροσωπεία":
        token = lex()

        funcinput(1)
        funcoutput(1)
        declarations()
        current_name = proc_name
        subprograms()

        if token.recognized_string == "αρχή_διαδικασίας":
            check_inside_func = 0
            decl_proc = quad.genQuad("begin_block",current_name,"_","_")
            start_of_proc = decl_proc
            sym_table.update_entry(current_name,startingQuad=start_of_proc)    #arxh endiamesou kwdika diadikasias
            token = lex()
            sequence()
            if token.recognized_string == "τέλος_διαδικασίας":
                quad.genQuad("end_block",current_name,"_","_")
                #sym_table.print_table()
                sym_table.write_table_to_file()

                last_emitted_index = generate_final_code(quad, last_emitted_index ,None)
                sym_table.remove_scope()
                token = lex()
            else:
                print(f"Syntax Error at line {line_number}: Expected 'τέλος_διαδικασίας'")
                sys.exit(1)
        else:
            print(f"Syntax Error at line {line_number}: Expected 'αρχή_διαδικασίας'")
            sys.exit(1)
    else:
        print(f"Syntax Error at line {line_number}: Expected 'διαπροσωπεία'")
        sys.exit(1)

def funcinput(functionality):   # CV / 0 gia function, 1 gia diadikasia 
    global token, func_table, proc_table
    if token.recognized_string == "είσοδος":
        token = lex()

        if functionality == 0:
            sym_table.add_formal_parameter(func_table.name, "int", "in")
        elif functionality == 1:
            sym_table.add_formal_parameter(proc_table.name, "int", "in")
        
        varlist(1)
    # else ε

def funcoutput(functionality):      # REF / 0 gia function, 1 gia diadikasia 
    global token, func_table, proc_table
    if token.recognized_string == "έξοδος":
        token = lex()

        if functionality == 0:
            sym_table.add_formal_parameter(func_table.name, "int", "out")
        elif functionality == 1:
            sym_table.add_formal_parameter(proc_table.name, "int", "out")

        varlist(2)
    # else ε

def sequence():
    global token
    statement()
    while token.recognized_string == ";":
        token = lex()
        statement()

def statement():
    global token
    if token.family == "id":
        assignment_stat()
    elif token.recognized_string == "εάν":
        if_stat()
    elif token.recognized_string == "όσο":
        while_stat()
    elif token.recognized_string == "επανάλαβε":
        do_stat()
    elif token.recognized_string == "για":
        for_stat()
    elif token.recognized_string == "διάβασε":
        input_stat()
    elif token.recognized_string == "γράψε":
        print_stat()
    elif token.recognized_string == "εκτέλεσε":
        call_stat()
    else:
        print(f"Syntax Error at line {line_number}: Invalid statement")
        sys.exit(1)

def assignment_stat():
    global token, end_of_func, func_name
    ret_int = 0
    if token.family == "id":
        target=token.recognized_string

        check_func_return = sym_table.find_entry(target)    # simasiologikh analish 1
        
        if ((target == func_name) and (check_inside_func == 1)):   #gia simasiologikh analish 5
            end_of_func = 1        #gia simasiologikh analish 5
            ret_int = 1
        elif ((isinstance(check_func_return,Function)) and (check_inside_func == 0)):
            print(f"Semantic Error at line {line_number}: Return call '{target}' outside of Function.")
            sys.exit(1) #SIMASIOLOGIKH ANALISH 4'''

        token = lex()

        if token.recognized_string == ":=":
            token = lex()
            source=expression()
            #quad.genQuad(":=",source,"_",target)
            if (ret_int == 1):
                quad.genQuad("ret",source,"_","_")
                ret_int = 0
            else:
                quad.genQuad(":=",source,"_",target)
        else:
            print(f"Syntax Error at line {line_number}: Expected ':='")
            sys.exit(1)
    else:
        print(f"Syntax Error at line {line_number}: Expected identifier")
        sys.exit(1)

def if_stat():
    global token

    # den xreiazetai if gia to εαν
    token = lex()
    cond=condition()
    quad.backpatch(cond.true_list,quad.nextQuad())
    if token.recognized_string == "τότε":
        token = lex()
        sequence()

        ifList=quad.makeList(quad.nextQuad())
        quad.genQuad("jump","_","_","_")
        quad.backpatch(cond.false_list,quad.nextQuad())

        elsepart()

        quad.backpatch(ifList,quad.nextQuad())

        if token.recognized_string == "εάν_τέλος":
            token = lex()
        else:
            print(f"Syntax Error at line {line_number}: Expected 'εάν_τέλος'")
            sys.exit(1)
    else:
        print(f"Syntax Error at line {line_number}: Expected 'τότε'")
        sys.exit(1)

def elsepart():
    global token
    if token.recognized_string == "αλλιώς":
        token = lex()
        sequence()
    # else ε

def while_stat():
    global token
    # δεν χρειαζεται if για το "οσο"
    token = lex()

    condQuad = quad.nextQuad()  #P0
    cond = condition()          # CONDITION
    quad.backpatch(cond.true_list, quad.nextQuad())    #P1

    if token.recognized_string == "επανάλαβε":
        token = lex()
        sequence()

        quad.genQuad("jump", "_", "_", condQuad)    #P2
        quad.backpatch(cond.false_list, quad.nextQuad())
            
        if token.recognized_string == "όσο_τέλος":
            token = lex()
        else:
            print(f"Syntax Error at line {line_number}: Expected 'όσο_τέλος'")
            sys.exit(1)
    else:
        print(f"Syntax Error at line {line_number}: Expected 'επανάλαβε'")
        sys.exit(1)

def do_stat():
    global token

    # δεν χρειαζεται if για το "επανάλαβε"
    token = lex()
    seqQuad=quad.nextQuad()
    sequence()
    if token.recognized_string == "μέχρι":
        token = lex()
        cond= condition()
        quad.backpatch(cond.true_list, quad.nextQuad())
        quad.backpatch(cond.false_list, seqQuad)
    else:
        print(f"Syntax Error at line {line_number}: Expected 'μέχρι'")
        sys.exit(1)



def for_stat():
    global token
    # δεν χρειαζεται if για το "για"
    token = lex()
    if token.family == "id":
        loop_var = token.recognized_string

        sym_table.find_entry(loop_var) #simasiologikh analush 1
        token = lex()

        if token.recognized_string == ":=":
            token = lex()

            start_expr = expression()
            quad.genQuad(":=", start_expr, "_", loop_var) #i = expr1
            startQuad = quad.nextQuad() #l1
            
            if token.recognized_string == "έως":
                token = lex()

                end_expr = expression() #!! telikh timh

                step_expr = step()  #vhma
                if (step_expr[0] == 'T'):   #an step arnhtiko girnaei proswrinh metavlhth, px T@11
                    step_is_positive = False    
                else:
                    step_is_positive = True

                if token.recognized_string == "επανάλαβε":
                    token = lex()

                    conditionQuad = quad.nextQuad()
                    if step_is_positive==True:    # dhmiourgia tetradas analogh toy step
                        #if i > expr
                        quad.genQuad(">=",loop_var, end_expr, "_")
                    else:
                        quad.genQuad("<=",loop_var, end_expr, "_")

                    sequence()

                    temp = quad.newTemp()   #upologismos neou i
                    sym_table.add_entry(TempVariable(temp,None))
                    quad.genQuad("+", loop_var, step_expr, temp)
                    quad.genQuad(":=", temp, "_", loop_var)


                    quad.genQuad("jump", "_", "_", startQuad)

                    quad.backpatch([conditionQuad], quad.nextQuad())    #simplirwsh proorismou sto arxiko condition tou for
                    
                    if token.recognized_string == "για_τέλος":
                        token = lex()
                    else:
                        print(f"Syntax Error at line {line_number}: Expected 'για_τέλος'")
                        sys.exit(1)
                else:
                    print(f"Syntax Error at line {line_number}: Expected 'επανάλαβε'")
                    sys.exit(1)
            else:
                print(f"Syntax Error at line {line_number}: Expected 'έως'")
                sys.exit(1)
        else:
            print(f"Syntax Error at line {line_number}: Expected ':='")
            sys.exit(1)
    else:
        print(f"Syntax Error at line {line_number}: Expected identifier")
        sys.exit(1)

def step():
    global token
    if token.recognized_string == "με_βήμα":
        token = lex()
        return expression()
    #else 
    return "0"

def print_stat():
    global token
    # δεν χρειαζεται if για το "γράψε"
    token = lex()
    x = expression()
    quad.genQuad("out",x,"_","_")


def input_stat():
    global token
    # δεν χρειαζεται if για το "διαβασε"
    token = lex()

    if token.family == "id":
        sym_table.find_entry(token.recognized_string)
        quad.genQuad("in",token.recognized_string,"_","_")
        token = lex()
    else:
        print(f"Syntax Error at line {line_number}: Expected identifier after 'διάβασε'")
        sys.exit(1)
    

def call_stat():
    global token
    # δεν χρειαζεται if για το "εκτέλεσε"
    token = lex()
    if token.family == "id":
        pname=token.recognized_string
        check_if_proc = sym_table.find_entry(pname)     #simasiologikh 1
        if not isinstance(check_if_proc, Procedure):
            print(f"Semantic Error at line {line_number}: Entity '{pname}' is not a Procedure")
            sys.exit(1) #SIMASIOLOGIKH ANALISH 6
        token = lex()
        idtail(pname)
        for i in range(len(formal_pars)):
            if not (formal_pars[i] == check_if_proc.formalParameters[i].mode):
                print(f"Semantic Error at line {line_number}: Wrong parameter given for Procedure '{pname}'")
                sys.exit(1) #SIMASIOLOGIKH ANALISH 7
        quad.genQuad("call",pname,"_","_")
    else:
        print(f"Syntax Error at line {line_number}: Expected identifier after 'εκτέλεσε'")
        sys.exit(1)


def idtail(caller_name):
    global token, formal_pars
    formal_pars = []
    
    if token.recognized_string == "(":
        actualpars(caller_name)
        return 1
    # else ε
    return 0

def actualpars(caller_name):
    global token
    # δεν χρειαζεται if για το "("
    token = lex()
    actualparlist(caller_name)
    if token.recognized_string == ")":
        token = lex()
    else:
        print(f"Syntax Error at line {line_number}: Expected ')'")
        sys.exit(1)


def actualparlist(caller_name):
    global token
    if (token.family == "number" or token.family == "id" or token.recognized_string == "%" or token.recognized_string == "("):
        actualparitem(caller_name)
        while token.recognized_string == ",":
            token = lex()
            actualparitem(caller_name)
    # else ε
    

def actualparitem(caller_name):
    global token, formal_pars
    if token.recognized_string == "%":
        token = lex()
        quad.genQuad("par",token.recognized_string,"ref",caller_name)
        formal_pars.append("out")
        if token.family == "id":
            token = lex()
        else:
            print(f"Syntax Error at line {line_number}: Expected identifier after '%'")
            sys.exit(1)
    else:
        par=expression()
        quad.genQuad("par",par,"cv",caller_name)
        formal_pars.append("in")


def condition():
    b_str=struct()
    global token

    q_str1=boolterm() #Q1
    b_str.true_list=q_str1.true_list
    b_str.false_list=q_str1.false_list

    while token.recognized_string == "ή":
        token = lex()
        
        quad.backpatch(b_str.false_list,quad.nextQuad())
        q_str2=boolterm() #Q2
        b_str.true_list=quad.mergeList(b_str.true_list,q_str2.true_list)
        b_str.false_list=q_str2.false_list
    return  b_str
        
def boolterm():
    q_str=struct()
    global token

    factor1=boolfactor() #R1
    q_str.true_list=factor1.true_list
    q_str.false_list=factor1.false_list

    while token.recognized_string == "και":
        token = lex()

        quad.backpatch(q_str.true_list,quad.nextQuad())
        factor2=boolfactor() #R2
        q_str.false_list=quad.mergeList(q_str.false_list,factor2.false_list)
        q_str.true_list=factor2.true_list
    return q_str


def boolfactor():
    r_str=struct()
    global token
    if token.recognized_string == "όχι":
        token = lex()
        if token.recognized_string == "[":
            token = lex()
            b_str=condition() #B
            if token.recognized_string == "]":
                token = lex()
                r_str.true_list=b_str.false_list
                r_str.false_list=b_str.true_list
                return r_str
            else:
                print(f"Syntax Error at line {line_number}: Expected ']'")
                sys.exit(1)
            
        else:
            print(f"Syntax Error at line {line_number}: Expected '[' after 'όχι'")
            sys.exit(1)

    elif token.recognized_string == "[":
        token = lex()
        b_str=condition()
        if token.recognized_string == "]":
            token = lex()
            r_str.true_list=b_str.true_list
            r_str.false_list=b_str.false_list
            return r_str
        else:
            print(f"Syntax Error at line {line_number}: Expected ']'")
            sys.exit(1)
    else:
        eplace1 = expression()
        real_op=relational_oper()
        eplace2 = expression()
        r_str.true_list=quad.makeList(quad.nextQuad())
        quad.genQuad(real_op,eplace1,eplace2,"_")
        r_str.false_list=quad.makeList(quad.nextQuad())
        quad.genQuad("jump","_","_","_")
        return r_str
        

def expression():
    global token
    ifminus = optional_sign()
    t1place = term()
    newtemp = None
    if ifminus == "-":      #xeirismos arnhtikwn arithmwn
        newtemp = quad.newTemp()
        sym_table.add_entry(TempVariable(newtemp,None))
        quad.genQuad(ifminus,"0",t1place,newtemp)

    while (token.recognized_string == "+" or token.recognized_string == "-"):
        oper = add_oper()
        t2place = term()
        w=quad.newTemp()
        sym_table.add_entry(TempVariable(w,None))
        quad.genQuad(oper,t1place,t2place,w)
        t1place=w
    
    if ifminus == "-":      #xeirismos arnhtikwn arithmwn
            eplace=newtemp
            return eplace
    
    eplace=t1place
    return eplace

def term():
    f1place = factor()
    while (token.recognized_string == "*" or token.recognized_string == "/"):
        oper = mul_oper()
        f2place = factor()
        w=quad.newTemp()
        sym_table.add_entry(TempVariable(w,None))
        quad.genQuad(oper,f1place,f2place,w)
        f1place=w
    
    tplace=f1place
    return tplace

def factor():
    global token, func_name
    if token.family == "number":
        fplace=token.recognized_string
        token = lex()
        return fplace
    elif token.recognized_string == "(":
        token = lex()
        eplace = expression()
        if token.recognized_string == ")":
            fplace = eplace
            token = lex()
            return fplace
        else:
            print(f"Syntax Error at line {line_number}: Expected ')'")
            sys.exit(1)
    elif token.family == "id":
        fplace= token.recognized_string
        #func_name = token.recognized_string
        random_entity = sym_table.find_entry(fplace)    # simasiologikh analish 1
        token = lex()
        check_func = idtail(fplace)
        if check_func == 1:
            if not isinstance(random_entity, Function):
                print(f"Semantic Error at line {line_number}: Entity '{fplace}' is not a Function")
                sys.exit(1) #SIMASIOLOGIKH ANALISH 6
            for i in range(len(formal_pars)):
                if (formal_pars[i] != random_entity.formalParameters[i].mode):
                    print(f"Semantic Error at line {line_number}: Wrong parameter given for Function '{fplace}'")
                    sys.exit(1) #SIMASIOLOGIKH ANALISH 7
            w = quad.newTemp()
            sym_table.add_entry(TempVariable(w,None))
            quad.genQuad("par", w, "ret", fplace)
            quad.genQuad("call",fplace,"_","_")
            return w
        return fplace
    else:
        print(f"Syntax Error at line {line_number}: Expected number, identifier, or '('")
        sys.exit(1)

def relational_oper():
    global token
    if token.recognized_string in {"=", "<=", ">=", "<>", "<", ">"}:
        oper=token.recognized_string
        token = lex()
        return oper
    else:
        print(f"Syntax Error at line {line_number}: Expected relational operator")
        sys.exit(1)

def add_oper():
    global token
    if (token.recognized_string == "+" or token.recognized_string == "-"):
        oper=token.recognized_string
        token = lex()
        return oper
    else:
        print(f"Syntax Error at line {line_number}: Expected '+' or '-'")
        sys.exit(1)
        

def mul_oper():
    global token
    if (token.recognized_string == "*" or token.recognized_string == "/"):
        oper=token.recognized_string
        token = lex()
        return oper
    else:
        print(f"Syntax Error at line {line_number}: Expected '*' or '/'")
        sys.exit(1)
        

def optional_sign():
    global token
    if (token.recognized_string == "+" or token.recognized_string == "-"):
        oper=token.recognized_string
        token = lex()
        return oper
    # else ε

def syntax_analyzer():
    global token
    token = lex()
    program()

# End of Syntax Analyzer
# End of Intermediate Code Generation
# End of Symbol Table
#====================================================


#====================================================
# Intermediate Code Helper Functions

class Quad:
    def __init__(self):
        self.quads = []  # lista tetradwn
        self.temp_count = 0  # metrhthw gia proswrines metavlhtes
        self.quad_count = 1  # metrhths gia tetrades

    def genQuad(self, operator, operand1, operand2, operand3):
        """Dimiourgei mia nea tetrada kai thn apothikeuei sth lista."""
        quad = (operator, operand1, operand2, operand3)
        self.quads.append(quad)
        self.quad_count += 1
        return self.quad_count - 1  # epistrefei to index ths tetradas

    def nextQuad(self):
        """Epistrefei ton arithmo ths epomenhs tetradas pou tha dhmiourgithei."""
        return self.quad_count

    def newTemp(self):
        """Dhmiourgei mia proswrinh nea metavlhth."""
        self.temp_count += 1
        return f"T@{self.temp_count}"

    def emptyList(self):
        """Dhmiourgei mia kenh lista gia etiketes tetradwn."""
        return []

    def makeList(self, label):
        """Dhmiourgei mia lista pou periexei ena label."""
        return [label]

    def mergeList(self, list1, list2):
        """kanei merge duo listes apo labels."""
        return list1 + list2

    def backpatch(self, lst, label):
        """Enimerwnei tis tetrades sth lista lst wste na deixnoun sthn etiketa label."""
        for quad_id in lst:
            index = quad_id -1
            self.quads[index] = (
                self.quads[index][0],  # operator
                self.quads[index][1],  # operand1
                self.quads[index][2],  # operand2
                label                    # operand3 (backpatch)
            )

    def printQuads(self):
        """Ektupwnei oles tis tetrades."""
        for i, quad in enumerate(self.quads, start=1):
            print(f"{i}: {quad}")

    def writeQuadsToFile(self):
        """Grafei tis tetrades se ena arxeio endiamesos.int."""
        with open(name_endiamesos, "w", encoding="utf-8") as file:
            for i, quad in enumerate(self.quads, start=1):
                file.write(f"{i} : {quad[0]} , {quad[1]} , {quad[2]} , {quad[3]}\n")

# End of Intermediate Code Helper Functions
#====================================================
    

#====================================================
# Symbol Generation Helper Functions

class Variable:
    def __init__(self, name, datatype, offset):
        self.name = name
        self.datatype = datatype
        self.offset = offset

    def __repr__(self):
        return f"Variable(n={self.name}, t={self.datatype}, o={self.offset})"

class Parameter:
    def __init__(self, name, mode, offset):
        self.name = name
        self.mode = mode
        self.offset = offset

    def __repr__(self):
        return f"Parameter(n={self.name}, m={self.mode}, o={self.offset})"

class Procedure:
    def __init__(self, name, startingQuad, frameLength, formalParameters):
        self.name = name
        self.startingQuad = startingQuad
        self.frameLength = frameLength
        self.formalParameters = formalParameters  # lista apo Parameter

    def __repr__(self):
        return f"Procedure(n={self.name}, sQ={self.startingQuad}, fL={self.frameLength}, fP={self.formalParameters})"

class Function:
    def __init__(self, name, datatype, startingQuad, frameLength, formalParameters):
        self.name = name
        self.datatype = datatype
        self.startingQuad = startingQuad
        self.frameLength = frameLength
        self.formalParameters = formalParameters  # lista apo Parameter

    def __repr__(self):
        return f"Function(n={self.name}, t={self.datatype}, sQ={self.startingQuad}, fL={self.frameLength}, fP={self.formalParameters})"

class FormalParameter:
    def __init__(self, datatype, mode):
        self.datatype = datatype
        self.mode = mode

    def __repr__(self):
        return f"FormalParameter(t={self.datatype}, m={self.mode})"

class TempVariable:
    def __init__(self, name, offset):
        self.name = name
        self.offset = offset

    def __repr__(self):
        return f"TempVariable(n={self.name}, o={self.offset})"

class SymbolTable:
    def __init__(self):
        self.stack = []  # Stoiva epipedwn, kathe epipedo einai mia lista eggrafwn
        self.offsets = []  # Diathrei to trexon offset gia kathe epipedo

    def add_scope(self):
        """Prosthetei ena neo epipedo ston pinaka sumvolwn."""
        self.stack.append([])
        self.offsets.append(12)  # Kathe neo scope ksekina me offset 12

    def remove_scope(self):
        """Afairei to pio prosfato epipedo tou pinaka sumvolwn kai enhmervnei to FrameLength an uparxei sunarthsh h diadikasia."""
        if not self.stack:
            raise RuntimeError("No scope available to remove.")

        removed_scope = self.stack.pop()
        next_offset = self.offsets.pop()

        # vriskoume teleftaia Function h Procedure prin to current scope
        for scope in reversed(self.stack):
            for entry in reversed(scope):
                if isinstance(entry, (Function, Procedure)):
                    entry.frameLength = next_offset  # enhmerwsh frameLength
                    return next_offset

        return next_offset
    
    def next_offset(self):
        next_offset = self.offsets.pop()
        return next_offset

    def add_entry(self, entry):
        """Prosthetei mia nea eggrafh sto trexon epipedo."""
        if not self.stack:
            print(f"No scope available to add an entry.")
            sys.exit(1)
        
        # trexon epipedo
        current_scope = self.stack[-1]

        # an iparxei eggrafh me ayto to onoma
        if any(hasattr(e, "name") and e.name == entry.name for e in current_scope):
            print(f"Semantic Error at line {line_number}: Entity '{entry.name}' has already been declared in this scope")
            sys.exit(1) #SIMASIOLOGIKH ANALISH 2

        # an den einai Function h Procedure pairnoume to epomeno offset
        if not isinstance(entry, (Function, Procedure)):
            if hasattr(entry, "offset"):
                entry.offset = self.get_next_offset()
                
        current_scope.append(entry)

    def find_entry(self, name):
        """Anazhta mia eggrafh apo to pio prosfato pros to palaiotero epipedo."""
        for scope in reversed(self.stack):
            for entry in scope:
                if hasattr(entry, "name") and entry.name == name:
                    return entry
        print(f"Semantic Error at line {line_number}: Entity '{name}' not found in symbol table.")
        sys.exit(1) #SIMASIOLOGIKH ANALISH 1  

    def find_entry_level(self, name):
        """Επιστρέφει το επίπεδο (index) στο οποίο βρίσκεται η εγγραφή με το δοσμένο όνομα."""
        for level in reversed(range(len(self.stack))):
            scope = self.stack[level]
            for entry in scope:
                if hasattr(entry, "name") and entry.name == name:
                    return level

    def update_entry(self, name, **kwargs):
        """Enhmerwnei ta pedia mia eggrafhs."""
        entry = self.find_entry(name)
        if entry:
            for key, value in kwargs.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)
        else:
            raise KeyError(f"Entry '{name}' not found.")
        
    def add_formal_parameter(self, proc_or_func_name, datatype, mode):
        """Prosthetei mia tupikh parametro se mia sunarthsh h diadikasia pou uparxei hdh."""
        entry = self.find_entry(proc_or_func_name)
    
        if entry and isinstance(entry, (Function, Procedure)):
            param = FormalParameter(datatype, mode)
            entry.formalParameters.append(param)
        else:
            raise KeyError(f"Function or Procedure '{proc_or_func_name}' not found in symbol table.")

        
    def get_nesting_level(self):
        return len(self.stack) - 1

    def print_table(self):
        print("\n--- Symbol Table ---")
        for i, scope in enumerate(self.stack):
            print(f"Scope {i} (Level {i}):")
            for entry in scope:
                print(f"  {entry}")
        print("--------------------\n")

    def get_next_offset(self):
        """Epistrefei to trexon offset kai to auksanei kata 4, ektos an einai Function h Procedure."""
        if not self.offsets:
            raise RuntimeError("No scope available to calculate offset.")
        
        current_offset = self.offsets[-1]
        self.offsets[-1] += 4  # auksanoume to offset kata 4 gia thn epomenh metavlhth
        return current_offset
    
    def create_sym_file(self):
        self.sym_filename = name_symtable
        with open(self.sym_filename, "w", encoding="utf-8") as f:
            f.write("--- Symbol Table ---\n")

    def write_table_to_file(self):
        if not hasattr(self, 'sym_filename'):
            print("Error: Symbol file not created yet.")
            return

        with open(self.sym_filename, "a", encoding="utf-8") as f:
            for i, scope in enumerate(self.stack):
                f.write(f"Scope {i} (Level {i}):\n")
                for entry in scope:
                    f.write(f"  {entry}\n")
            f.write("--------------------\n")

    def __repr__(self):
        return "\n".join(f"Scope {i}: {scope}" for i, scope in enumerate(self.stack))

# End of Symbol Generation Helper Functions
#====================================================
# Final Code Generation Helper Functions
assmebly_instr=[]

def make_final_code_file():
    
    # Δημιουργεί ή καθαρίζει το αρχείο
    with open(name_telikos, "w") as f:
        f.write("\t.data\n")
        f.write('\tstr_nl: .asciz "\\n"\n')
        f.write("\t.text\n\n")
    get_risc_instr("L",[-1])
    get_risc_instr("j",["Lmain"])


def get_risc_instr(op,terms):
    if op in ["li","la","mv"]:
        line = "\t{} {}, {}".format(op, terms[0], terms[1])
    elif op in ["lw","sw"]:
        line = "\t{} {}, {}({})".format(op, terms[0], terms[1], terms[2])
    elif op in ['add', 'addi', 'sub', 'subu', 'mul', 'div', 'beq', 'blt', 'bgt', 'ble', 'bge', 'bne']:
        line = "\t{} {}, {}, {}".format(op, terms[0], terms[1], terms[2])
    elif op in ['j', 'jal', 'jr', 'b']:
	    line = "\t{} {}".format(op, terms[0])
    elif op in ["ecall"]:
        line = "\t{}".format(op)
    elif op in ["L"]:
        if terms[0] == "main":
            line = "L{}:".format(terms[0])
        else:
            line = "\nL{}:".format(terms[0]+1)
    else:
        return
    with open(name_telikos, "a") as f:
        f.write(line + "\n")
    
def is_local(var):
    level = sym_table.find_entry_level(var)
    return level == sym_table.get_nesting_level()

def is_global(var):
    level= sym_table.find_entry_level(var)
    return level==0

def is_temp_var(var):
    if isinstance(var,TempVariable):
        return True
    else:
        return False
    
def is_parameter(var):
    if isinstance(var,Parameter):
        return True
    else:
        return False
    
def is_variable(var):
    if isinstance(var,Variable):
        return True
    else:
        return False   

def is_cv_par(var):
    if isinstance(var,Parameter) and var.mode == "cv":
        return True
    else:
        return False 

def is_ref_par(var):
    if isinstance(var,Parameter) and var.mode == "ref":
        return True
    else:
        return False 
    
def belongs_ancestor(var):
    level = sym_table.find_entry_level(var)
    current_level = sym_table.get_nesting_level()
    return 0 <= level < current_level

def gnlvcode(var):
    global assmebly_instr

    item=sym_table.find_entry(var)
    dest_level=sym_table.find_entry_level(var)
    cur_level=sym_table.get_nesting_level()
    levels_to_hop=cur_level-dest_level

    get_risc_instr("lw",["t0","-4","sp"])   #vgainei ektos tou epipedou tou
    
    for i in range (levels_to_hop-1,0,-1):  # N-1
        get_risc_instr("lw",["t0","-4","t0"])
    get_risc_instr("addi",["t0","t0",str(-item.offset)])

def loadvr(var,reg):
    global assmebly_instr
    if var.isdigit():
        get_risc_instr("li",[reg,var])
    else:
        item = sym_table.find_entry(var)
        offset= item.offset
        if is_local(var):
            if is_cv_par(item) or is_temp_var(item) or is_variable(item):
                get_risc_instr("lw",[reg , str(-offset), "sp"])
            elif is_ref_par(item):
                get_risc_instr("lw",["t0" , str(-offset), "sp"])
                get_risc_instr("lw",[reg , 0, "t0"])
        elif is_global(var):
            get_risc_instr("lw",[reg, str(-offset), "gp"])
        elif is_variable(item) or is_cv_par(item):
            gnlvcode(var)
            get_risc_instr("lw",[reg , 0, "t0"])
        elif is_ref_par(item):
            gnlvcode(var)
            get_risc_instr("lw",["t0" , 0, "t0"])
            get_risc_instr("lw",[reg , 0, "t0"])

def storerv(reg,var):
    global assmebly_instr
    if var.isdigit():
        get_risc_instr("li",[reg,var])   #!!!!!!!!
    else:
        item = sym_table.find_entry(var)
        
        if is_local(var):
            if is_cv_par(item) or is_temp_var(item) or is_variable(item):
                offset= item.offset
                get_risc_instr("sw",[reg , str(-offset), "sp"])
            elif is_ref_par(item):
                offset= item.offset
                get_risc_instr("lw",["t0" , str(-offset), "sp"])
                get_risc_instr("sw",[reg , 0, "t0"])
        elif is_global(var):
            offset= item.offset
            get_risc_instr("sw",[reg, str(-offset), "gp"])
        elif is_variable(item) or is_cv_par(item):
            gnlvcode(var)
            get_risc_instr("sw",[reg , 0, "t0"])
        elif is_ref_par(item):
            gnlvcode(var)
            get_risc_instr("lw",["t0" , 0, "t0"])
            get_risc_instr("sw",[reg , 0, "t0"])


def generate_final_code(quad_obj, start_index, framelength_main):
    end_index = len(quad_obj.quads)
    index_par = 0
    
    for i in range(start_index, end_index):
        op, arg1, arg2, result = quad_obj.quads[i]
        # === RISC-V GENERATION ===
        if op == ':=':
            get_risc_instr("L",[i])
            loadvr(arg1,"t1")
            storerv("t1", result)
        elif op == '+':
            get_risc_instr("L",[i])
            loadvr(arg1,"t1")
            loadvr(arg2,"t2")
            get_risc_instr("add", ["t1", "t1", "t2"])
            storerv("t1", result)
        elif op == '-':
            get_risc_instr("L",[i])
            loadvr(arg1,"t1")
            loadvr(arg2,"t2")
            get_risc_instr("sub", ["t1", "t1", "t2"])
            storerv("t1", result)
        elif op == '*':
            get_risc_instr("L",[i])
            loadvr(arg1,"t1")
            loadvr(arg2,"t2")
            get_risc_instr("mul", ["t1", "t1", "t2"])
            storerv("t1", result)
        elif op == '/':
            get_risc_instr("L",[i])
            loadvr(arg1,"t1")
            loadvr(arg2,"t2")
            get_risc_instr("div", ["t1", "t1", "t2"])
            storerv("t1", result)
        elif op in ['<', '<=', '>', '>=', '=', '<>']:
            branch_map = {
                '=': "beq",
                '<>': "bne",
                '<': "blt",
                '<=': "ble",
                '>': "bgt",
                '>=': "bge"
            }
            risc_op = branch_map[op]
            get_risc_instr("L",[i])
            loadvr(arg1, "t1")
            loadvr(arg2,"t2")
            get_risc_instr(risc_op, ["t1", "t2", f"L{result}"])
        elif op == 'jump':
            get_risc_instr("L",[i])
            get_risc_instr("j", [f"L{result}"])
        elif op == 'in':
            get_risc_instr("L",[i])
            get_risc_instr("li", ["a7", "5"])
            get_risc_instr("ecall", [])
            storerv("a0",arg1)
        elif op == 'out':
            get_risc_instr("L",[i])
            loadvr(arg1,"a0")
            get_risc_instr("li", ["a7", "1"])
            get_risc_instr("ecall", [])
            get_risc_instr("la", ["a0", "str_nl"])
            get_risc_instr("li", ["a7", "4"])
            get_risc_instr("ecall", [])
        elif op == 'ret':
            get_risc_instr("L",[i])
            loadvr(arg1, "t1")
            get_risc_instr("lw",["t0" , str(-8), "sp"])
            get_risc_instr("sw",["t1" , 0, "t0"])
        elif op == 'par':
            get_risc_instr("L",[i])
            index_par+=1
            if index_par == 1:
                get_risc_instr("addi", ["fp", "sp", str(sym_table.find_entry(result).frameLength)])
                gen_par_final_code(quad_obj.quads[i], index_par)
            else:
                gen_par_final_code(quad_obj.quads[i], index_par)
        elif op == 'call':
            item = sym_table.find_entry(arg1)
            get_risc_instr("L",[i])
            if index_par == 0:
                get_risc_instr("addi", ["fp", "sp", str(sym_table.find_entry(arg1).frameLength)])
            if sym_table.get_nesting_level() != sym_table.find_entry_level(arg1):
                get_risc_instr("lw",["t0" , str(-4), "sp"]) # aderfos
                get_risc_instr("sw",["t0" , str(-4), "fp"])  
            else:
                get_risc_instr("sw",["sp" , str(-4), "fp"]) #goneas
            get_risc_instr("addi", ["sp", "sp", str(sym_table.find_entry(arg1).frameLength)])
            get_risc_instr("jal", [f"L{str(sym_table.find_entry(arg1).startingQuad)}"])
            get_risc_instr("addi", ["sp", "sp", str(-sym_table.find_entry(arg1).frameLength)])
                
            index_par = 0
        elif op == 'begin_block' and arg1 == prog_name:
            get_risc_instr("L",[i])
            get_risc_instr("L",["main"])
            get_risc_instr("addi", ["sp", "sp", str(framelength_main)])
            get_risc_instr("mv", ["gp", "sp"])
        elif op == 'begin_block':
            get_risc_instr("L",[i])
            get_risc_instr("sw",["ra" , 0, "sp"])
        elif op == 'end_block' and arg1 != prog_name:
            get_risc_instr("L",[i])
            get_risc_instr("lw",["ra" , 0, "sp"])
            get_risc_instr("jr",["ra"])
        elif op == 'halt':
            get_risc_instr("L",[i])
            get_risc_instr("li", ["a0", "0"])
            get_risc_instr("li", ["a7", "93"])
            get_risc_instr("ecall", [])
        elif op == 'label':
            with open("output.asm", "a") as f:
                f.write(f"L{result}:\n")
        else:
            get_risc_instr("L",[i])
            #print(f"Warning: Άγνωστη τετράδα: {quad_obj.quads[i]}")

    return end_index  # returns next intermidiate code line

def gen_par_final_code(quad, i):
    op, arg1, arg2, result = quad
    if arg2 == 'cv':
        loadvr(arg1, "t0")
        d = 12 + (i-1) * 4
        get_risc_instr("sw",["t0", str(-d), "fp"])
    elif arg2 == 'ret':
        get_risc_instr("addi", ["t0", "sp", str(-sym_table.find_entry(arg1).offset)])
        get_risc_instr("sw",["t0", str(-8), "fp"])
    elif arg2 == 'ref':
        d = 12 + (i-1) * 4
        item=sym_table.find_entry(arg1)
        if (is_local(arg1) and is_variable(item) or is_temp_var(item) or is_cv_par(item)):
            get_risc_instr("addi", ["t0", "sp", str(-item.offset)])
            get_risc_instr("sw",["t0", str(-d), "fp"])
        elif ((is_local(arg1) and is_variable(item)) or is_cv_par(item)) and belongs_ancestor(arg1):
            gnlvcode(arg1)
            get_risc_instr("sw",["t0", str(-d), "fp"])
        elif is_global(arg1):
            get_risc_instr("addi", ["t0", "gp", str(-item.offset)])
            get_risc_instr("sw",["t0", str(-d), "gp"])
        elif is_ref_par(item):
            get_risc_instr("lw",["t0", str(-item.offset), "sp"])
            get_risc_instr("sw",["t0", str(-d), "fp"])
        elif is_ref_par(item) and belongs_ancestor(arg1):
            gnlvcode(arg1)
            get_risc_instr("lw",["t0", 0, "t0"])
            get_risc_instr("sw",["t0", str(-d), "fp"])



# End of Final Code Generation Helper Functions
#====================================================
# MAIN

def main():
    global file, token, quad, name_endiamesos, name_symtable, name_telikos, last_emitted_index
    if len(sys.argv) < 2:
        print("Usage: python greek_5252_5321.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not input_file.endswith(".gr"):
        print(f"Error: The input must be a .gr file.")
        sys.exit(1) 

    try:
        with open(input_file, "r", encoding="utf-8", errors="replace") as infile:
            name_endiamesos = os.path.splitext(input_file)[0] + ".int"
            name_symtable = os.path.splitext(input_file)[0] + ".sym"
            name_telikos = os.path.splitext(input_file)[0] + ".asm"
            last_emitted_index = 0  # deixnei thn teleutaia tetrada pou metafrastike
            make_final_code_file()
            file = infile
            quad=Quad()
            syntax_analyzer()
            
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()