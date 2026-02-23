from datetime import datetime, timedelta

today = datetime.now()

print("Yesterday:", today - timedelta(days=1))
print("Today:", today)
print("Tomorrow:", today + timedelta(days=1))
