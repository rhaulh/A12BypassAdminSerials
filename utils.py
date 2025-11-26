def validate (serial: str) -> bool:
    if not serial:
        return False
    return 5 <= len(serial) <= 40
