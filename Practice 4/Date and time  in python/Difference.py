from datetime import datetime, timedelta

now = datetime.now()
yesterday = now - timedelta(days=1)

print((now - yesterday).total_seconds())
