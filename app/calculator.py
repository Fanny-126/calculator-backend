import ast
import operator


class CalculatorError(Exception):
    """Custom exception for calculator errors."""


class SafeCalculator:
    """Safe mathematical expression calculator."""

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def calculate(self, expression: str) -> float:
        """
        Calculate a mathematical expression.

        Supported:
        - Addition
        - Subtraction
        - Multiplication
        - Division
        - Decimal numbers
        - Parentheses
        - Operator precedence
        - Unary plus and minus
        """

        if not isinstance(expression, str):
            raise CalculatorError("Expression must be a string.")

        expression = expression.strip()

        if not expression:
            raise CalculatorError("Expression cannot be empty.")

        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError:
            raise CalculatorError("Invalid expression.")

        try:
            result = self._evaluate(tree.body)
        except CalculatorError:
            raise
        except ZeroDivisionError:
            raise CalculatorError("Cannot divide by zero.")
        except (ValueError, TypeError, OverflowError):
            raise CalculatorError("Failed to calculate the expression.")

        return result

    def _evaluate(self, node):
        """Evaluate a validated AST node."""

        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                raise CalculatorError("Boolean values are not supported.")

            if isinstance(node.value, (int, float)):
                return node.value

            raise CalculatorError("Only numeric values are supported.")

        if isinstance(node, ast.BinOp):
            operator_function = self.OPERATORS.get(type(node.op))

            if operator_function is None:
                raise CalculatorError("Unsupported operator.")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            try:
                return operator_function(left, right)
            except ZeroDivisionError:
                raise CalculatorError("Cannot divide by zero.")

        if isinstance(node, ast.UnaryOp):
            operator_function = self.OPERATORS.get(type(node.op))

            if operator_function is None:
                raise CalculatorError("Unsupported unary operator.")

            operand = self._evaluate(node.operand)
            return operator_function(operand)

        raise CalculatorError("Expression contains unsupported content.")


def calculate_expression(expression: str) -> float:
    """Calculate an expression using the safe calculator."""
    calculator = SafeCalculator()
    return calculator.calculate(expression)