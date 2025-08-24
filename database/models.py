from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class User:
    user_id: int
    username: str = ""
    role: int = 0
    registered: bool = False
    registration_date: Optional[str] = None
    clan_id: Optional[int] = None
    clan_role: int = 0
    rating: int = 1000
    games_played: int = 0
    games_won: int = 0
    room_sign: str = ""
    last_activity: Optional[str] = None
    messages_count: int = 0
    violations_count: int = 0
    online_time: int = 0  # в секундах
    last_online: Optional[str] = None
    referral_code: str = ""
    referred_by: Optional[int] = None
    referrals_count: int = 0
    photos: List[str] = None  # список photo_id

    def __post_init__(self):
        if self.photos is None:
            self.photos = []

@dataclass
class Violation:
    violation_id: int
    user_id: int
    moderator_id: Optional[int]  # None если система
    reason: str
    duration: int  # в часах
    date: str
