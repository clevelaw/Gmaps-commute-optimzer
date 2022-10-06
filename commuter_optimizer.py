import googlemaps
from datetime import datetime

my_date = datetime.today().strftime('%A')

#API KEY
gmaps = googlemaps.Client(key='AIzaSyA76RjHZJgUN3RU2NPRbYTOHfy39IlvYg8')

#coordinates of addresses for commute
work = "30.27776141307871, -97.73169690805364"
home = "30.418150227932976, -97.65688514380827"

#time that the commute was figured
now = datetime.now()
my_date = datetime.today().strftime('%A')

class Commuting:
    "takes 2 address as coordinates and outputs a tuple with the (commute time from add1 to add2, add2 to add1)"
    def __init__(self, work_add, home_add):
        self._work_add = work_add
        self._home_add = home_add

    def commute_time(self):
        work_to_home = gmaps.directions(self._work_add, self._home_add, mode="driving", departure_time=now)
        home_to_work = gmaps.directions(self._home_add, self._work_add, mode="driving", departure_time=now)

        wth_commute_str = work_to_home[0]['legs'][0]['duration']['text']
        htw_commute_str = home_to_work[0]['legs'][0]['duration']['text']

        #time is returned as a string ie "99 min", filter and returns all ints
        wth = [int(x) for x in wth_commute_str.split() if x.isdigit()][0]
        htw = [int(x) for x in htw_commute_str.split() if x.isdigit()][0]

        date_data = datetime.now()
        day_of = datetime.today().strftime('%A')

        eight_later = date_data.hour + 8
        if eight_later > 24:
            eight_later -= 24

        times = [date_data.month, date_data.day, date_data.hour, date_data.minute, date_data.second, day_of, eight_later]



        return wth, htw, times

cc = Commuting(work, home)
travel_times = cc.commute_time()
#(to home, to work, [month, day, hour, minute, second, weekday, eight_later])

time_dict = {}
print("<<<<<<<<<<<<")
print(travel_times[2][5])
print("Month:", travel_times[2][0], "Day:", travel_times[2][1])
print("Time:", travel_times[2][2],":",travel_times[2][3],":",travel_times[2][4])
print("Time 8 hours from now:", travel_times[2][6],":",now.minute,":",now.second)
print("Commute to work:", travel_times[1])
print("Commute to home:", travel_times[0])
print("total day at this rate:", travel_times[0]/60+travel_times[1]/60+8+10/60, "hours")

#time_dict[now] = [wth_commute, htw_commute]