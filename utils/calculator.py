import ast
import operator as op

# 支持的运算符
SAFE_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def safe_eval(expr: str) -> float:
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return SAFE_OPERATORS[type(node.op)](
                _eval(node.left), _eval(node.right)
            )
        elif isinstance(node, ast.UnaryOp):
            return SAFE_OPERATORS[type(node.op)](_eval(node.operand))
        else:
            raise TypeError("不支持的表达式")

    node = ast.parse(expr, mode="eval").body
    return _eval(node)


def calculator(expr: str) -> str:
    expr = expr.replace("计算", "").replace("^", "**").strip()

    try:
        result = safe_eval(expr)
        return str(result)
    except Exception:
        return "计算失败，请检查表达式"
