# rpn.py
# Zachary Moore
# CSCI 111, Fall 2022
# Evaluates expressions in text file using reverse polish notation

# Bonus addition: Added capability of using/storing variables and defining variables in terms of other variables

import math, string

The_Stack = []
store = dict()  # user-defined variable storage

def parse_integer(number):

    list_num = list(number)
    
    sign = 1
    accumulator = 0

    if '+' in number:
        list_num.remove('+')

    elif '-' in number:
        list_num.remove('-')
        sign = -1

    for d in list_num:
        accumulator = accumulator * 10 + (ord(d) - ord('0'))

    return (sign * accumulator)


def parse_float(number):

    exponent = 0
    num = number


    if 'e' in number:
        
        split_e = number.split('e')
        
        exponent = parse_integer(split_e[1])
        
        
        num = split_e[0]


    if '.' in num:

        split_decimal = num.split('.')

        whole = parse_integer(split_decimal[0])

        n = len(split_decimal[1])

        fraction = parse_integer(split_decimal[1])

        fraction = fraction / (10**n)

        if whole < 0:
            fraction = fraction * -1.

    if '.' not in num:
        whole = parse_integer(num)
        fraction = 0.0

    return ((whole + fraction) * (10 ** exponent))


def parse_number(number):

    if 'e' in number:
        num = parse_float(number)
        
    elif '.' in number:
        num = parse_float(number)
        
    else:
        num = parse_integer(number)

    return(num)


def is_keyword(word):
    keyword_list = ['pop','clr','+','-','*','/','**','sin','cos','sqrt','def']

    return word in keyword_list


def tokenize(statement):
    token_list = list(statement.split())

    if 'def' in token_list:
        for i in range(len(token_list)):
            if not is_keyword(token_list[i]) and token_list[i] not in store and ( i != len(token_list)-2 ):  # allows any variable name
                token_list[i] = parse_number(token_list[i]) 
    
    else:
        for i in range(len(token_list)):
            if not is_keyword(token_list[i]) and token_list[i] not in store:
                token_list[i] = parse_number(token_list[i])               
                
    return (token_list)


def rpnline(line,stack):

    global store

    input_list = tokenize(line)
      
    for i in range(len(input_list)):

        print('Stack:',stack,'Tokens:',input_list[i:])
        
        if not is_keyword(input_list[i]):
            stack.append(input_list[i])
 
        else:

            # Handling Variables
         
            if stack[len(stack)-1] in store:   # converts any stored variables to their numerical values prior to calculations
                stack[len(stack)-1] = store[stack[len(stack)-1]]
                    
            if len(stack) >= 2:
                if stack[len(stack)-2] in store:
                    stack[len(stack)-2] = store[stack[len(stack)-2]]

            # Handling Keywords
                
            if input_list[i] == '+':
                add_operand1 = stack.pop(len(stack)-1)
                add_operand2 = stack.pop(len(stack)-1)
                add_result = add_operand1 + add_operand2
                stack.append(add_result)
                
            elif input_list[i] == '*':
                mult_operand1 = stack.pop(len(stack)-1)
                mult_operand2 = stack.pop(len(stack)-1)
                mult_result = mult_operand1 * mult_operand2
                stack.append(mult_result)

            elif input_list[i] == '-':
                sub_operand1 = stack.pop(len(stack)-2)
                sub_operand2 = stack.pop(len(stack)-1)
                sub_result = sub_operand1 - sub_operand2
                stack.append(sub_result)

            elif input_list[i] == '/':
                div_operand1 = stack.pop(len(stack)-2)
                div_operand2 = stack.pop(len(stack)-1)
                div_result = div_operand1 / div_operand2
                stack.append(div_result)

            elif input_list[i] == 'sin':
                sin_operand = stack.pop(len(stack)-1)
                sin_result = math.sin(sin_operand)
                stack.append(sin_result)

            elif input_list[i] == 'cos':
                cos_operand = stack.pop(len(stack)-1)
                cos_result = math.cos(cos_operand)
                stack.append(cos_result)

            elif input_list[i] == 'sqrt':
                sqrt_operand = stack.pop(len(stack)-1)
                sqrt_result = math.sqrt(sqrt_operand)
                stack.append(sqrt_result)

            elif input_list[i] == '**':
                exp_operand1 = stack.pop(len(stack)-2)
                exp_operand2 = stack.pop(len(stack)-1)
                exp_result = exp_operand1 ** exp_operand2
                stack.append(exp_result)

            elif input_list[i] == 'clr':
                del stack[:]

            elif input_list[i] == 'pop':
                del stack[len(stack)-1]

            elif input_list[i] == 'def':  # stores variables
                key = stack.pop(len(stack)-1)
                value = stack.pop(len(stack)-1)
                store[key] = value

    print(stack)


def repl(stack):
    
    while True:
        line = input('RPN >>> ')
        if line == 'exit':
            break
        rpnline(line,stack)


def runfile(fname,stack):
    fin = open(fname)
    for line in fin:
        line = line.strip()
        if line == 'exit':
            break
        print('INPUT:',line)
        rpnline(line,stack)

repl(The_Stack)

#runfile('numfile.txt',The_Stack)

