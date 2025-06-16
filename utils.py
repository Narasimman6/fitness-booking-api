from datetime import datetime
import pytz

def convert_timezone(dt_str: str, from_tz: str, to_tz: str) -> str:
    """Convert datetime string from one timezone to another"""
    try:
        from_zone = pytz.timezone(from_tz)
        to_zone = pytz.timezone(to_tz)
        
        dt = datetime.fromisoformat(dt_str)
        dt = from_zone.localize(dt)
        dt = dt.astimezone(to_zone)
        
        return dt.isoformat()
    except Exception as e:
        raise ValueError(f"Timezone conversion failed: {str(e)}")
