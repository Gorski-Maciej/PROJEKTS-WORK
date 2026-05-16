from __future__ import annotations

import ast
import operator
from typing import Any

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_CMP_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
}


def evaluate_condition(condition: str, context: dict[str, Any]) -> bool:
    if not condition:
        return True

    tree = ast.parse(condition, mode='eval')

    def ev(node: ast.AST) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return context.get(node.id)
        if isinstance(node, ast.UnaryOp):
            val = ev(node.operand)
            if isinstance(node.op, ast.Not):
                return not val
            if isinstance(node.op, ast.USub):
                return -val
        if isinstance(node, ast.BinOp):
            return _BIN_OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.Compare):
            left = ev(node.left)
            for op, right_node in zip(node.ops, node.comparators):
                right = ev(right_node)
                if not _CMP_OPS[type(op)](left, right):
                    return False
                left = right
            return True
        if isinstance(node, ast.BoolOp):
            values = [ev(v) for v in node.values]
            if isinstance(node.op, ast.And):
                return all(values)
            if isinstance(node.op, ast.Or):
                return any(values)
        raise ValueError(f'Unsupported expression: {type(node).__name__}')

    try:
        return bool(ev(tree.body))
    except Exception:
        return False
