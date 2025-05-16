from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, Text, DateTime, Integer, LargeBinary, \
    ForeignKey, Boolean
import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None] = mapped_column(String(50))
    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    phone_number: Mapped[str | None] = mapped_column(String(100))
    is_admin: Mapped[bool] = mapped_column(Boolean)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    datetime: Mapped[datetime | None] = mapped_column(
        DateTime(), default=datetime.datetime.now)
    vacant_places: Mapped[int] = mapped_column(Integer)
    address: Mapped[str | None] = mapped_column(String(100))
    map_photo: Mapped[bytes | None] = mapped_column(LargeBinary)


class UserEventConnect(Base):
    __tablename__ = "user_event_connect"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True)
    event_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("events.id", ondelete="CASCADE"),
        primary_key=True)
    date_of_registration: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.datetime.now)
    qr_code: Mapped[bytes | None] = mapped_column(LargeBinary)


class EventWaitingList(Base):
    __tablename__ = "event_waiting_list"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True)
    event_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("events.id", ondelete="CASCADE"),
        primary_key=True)

    date_of_registration: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.datetime.now)


class MasterClass(Base):
    __tablename__ = "master_class"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    event_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    datetime: Mapped[datetime | None] = mapped_column(DateTime())
    vacant_places: Mapped[int] = mapped_column(Integer)
    map_photo: Mapped[bytes | None] = mapped_column(LargeBinary)


class UserMasterclassConnect(Base):
    __tablename__ = "user_masterclass_connect"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True)
    master_class_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("master_class.id", ondelete="CASCADE"),
        primary_key=True)
    date_of_registration: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.datetime.now)
    qr_code: Mapped[bytes | None] = mapped_column(LargeBinary)


class MasterClassWaitingList(Base):
    __tablename__ = "master_class_waiting_list"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True)
    master_class_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("master_class.id", ondelete="CASCADE"),
        primary_key=True)

    date_of_registration: Mapped[datetime] = mapped_column(DateTime())





