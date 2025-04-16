"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 30/01/2025
"""
from datetime import datetime, timezone, timedelta
from typing import Optional

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar

from ibtrading.settings import Settings

WEEKDAY2NUM = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}


def datetime_encoder(dt: datetime) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()  # Returns ISO 8601 formatted datetime


def datetime_from_str(dt_str: str, tz=None) -> Optional[datetime]:
    if not dt_str:
        return None
    dt = datetime.fromisoformat(dt_str)  # Parses ISO 8601 formatted datetime
    if tz:
        dt = dt.replace(tzinfo=tz)
    return dt


def convert_to_default_tz(dt: datetime) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(Settings.TIMEZONE)


def replace_tz(dt: datetime, tz=None) -> datetime:
    if tz is None:
        tz = Settings.TIMEZONE
    return dt.replace(tzinfo=tz)


def current_time() -> datetime:
    return datetime.now(tz=Settings.TIMEZONE)


def _next_weekday(reference_date: datetime, target_weekday: int, offset_days: int = 0) -> datetime:
    """
    Get the next given weekday after an optional offset.

    :param reference_date: The reference datetime object.
    :param target_weekday: The target weekday (Monday=0, ..., Sunday=6).
    :param offset_days: Number of days to offset from the reference date before finding the next target weekday.
    :return: Datetime object representing the next occurrence of the target weekday.
    """
    future_date = reference_date + timedelta(days=offset_days)  # Apply offset
    days_ahead = (target_weekday - future_date.weekday()) % 7  # Find next target weekday
    days_ahead = 7 if days_ahead == 0 else days_ahead  # Ensure it's the next occurrence, not the same day
    return future_date + timedelta(days=days_ahead)


def next_weekday(reference_date: datetime = None, target_weekday: str = None, offset_days: int = 0,
                 target_day_label: str = None, tz=None) -> datetime:
    """
    Get the next given weekday after an optional offset.
    :param reference_date: The reference datetime object.
    :param target_weekday: The target weekday (Monday=0, ..., Sunday=6).
    :param offset_days: Number of days to offset from the reference date before finding the next target weekday.
    :param target_day_label: Optional label for the target weekday (e.g., "last-friday-of-month, next-sunday, etc").
    :param tz: tzinfo object to be used for the datetime object.
    :return: Datetime object representing the next occurrence of the target weekday.
    """
    tz = tz or Settings.TIMEZONE
    if reference_date is None:
        ref_date = datetime.now(tz=tz)
    else:
        ref_date = reference_date.replace(tzinfo=tz)

    if target_weekday is not None:
        _target_weekday = WEEKDAY2NUM[target_weekday.lower()]
        days_ahead = (_target_weekday - ref_date.weekday()) % 7  # Find next target weekday
        days_ahead = 7 if days_ahead == 0 else days_ahead  # Ensure it's the next occurrence, not the same day
        return ref_date + timedelta(days=days_ahead)
    elif target_day_label:
        if target_day_label.lower() == "last-friday-of-month":
            # Find the last Friday of the month
            next_month = (ref_date.month % 12) + 1
            year = ref_date.year if next_month > 1 else ref_date.year + 1
            last_friday = datetime(year, next_month, 1, tzinfo=tz) - timedelta(days=1)
            while last_friday.weekday() != 4:  # 4 = Friday
                last_friday -= timedelta(days=1)
            return last_friday
        else:
            raise ValueError(f"Unhandled target day: {target_day_label}")
    else:
        return ref_date + timedelta(days=offset_days)  # Apply offset)


def next_weekday_v0(reference_date: datetime = None, target_weekday: str = None, offset_days: int = 0,
                    target_day_label: str = None, tz=None) -> datetime:
    """
    Get the next given weekday after an optional offset.
    :param reference_date: The reference datetime object.
    :param target_weekday: The target weekday (Monday=0, ..., Sunday=6).
    :param offset_days: Number of days to offset from the reference date before finding the next target weekday.
    :param target_day_label: Optional label for the target weekday (e.g., "last-friday, next-sunday, etc").
    :param tz: tzinfo object to be used for the datetime object.
    :return: Datetime object representing the next occurrence of the target weekday.
    """
    tz = tz or Settings.TIMEZONE
    if reference_date is None:
        reference_date = datetime.now(tz=tz)
    future_date = reference_date + timedelta(days=offset_days)  # Apply offset
    if target_weekday is None:
        return future_date
    _target_weekday = WEEKDAY2NUM[target_weekday.lower()]
    days_ahead = (_target_weekday - future_date.weekday()) % 7  # Find next target weekday
    days_ahead = 7 if days_ahead == 0 else days_ahead  # Ensure it's the next occurrence, not the same day
    return future_date + timedelta(days=days_ahead)


def next_business_day(date, tz=None):
    date = pd.to_datetime(date)
    if date.weekday() < 5 and date not in USFederalHolidayCalendar().holidays():
        return date
    else:
        us_business_day = pd.offsets.CustomBusinessDay(calendar=USFederalHolidayCalendar())
        return date + us_business_day


def is_third_friday(date: datetime) -> bool:
    return date.weekday() == 4 and 15 <= date.day <= 21


def get_next_option_expiry_day(ref_date: datetime = None, tz=None, offset_days: int = 0, target_weekday: str = None,
                               target_day_label: str = None, skip_third_friday: bool = False) -> Optional[str]:
    tz = tz or Settings.TIMEZONE
    if ref_date is None:
        ref_date = datetime.now(tz)

    expiry_day = next_weekday(reference_date=ref_date, offset_days=offset_days,
                              target_weekday=target_weekday,
                              target_day_label=target_day_label)
    if skip_third_friday:
        if is_third_friday(date=expiry_day):
            expiry_day += timedelta(days=1)
    expiry_day = next_business_day(expiry_day)
    expiry_str = expiry_day.strftime("%Y%m%d")
    return expiry_str
