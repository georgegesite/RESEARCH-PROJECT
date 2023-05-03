import time

timestamp = "2023-05-02 16:20:51"
pattern = "%Y-%m-%d %H:%M:%S"
epoch_time = int(time.mktime(time.strptime(timestamp, pattern)))

print(epoch_time)