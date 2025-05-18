import json
import qrcode
from io import BytesIO
from PIL import Image
import cv2
import numpy as np


async def read_qr_code(image_bytes: bytes) -> dict | None:
    """
    Распознаёт QR-код из изображения в байтах и возвращает словарь.
    """
    try:
        # Открываем изображение через PIL
        img = Image.open(BytesIO(image_bytes)).convert("RGB")

        # Переводим в формат, понятный OpenCV
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Распознаём QR-код
        detector = cv2.QRCodeDetector()
        data, points, _ = detector.detectAndDecode(img_cv)

        if not data:
            return None

        return json.loads(data)

    except Exception:
        return None


async def generate_qr_code(tg_id: int, event_id: int) -> bytes:
    """
    Генерирует QR-код с информацией о пользователе и событии.
    Возвращает изображение в виде байтов PNG.
    """
    data = {
        "user": {"tg_id": tg_id},
        "event": {"event_id": event_id}
    }

    data_json = json.dumps(data)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_json)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
