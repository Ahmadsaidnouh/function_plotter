import numpy as np
import matplotlib.pyplot as plt
from PySide2.QtWidgets import QMessageBox
import re


# the main function
def plot_handler(func, min_x, max_x):
    plt.close()
    if not valid_inputs(func, min_x, max_x):
        return
    min_x = int(min_x)
    max_x = int(max_x)
    x_list = np.linspace(min_x, max_x, num=(max_x - min_x) * 100)

    while func[0] == ' ':
        func = func.replace(" ", "", 1)
    func = func[::-1]

    while func[0] == ' ':
        func = func.replace(" ", "", 1)

    func = func[::-1]

    try:
        postfix_stack = infix_to_postfix(func + ' ', x_list)
        if type(postfix_stack) is list:
            y_list = evaluate_postfix(postfix_stack)
            plot(x_list, y_list, func)
    except Exception as e:
        display_error_message("Syntax Error: " + func + " is an invalid function.")


# parses then evaluates then transforms from infix to postfix.
def infix_to_postfix(func, x_list):
    postfix_stack = []
    operator_stack = [' ']
    single_func = ''
    func_count = 0
    operation_count = 0
    for i in range(0, len(func)):
        ch = func[i]
        if i > 0 and i < len(func) - 2:
            operator = func[i - 1:i + 2]
        else:
            operator = ''
        if ch == ' ' and i != 0 and single_func != '' and single_func != ' ':
            single_func = single_func.replace(" ", "")
            single_func = validate_evaluate_single_func(single_func, x_list)
            if type(single_func) is np.ndarray:
                postfix_stack.append(single_func)
                single_func = ''
                func_count += 1
            else:
                return "Error"
        elif operator == ' + ' or operator == ' - ' or operator == ' * ' or operator == ' / ':
            if less_precedence(func[i], operator_stack[-1]):
                while (len(operator_stack) > 0) and (operator_stack[-1] != ' '):
                    postfix_stack.append(operator_stack.pop())
            operator_stack.append(func[i])
            operation_count += 1
        elif operator == ' ^ ':
            display_error_message("Syntax Error: ^ operator is not allowed between single functions.")
            return "Error"
        else:
            if ch != ' ':
                single_func = single_func + ch

    while len(operator_stack) > 0:
        if operator_stack[-1] == ' ' or operator_stack[-1] == '':
            operator_stack.pop()
            continue
        postfix_stack.append(operator_stack.pop())
    if operation_count != func_count - 1:
        display_error_message("Syntax Error: " + func + " is an invalid function.")
        return "Error"

    return postfix_stack


# once our function is successfully parsed and transformed from infix to postfix, this function is
# called to evaluate that postfix
def evaluate_postfix(postfix_stack):
    temp_stack = []
    for i in range(len(postfix_stack)):
        item = postfix_stack[i]
        if type(item) is not np.ndarray:
            a = temp_stack.pop()
            b = temp_stack.pop()
            if item == '+':
                result = b + a
            elif item == '-':
                result = b - a
            elif item == '*':
                result = b * a
            elif item == '/':
                result = b / a

            temp_stack.append(result)
        else:
            temp_stack.append(postfix_stack[i])

    return temp_stack[-1]


# it plots the wanted function
def plot(x_list, y_list, title):
    plt.figure(num=0, dpi=120)
    plt.plot(x_list, y_list)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("f(x) = " + title)
    plt.show()


# validates min_x < max_x and that the entered function is not empty.
def valid_inputs(func, min_x, max_x):
    if (func == '') or (min_x >= max_x):
        if func == '':
            message = 'ERROR: Must enter function!!'
        else:
            message = 'ERROR: (minimum x) must be less than (maximum x)'
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText(message)
        msg.exec_()
        return False

    match = re.search("^[0-9xsincota()*/+-.^ ]*$", func)
    if not match:
        display_syntax_error(func)
        return False

    return True


