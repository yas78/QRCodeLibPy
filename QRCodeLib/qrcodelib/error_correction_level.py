class ErrorCorrectionLevel:
    _level = {"L": 0, "M": 1, "Q": 2, "H": 3}

    L = _level["L"]
    M = _level["M"]
    Q = _level["Q"]
    H = _level["H"]

    @classmethod
    def to_int(cls, s: str) -> int:
        return cls._level[s]
