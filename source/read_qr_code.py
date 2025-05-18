import json
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
from pyzbar.pyzbar import decode


def read_qr_code_from_bytes(image_bytes: bytes):
    """
    Принимает последовательность байт изображения,
    возвращает расшифрованный JSON с QR-кода (или None).
    """
    try:
        img = Image.open(BytesIO(image_bytes)).convert("L")

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)

        img = img.filter(ImageFilter.SHARPEN)

        img = img.point(lambda p: 255 if p > 128 else 0)

        decoded_objects = decode(img)

        if not decoded_objects:
            return None

        qr_data = decoded_objects[0].data.decode('utf-8')

        try:
            qr_data_json = json.loads(qr_data)
            #print(f"Декодированные данные: {qr_data_json}")
            return qr_data_json
        except json.JSONDecodeError:
            return None

    except FileNotFoundError:
        return None
    except Exception as e:
        return None
