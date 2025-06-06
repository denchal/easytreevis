def is_string_convertible(x) -> bool:
    try:
        str(x)
        return True
    except Exception:
        return False