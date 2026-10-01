import ast

def parse_params(items: list[str]) -> dict[str, str]:
    """Превращает ['count=5', 'sort=true'] в {'count': '5', 'sort': 'true'}."""
    params: dict[str, str] = {}
    for item in items:
        key, sep, value = item.partition("=")   # делит по ПЕРВОМУ "="
        key = key.strip()
        if not sep or not key:
            raise ValueError(f"expected key=value, got {item!r}")
        if key in params:
            raise ValueError(f"duplicate parameter: {key}")
        params[key] = value
    return params


def parse_bool(raw: str) -> bool:
    """Превращает 'true'/'false' (и похожие варианты) в bool."""
    value = raw.strip().lower()
    if value in {"1", "true", "yes", "y", "on"}:
        return True
    if value in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError(f"expected true/false, got {raw!r}")

def parse_optional(raw: str, conv):
    """'None' или пустая строка -> None, иначе conv(raw)."""
    return None if raw.strip() in ("", "None") else conv(raw)

def parse_marks(raw: str) -> list[int | None]:
    """Превращает '[10, None, 8]' в [10, None, 8]."""
    try:
        value = ast.literal_eval(raw.strip())
    except (ValueError, SyntaxError):
        raise ValueError(f"marks: cannot parse {raw!r}, expected a list like [10, None, 8]")

    if not isinstance(value, (list, tuple)):
        raise ValueError(f"marks must be a list, got {type(value).__name__}")

    for m in value:
        if m is not None and (isinstance(m, bool) or not isinstance(m, int)):
            raise ValueError(f"marks must contain integers or None, got {m!r}")

    return list(value)
