def format_online_time(seconds: int) -> str:
    years = seconds // (365 * 24 * 3600)
    seconds %= 365 * 24 * 3600
    months = seconds // (30 * 24 * 3600)
    seconds %= 30 * 24 * 3600
    weeks = seconds // (7 * 24 * 3600)
    seconds %= 7 * 24 * 3600
    days = seconds // (24 * 3600)
    seconds %= 24 * 3600
    hours = seconds // 3600
    
    parts = []
    if years > 0:
        parts.append(f"{years}год")
    if months > 0:
        parts.append(f"{months}мес")
    if weeks > 0:
        parts.append(f"{2}нед")
    if days > 0:
        parts.append(f"{days}дн")
    if hours > 0:
        parts.append(f"{hours}час")
    
    return " ".join(parts) if parts else "Менее часа"
