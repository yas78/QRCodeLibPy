class Module:
    @classmethod
    def get_num_modules_per_side(cls, version: int) -> int:
        return 17 + 4 * version
