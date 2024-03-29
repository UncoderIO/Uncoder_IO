class CustomEnumMeta(type):
    def __new__(cls, name: str, bases: tuple, attrs: dict):
        _attrs, _enum = {}, {}
        for base in bases:
            if isinstance(base, cls):
                _enum.update(getattr(base, "_enum", {}))

        for key, value in attrs.items():
            if key[:2] == key[-2:] == "__" or hasattr(value, "__get__"):
                _attrs[key] = value
            else:
                _enum[key] = value

        _attrs["_enum"] = _enum

        return super().__new__(cls, name, bases, _attrs)

    def __contains__(cls, name: str):
        return name in cls._enum.values()

    def __getattr__(cls, name: str):
        try:
            return cls._enum[name]
        except KeyError as e:
            raise AttributeError(name) from e


class CustomEnum(metaclass=CustomEnumMeta):
    pass
