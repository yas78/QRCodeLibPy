class Module(object):
    """
        モジュール
    """
    @classmethod
    def get_num_modules_per_side(cls, version: int) -> int:
        """
            １辺のモジュール数を返します。
        """
        return 17 + version * 4
