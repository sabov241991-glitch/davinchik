from datetime import datetime, timedelta
from database.database import Database

async def ban_user(user_id: int, hours: int, moderator: str, reason: str):
    db = Database('davinchik.db')
    user = db.get_user(user_id)
    
    user.violations_count += 1
    user.save_to_db()
    
    # Запись нарушения
    violation = Violation(
        violation_id=0,
        user_id=user_id,
        moderator_id=None if moderator == "Система" else moderator,
        reason=reason,
        duration=hours,
        date=datetime.now().isoformat()
    )
    db.save_violation(violation)
    
    # Здесь логика бана пользователя
