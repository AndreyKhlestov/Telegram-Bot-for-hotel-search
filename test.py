from datetime import datetime, date, timedelta


a = datetime.now().date()
a += timedelta(days=1)
print(a)
