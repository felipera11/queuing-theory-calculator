import ast

import streamlit as st


def _parse_numeric_expression(value_str):
    normalized_value = value_str.replace(",", ".").strip()

    if not normalized_value:
        return None

    try:
        return float(normalized_value)
    except ValueError:
        pass

    try:
        expression = ast.parse(normalized_value, mode="eval")
    except SyntaxError as exc:
        raise ValueError from exc

    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.USub,
        ast.UAdd,
        ast.Constant,
    )

    for node in ast.walk(expression):
        if not isinstance(node, allowed_nodes):
            raise ValueError("Expressão inválida")
        if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
            raise ValueError("Expressão inválida")

    return float(eval(compile(expression, "<input>", "eval"), {"__builtins__": {}}, {}))


def input_rate(label, key_prefix, help_text=None):
    value_str = st.text_input(
        label,
        placeholder="Ex: 10  ou  1/6  (aceita expressões)",
        key=f"{key_prefix}_input",
        help=help_text,
    )

    try:
        parsed_value = _parse_numeric_expression(value_str)
        return parsed_value if parsed_value is not None else 0
    except (ValueError, TypeError):
        st.error(f"Digite um número válido para {label}")
        return 0


def input_lambda(prefix=""):
    return input_rate(
        "λ — Taxa de chegada (clientes/hora)",
        f"{prefix}_lambda",
        help_text="Número médio de clientes que chegam por hora. Aceita frações: ex. 1/6.",
    )


def input_mi(prefix=""):
    return input_rate(
        "μ — Taxa de serviço (clientes/hora)",
        f"{prefix}_mi",
        help_text="Número médio de clientes atendidos por hora por servidor. Aceita frações: ex. 1/4.",
    )


def input_integer(label, key, default=0, placeholder=None, min_value=None, max_value=None, help_text=None):
    value_str = st.text_input(
        label,
        value=str(default),
        placeholder=placeholder or f"Ex: {default}",
        key=key,
        help=help_text,
    )

    try:
        parsed_value = _parse_numeric_expression(value_str)
        value = int(parsed_value) if parsed_value is not None else default
    except ValueError:
        st.error(f"Digite um número inteiro válido para {label}")
        return default

    if min_value is not None and value < min_value:
        st.error(f"{label} deve ser maior ou igual a {min_value}")
        return default

    if max_value is not None and value > max_value:
        st.error(f"{label} deve ser menor ou igual a {max_value}")
        return default

    return value


def input_float_value(label, key, default=0.0, placeholder=None, min_value=None, max_value=None, help_text=None):
    value_str = st.text_input(
        label,
        value="" if default is None else str(default),
        placeholder=placeholder or f"Ex: {default}",
        key=key,
        help=help_text,
    )

    if not value_str:
        return default

    try:
        parsed_value = _parse_numeric_expression(value_str)
        value = float(parsed_value)
    except ValueError:
        st.error(f"Digite um número válido para {label}")
        return default

    if min_value is not None and value < min_value:
        st.error(f"{label} deve ser maior ou igual a {min_value}")
        return default

    if max_value is not None and value > max_value:
        st.error(f"{label} deve ser menor ou igual a {max_value}")
        return default

    return value
