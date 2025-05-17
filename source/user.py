import qrcode
import json
import os
from working_classes import Event, Activity

class UserClass:
    def __init__(self, user_id: int = None,
                 tg_id: int = None,
                 username: str = None,
                 first_name: str = None, last_name: str = None,
                 phone: str = None,
                 is_admin: bool = False):
        self.user_id = user_id
        self.tg_id = tg_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone
        self.is_admin = is_admin

    def generate_qr_code(self, event: Event | Activity, filename="qrcode.png"):
        data = {
            "user": {
                "user_id": self.user_id,
                "name": self.username,
                "email": self.phone_number
            },
            "event": {
                "event_id": event.id,
                "event_type": "Event" if event is Event else "Activity",
                "event_name": event.name if event is Activity else event.title
            }
        }

        data_str = json.dumps(data)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_str)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        return os.path.abspath(filename)
