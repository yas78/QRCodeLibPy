from EncodingMode import EncodingMode
from encoder.AlphanumericEncoder import AlphanumericEncoder
from encoder.ByteEncoder import ByteEncoder
from encoder.KanjiEncoder import KanjiEncoder
from encoder.NumericEncoder import NumericEncoder
from encoder.QRCodeEncoder import QRCodeEncoder


class QRCodeEncoderFactory(object):

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
