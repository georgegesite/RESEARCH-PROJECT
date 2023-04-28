import time

timestamp = "2023-04-25 18:13:48"
pattern = "%Y-%m-%d %H:%M:%S"
epoch_time = int(time.mktime(time.strptime(timestamp, pattern)))

print(epoch_time)