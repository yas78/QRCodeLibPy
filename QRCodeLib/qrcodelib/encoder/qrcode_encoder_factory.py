from ..encoding_mode import EncodingMode
from .alphanumeric_encoder import AlphanumericEncoder
from .byte_encoder import ByteEncoder
from .kanji_encoder import KanjiEncoder
from .numeric_encoder import NumericEncoder
from .qrcode_encoder import QRCodeEncoder


class QRCodeEncoderFactory:

    @classmethod
    def create_encoder(cls,  enc_mode: int, byte_mode_encoding: str) -> QRCodeEncoder:
        if enc_mode == EncodingMode.NUMERIC:
            return NumericEncoder()

        if enc_mode == EncodingMode.ALPHA_NUMERIC:
            return AlphanumericEncoder()

        if enc_mode == EncodingMode.EIGHT_BIT_BYTE:
            return ByteEncoder(byte_mode_encoding)

        if enc_mode == EncodingMode.KANJI:
            return KanjiEncoder()
        
        raise ValueError("enc_mode")
