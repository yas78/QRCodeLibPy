from .ModeIndicator import ModeIndicator
from .SymbolSequenceIndicator import SymbolSequenceIndicator


class StructuredAppend(object):
    """
        構造的連接
    """
    # パリティデータのビット数
    PARITY_DATA_LENGTH = 8

    # 構造的連接ヘッダーのビット数
    HEADER_LENGTH = (
        ModeIndicator.LENGTH
        + SymbolSequenceIndicator.POSITION_LENGTH
        + SymbolSequenceIndicator.TOTAL_NUMBER_LENGTH
        + PARITY_DATA_LENGTH
    )
