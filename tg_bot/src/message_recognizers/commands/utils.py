def prepare_light_name(name: str) -> str:
    lampochka = "лампочка"
    if name.startswith(lampochka):
        name = name[len(lampochka) :]

    name = name.strip().lower()
    return name
