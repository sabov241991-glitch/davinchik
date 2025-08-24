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
    online_time: int = 0
    last_online: Optional[str] = None
    referral_code: str = ""
    referred_by: Optional[int] = None
    referrals_count: int = 0
    photos: List[str] = None

    def __post_init__(self):
        if self.photos is None:
            self.photos = []

@dataclass
class Profile:
    user_id: int
    name: str = ""
    age: int = 0
    gender: str = ""
    bio: str = ""

@dataclass
class Clan:
    clan_id: int
    name: str
    description: str
    owner_id: int
    created_date: str
    members_count: int = 1
    rating: int = 1000

@dataclass
class Announcement:
    announcement_id: int
    user_id: int
    text: str
    date: str
