

def extract_text_after_command(text: str, key: str) -> str | None:
    pos = text.find(key)
    if pos == -1:
        return None

    pos = pos + len(key) + 1

    filtered_text = text[pos:]

    return filtered_text