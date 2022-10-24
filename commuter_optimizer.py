import googlemaps
from datetime import datetime
import time
from weather_call import *

import json
import csv


#API KEY
gmaps = googlemaps.Client(key='AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

#coordinates of addresses for commute
work = "30.27776141307871, -97.73169690805364"
home = "30.418150227932976, -97.65688514380827"

# north dakota for debugging
# work = "46.87405322078762, -96.79005193134536"

class Commuting:
    "takes 2 address as coordinates and outputs a tuple with the (commute time from add1 to add2, add2 to add1)"

    def __init__(self, work_add, home_add):
        self._work_add = work_add
        self._home_add = home_add
        self._now = datetime.now()


    def commute_time(self):
        work_to_home = gmaps.directions(self._work_add, self._home_add, mode="driving", departure_time=self._now)
        home_to_work = gmaps.directions(self._home_add, self._work_add, mode="driving", departure_time=self._now)

        # commute time with no traffic in seconds
        wth_no_traffic = work_to_home[0]['legs'][0]['duration']['value']
        htw_no_traffic = work_to_home[0]['legs'][0]['duration']['value']

        # gives the commute time in seconds, longer trips dont appear to have the traffic data
        if "duration_in_traffic" not in work_to_home[0]['legs'][0].keys():
            wth = wth_no_traffic
        else:
            wth = work_to_home[0]['legs'][0]['duration_in_traffic']['value']
        if "duration_in_traffic" not in home_to_work[0]['legs'][0]:
            htw = htw_no_traffic
        else:
            htw = home_to_work[0]['legs'][0]['duration_in_traffic']['value']

        if wth < wth_no_traffic:
            wth = wth_no_traffic
        if htw < htw_no_traffic:
            htw = htw_no_traffic


        #warnings on the route
        warnings_wth = work_to_home[0]['warnings']
        warnings_htw = work_to_home[0]['warnings']

        date_data = datetime.now()
        day_of = datetime.today().strftime('%A')

        s_from_midnight =(date_data.hour*3600) + (date_data.minute*60) + date_data.second

        #finds the time for eight hours after the commute has been calculated
        eight_later = date_data.hour + 8
        if eight_later > 24:
            eight_later -= 24

        times = {
            "to_work": htw,
            "to_home": wth,
            "to_work_no_traffic": htw_no_traffic,
            "to_home_no_traffic": wth_no_traffic,
            "warnings_wth": warnings_wth,
            "warnings_htw": warnings_htw,
            "year": date_data.year,
            "month": date_data.month,
            "day": date_data.day,
            "hour": date_data.hour,
            "minute": date_data.minute,
            "second": date_data.second,
            "day_of": day_of,
            "eight_later": eight_later,
            "s_from_midnight": s_from_midnight
        }

        return times

    def show_output(self, dict):
        print("-----------------------------------------------------------------")
        print(f'Date: {dict["month"]}/{dict["day"]}, {dict["day_of"]}')
        print(f'Time: {travel_times["hour"]}:{dict["minute"]}:{dict["second"]}')
        print(f'Commute to work: {dict["to_work"] / 60: .3} minutes')
        print(f'Commute to home: {dict["to_home"] / 60: .3} minutes')
        print(f'Time lost to traffic to work: {(dict["to_work_no_traffic"] - dict["to_work"])/60: .3} minutes')
        print(f'Time lost to traffic to home: {(dict["to_home_no_traffic"] - dict["to_home"])/60: .3} minutes')
        print(f'Total day if leaving now: '
              f'{dict["to_work"] / 3600 + dict["to_home"] / 3600 + 8 + 10 / 60: .3} hours')
        print("-----------------------------------------------------------------")

    def show_raw(self, dict):
        print(dict.keys())
        for i in dict.keys():
            print(f"{i}:{dict[i]}")


data_for_day = []

start_time = time.time()
while True:
    # running commute collection API
    cc = Commuting(work, home)
    travel_times = cc.commute_time()
    cc.show_output(travel_times)
    # cc.show_raw(travel_times)


    # running weather collection API
    ww = Commute_weather("Austin")
    whats_weather = ww.gather_weather()
    ww.show_weather(whats_weather)
    data_for_day.append([travel_times, whats_weather])

    save_file = "test" + str(travel_times["month"]) + "-" + str(travel_times["day"]) + "commute.json"

    print("ahsdfasdfasdf")
    with open(save_file, "w") as write_file:
        json.dump(data_for_day, write_file)

    print("waiting...")
    #run program every 1 minute
    time.sleep(10.0-((time.time() - start_time)%10.0))


