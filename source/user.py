import qrcode
import json
import os
from source.working_classes import Event, Activity
import json
import qrcode
from io import BytesIO

class UserClass:
    def __init__(self, user_id: int = None,
                 tg_id: int = None,
                 username: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 phone: str = None,
                 is_admin: bool = False):
        self.user_id = user_id
        self.tg_id = tg_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone
        self.is_admin = is_admin

    import json
    import qrcode
    from io import BytesIO


