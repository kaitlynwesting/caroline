import datetime

a = datetime.datetime(2020, 5, 17)
x = datetime.datetime.now()

distance = (x - a)
print(distance)
print(round(distance.seconds/3600, 2), "hours")



