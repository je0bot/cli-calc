# cli calculator 

import re

operations = {  # operations are managed here
    '+': lambda a, b: (a + b, None),
    '-': lambda a, b: (a - b, None),
    '*': lambda a, b: (a * b, None),
    '/': lambda a, b: (None, "Error: Division by zero") if b == 0 else (a / b, None),
}

history = []    # to maintain history


def calculate(expression_str):
   
    expression_str = re.sub(r'\s*([+\-*/])\s*', r' \1 ', expression_str).strip()    # this will help us the match the spacing in input given bt userr
    tokens = expression_str.split()     # it'll store the numbers and operators

    try:  
        numbers = []
        operators = []
        for i, token in enumerate(tokens):
            if i % 2 == 0:  
                numbers.append(float(token))
            else:           
                if token not in operations:
                    return None, f"Unknown operator '{token}'"
                operators.append(token)
    except ValueError:
        return None, "Invalid number in expression"

    if not numbers:
        return None, "Empty expression"
    if len(numbers) != len(operators) + 1:
        return None, "Wrong format. Example: 5 + 3 * 2"

    i = 0
    while i < len(operators):
        if operators[i] in ('*', '/'):
            value, error = operations[operators[i]](numbers[i], numbers[i + 1])
            if error:
                return None, error
            numbers[i:i + 2] = [value]   
            operators.pop(i)             
        else:
            i += 1

    
    result = numbers[0]
    for i, op in enumerate(operators):
        value, error = operations[op](result, numbers[i + 1])
        if error:
            return None, error
        result = value

    return result, None


def show_history():
    if not history:
        print("No history yet.")
    else:
        print("\n--- History ---")
        for i, entry in enumerate(history, 1):
            print(f"  {i}. {entry}")
        print("---------------\n")


print("Commands: 'history', 'clear', 'exit'")
print("Supports: 5 + 3 * 2  or  5+3*2\n")

while True:
    try:
        user_input = input(">>> ").strip()

        if not user_input:
            continue

       
        if user_input.lower() == 'exit':
            print("Bye!")
            break

        if user_input.lower() == 'history':
            show_history()
            continue

        if user_input.lower() == 'clear':
            history.clear()        
            print("History cleared.")
            continue

        result, error = calculate(user_input)

        if error:
            print(f"Error: {error}")
        else:
            display = int(result) if result == int(result) else round(result, 6)
            output = f"{user_input} = {display}"
            print(f"Result: {display}")
            history.append(output)

    except Exception as e:
        print(f"Something went wrong: {e}")