# used to display error message and point at the character that caused syntax error.
def display_syntax_error(func):
    for i in range(0, len(func)):
        sub_string = func[0:i + 1]
        match = re.search("^[0-9xsincota()*/+-.^ ]*$", sub_string)
        if not match:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle('Error')
            if i != len(func) - 1:
                message = 'Syntax Error: ' + sub_string[0:i] + "\u0332".join(
                    sub_string[i].upper() + func[i + 1]) + func[i + 2:len(
                    func)] + " is not a valid character in the function"
            else:
                message = 'Syntax Error: \n' + sub_string[0:i] + "\u0332".join(
                    sub_string[i].upper() + " ") + " is not a valid single function"
            msg.setText(message)
            msg.exec_()
            break


# used to display error messages
def display_error_message(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle('Error')
    msg.setText(message)
    msg.exec_()


# check if the given func is valid or not. If valid, it then evaluates it. If not, then will display
# the appropriate error message
def validate_evaluate_single_func(func, x):
    const1 = 1
    const2 = 1
    if is_number(func):
        return float(func) * x ** 0

    first_ch_match = re.search("[0-9xsct]", func[0])
    last_ch_match = re.search("[0-9x)]", func[len(func) - 1])
    if not first_ch_match or not last_ch_match:
        display_error_message("Syntax Error: " + func + " is an invalid single function.")
        return "Error"

    const_str = ''
    for i in range(0, len(func)):
        ch = func[i]
        if ch == '*' or ch == '^' or ch == 'c' or ch == 's' or ch == 't' or ch == "x":
            if len(const_str) != 0:
                const1 = float(const_str)
                const_str = ''
            for j in range(i, len(func)):
                if func[j] == "x":
                    if j != len(func) - 1 and func[j + 1] == '^':
                        power = func[j + 2:len(func)]
                        if power.isnumeric():
                            return const1 * x ** int(power)
                        else:
                            display_error_message("Syntax Error: " + " Power is not positive integer in " + func)
                            return "Error"
                    elif j == len(func) - 1:
                        return const1 * x
                    else:
                        display_error_message("Syntax Error: ^ is missing in " + func)
                        return "Error"

                elif func[j:j + 3] == 'cos':
                    parenthesis = func[j + 3: len(func)]
                    const2 = evaluate_const2(parenthesis)
                    if const2 == "Error":
                        display_error_message("Syntax Error: invalid parenthesis content in the " + func)
                        return "Error"
                    return const1 * np.cos(const2 * x)
                elif func[j:j + 3] == 'sin':
                    parenthesis = func[j + 3: len(func)]
                    const2 = evaluate_const2(parenthesis)
                    if const2 == "Error":
                        display_error_message("Syntax Error: invalid parenthesis content in the " + func)
                        return "Error"
                    return const1 * np.sin(const2 * x)
                elif func[j:j + 3] == 'tan':
                    parenthesis = func[j + 3: len(func)]
                    const2 = evaluate_const2(parenthesis)
                    if const2 == "Error":
                        display_error_message("Syntax Error: invalid parenthesis content in the " + func)
                        return "Error"
                    return const1 * np.tan(const2 * x)
                elif func[j] == '^':
                    match = re.search("\^x$", func)
                    if not match:
                        display_error_message("Syntax Error: " + func + " is an invalid single function.")
                        return "Error"
                    return float(const1) ** x
        else:
            const_str = const_str + ch


# uses regex to extract the omega in the cos(w*x) || sin(w*x) || tan(w*x) from a given string
def evaluate_const2(func):
    if len(func) < 3:
        return 'Error'

    if len(func) == 3 and func == '(x)':
        return 1

    match = re.search("(^\(-?)([0-9.]*)(\*x\)$)", func)

    if not match:
        return "Error"

    func = func.replace("(", '')
    func = func.replace(")", '')
    func = func.replace("x", '')
    func = func.replace("*", '')
    return float(func)


# returns true if op1 has lower priority than op2, false otherwise
def less_precedence(op1, op2):
    op1_prec = precedence(op1)
    op2_prec = precedence(op2)
    return op1_prec < op2_prec


# assigns a value to each group of operations so that to be known which operation has higher priority
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0


# returns true is the s is float, false otherwise
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
