from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal, TYPE_CHECKING
import uuid
from datetime import datetime

# Используем TYPE_CHECKING для избежания циклических импортов при аннотации
if TYPE_CHECKING:
    from __main__ import Event


@dataclass
class Activity:
    _name: str = field(init=True)
    _location: Optional[str] = field(init=True)
    _start_time: datetime = field(init=True)
    _end_time: datetime = field(init=True)
    _link: Optional[str] = field(init=True)
    _event: 'Event' = field(init=True)
    _attendees: Dict[int, bool] = field(default_factory=dict)
    _id: str = field(init=True, default=None)

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        try:
            uuid.UUID(value)
            self._id = value
        except ValueError:
            raise ValueError("ID должен быть валидным UUID")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Имя не может быть пустым")
        self._name = value

    @property
    def location(self) -> Optional[str]:
        return self._location

    @location.setter
    def location(self, value: Optional[str]) -> None:
        self._location = value

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @start_time.setter
    def datetime(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise ValueError("Дата и время должны быть объектом datetime")
        self._start_time = value

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @end_time.setter
    def datetime(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise ValueError("Дата и время должны быть объектом datetime")
        self._end_time = value

    @property
    def link(self) -> Optional[str]:
        return self._link

    @link.setter
    def link(self, value: Optional[str]) -> None:
        self._link = value

    @property
    def event(self) -> 'Event':
        return self._event

    @event.setter
    def event(self, value: 'Event') -> None:
        if not isinstance(value, Event):
            raise ValueError("Event должен быть объектом класса Event")
        self._event = value

    @property
    def attendees(self) -> Dict[int, bool]:
        return self._attendees

    @attendees.setter
    def attendees(self, value: Dict[int, bool]) -> None:
        if not isinstance(value, dict):
            raise ValueError("Attendees должен быть словарем")
        self._attendees = value

    def register_user(self, user_id: int) -> None:
        self._attendees[user_id] = False

    def mark_attended(self, user_id: int) -> None:
        if user_id in self._attendees:
            self._attendees[user_id] = True

    def is_attended(self, user_id: int) -> bool:
        return self._attendees.get(user_id, False)


@dataclass
class Event:
    _title: str = field(init=True)
    _description: str = field(init=True)
    _start_time: datetime = field(init=True)
    _end_time: datetime = field(init=True)
    _link: Optional[str] = field(init=True)
    _location: str = field(init=True)
    _status: Literal["offline", "online"] = field(init=True)
    _vacant_places: int = field(init=True)
    _activities: List[Activity] = field(default_factory=list)
    _id: str = field(init=True, default=None)

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        try:
            uuid.UUID(value)
            self._id = value
        except ValueError:
            raise ValueError("ID должен быть валидным UUID")

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Заголовок не может быть пустым")
        self._title = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Описание не может быть пустым")
        self._description = value

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @start_time.setter
    def start_time(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise ValueError("Время начала должно быть объектом datetime")
        if hasattr(self, '_end_time') and value > self._end_time:
            raise ValueError("Время начала не может быть позже времени окончания")
        self._start_time = value

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @end_time.setter
    def end_time(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise ValueError("Время окончания должно быть объектом datetime")
        if value < self._start_time:
            raise ValueError("Время окончания не может быть раньше времени начала")
        self._end_time = value

    @property
    def link(self) -> Optional[str]:
        return self._link

    @link.setter
    def link(self, value: Optional[str]) -> None:
        self._link = value

    @property
    def status(self) -> Literal["offline", "online"]:
        return self._status

    @status.setter
    def status(self, value: Literal["offline", "online"]) -> None:
        if value not in ["offline", "online"]:
            raise ValueError("Статус должен быть 'offline' или 'online'")
        self._status = value

    @property
    def activities(self) -> List[Activity]:
        return self._activities

    @activities.setter
    def activities(self, value: List[Activity]) -> None:
        if not isinstance(value, list):
            raise ValueError("Activities должен быть списком")
        self._activities = value

    def add_activity(self, name: str, location: Optional[str], link: Optional[str], start_time: datetime, end_time: datetime) -> Activity:
        if not (self._start_time <= start_time <= self._end_time and self._start_time <= end_time <= self._end_time):
            raise ValueError("Дата и время активности должны быть в пределах времени события")
        activity = Activity(
            _id=str(uuid.uuid4()),
            _name=name,
            _location=location,
            _link=link,
            _start_time=start_time,
            _end_time=end_time,
            _event=self
        )
        self._activities.append(activity)
        return activity

    def get_activity(self, activity_id: str) -> Optional[Activity]:
        for activity in self._activities:
            if activity.id == activity_id:
                return activity
        return None