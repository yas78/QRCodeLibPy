class Charset(object):
    SHIFT_JIS = "Shift_JIS"
    GB2312 = "GB2312"
    EUC_KR = "EUC-KR"
    UTF_8 = "UTF-8"

    _cjK_charset_names = [SHIFT_JIS, GB2312, EUC_KR]

    def __init__(self):
        pass

    @classmethod
    def is_jp(cls, charset_name: str) -> bool:
        return charset_name.lower() == cls.SHIFT_JIS.lower()

    @classmethod
    def is_cjk(cls, charset_name: str) -> bool:
        if not charset_name:
            raise ValueError("charset_name")

        for name in map(lambda x: x.lower(), cls._cjK_charset_names):
            if charset_name.lower() == name:
                return True

        return False
