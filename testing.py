import numpy as np

stack = np.linspace(0,1,num=10)
# stack = stack.tolist()
# stack.append([1, 2,4])

# stack.append('+')
print(float("-5.6"))
print(np.flip(stack))
# import re
#
# def evaluate(func):
#     if len(func) < 3:
#         return 'Error'
#
#     match = re.search("(^\(-?)([0-9.]*)(\*x\)$)", func)
#
#     if not match:
#         return "Error"
#
#     func = func.replace("(", '')
#     func = func.replace(")", '')
#     func = func.replace("x", '')
#     func = func.replace("*", '')
#
#     return float(func)
#
# print(evaluate("(-.9*x)"))
#
