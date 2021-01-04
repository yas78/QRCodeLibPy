class Constants:
    MIN_VERSION = 1
    MAX_VERSION = 40


class Values:
    BLANK = 0
    WORD = 1
    ALIGNMENT = 2
    FINDER = 3
    FORMAT = 4
    SEPARATOR = 5
    TIMING = 6
    VERSION = 7

    @classmethod
    def is_dark(cls, value: int) -> int:
        return value > cls.BLANK
