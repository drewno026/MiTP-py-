class CalculatorLogic:
    def __init__(self):
        self.current_system = 10
        self.previous_system = 10

    def evaluate_expression(self, expression):
        try:
            if self.current_system in [2, 16]:
                expression = self.convert_expression(expression)

            expression = expression.replace("√", "**0.5").replace("^", "**")
            result = eval(expression, {"__builtins__": None}, {})

            if self.current_system in [2, 16]:
                return self.convert_number(str(result), 10, self.current_system)
            else:
                return str(result)
        except ZeroDivisionError:
            raise ValueError("You cannot divide by zero")
        except Exception:
            raise ValueError("Invalid expression")

    def convert_expression(self, expression):
        result = ""
        number = ""

        for char in expression:
            if char.isalnum():
                number += char
            else:
                if number:
                    try:
                        result += str(int(number, self.current_system))
                    except ValueError:
                        raise ValueError(f"Incorrect number '{number}' in {self.current_system} system.")
                    number = ""
                result += char
        if number:
            try:
                result += str(int(number, self.current_system))
            except ValueError:
                raise ValueError(f"Incorrect number '{number}' in {self.current_system} system.")
        return result

    def convert_number(self, number, from_base, to_base):
        if not number.strip():
            return ""
        try:
            print(number)
            decimal_value = int(number, from_base)
            match to_base:
                case 2:
                    return bin(decimal_value)[2:]
                case 16:
                    return hex(decimal_value)[2:].upper()
                case 10:
                    return str(decimal_value)
        except ValueError:
            raise ValueError("Incorrect number in this system")
