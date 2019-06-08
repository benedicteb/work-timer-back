from datetime import datetime as dt

import pytz


def tz_aware_now(timezone=pytz.timezone("Europe/Oslo")):
    return dt.utcnow().replace(tzinfo=pytz.utc).astimezone(timezone)
