from .mode_indicator import ModeIndicator
from .symbol_sequence_indicator import SymbolSequenceIndicator


class StructuredAppend:
    PARITY_DATA_LENGTH = 8

    HEADER_LENGTH = (
        ModeIndicator.LENGTH
        + SymbolSequenceIndicator.POSITION_LENGTH
        + SymbolSequenceIndicator.NUM_SYMBOLS_LENGTH
        + PARITY_DATA_LENGTH
    )
