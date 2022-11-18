import googlemaps
from datetime import datetime
import time
from weather_call import *
import json

import os.path
from os import path

import pandas as pd


#API KEY
google_api = open('google_api.txt', 'r').read()
gmaps = googlemaps.Client(key=google_api)

#coordinates of addresses for commute
work = "30.27776141307871, -97.73169690805364"
home = "30.418150227932976, -97.65688514380827"

class Commuting:
    """
    takes two addresses as coordinates and returns a dictionary with info on the commute between them

    methods:
        commute_time() - calculates all the parameters between the two points
        show_output()  - Nice text output for info about the commute
        show_raw()     - Outputs the dictionary of commute info for the commute
    """

    def __init__(self, work_add, home_add):
        self._work_add = work_add
        self._home_add = home_add
        self._now = datetime.now()


    def commute_time(self) -> dict:
        """
        calls the google maps api to find info on the commute to and from two locations
        input - none, locations are passed to the Commuting class
        return - dictionary containing all the commute info
        """
        work_to_home = gmaps.directions(self._work_add,
                                        self._home_add,
                                        mode="driving",
                                        departure_time=self._now)
        home_to_work = gmaps.directions(self._home_add,
                                        self._work_add,
                                        mode="driving",
                                        departure_time=self._now)

        # commute time with no traffic in seconds
        wth_no_traffic = work_to_home[0]['legs'][0]['duration']['value']
        htw_no_traffic = work_to_home[0]['legs'][0]['duration']['value']

        # gives the commute time in seconds, longer trips dont appear to have the traffic data
        # commute w/ traffic is sometimes shorter than without, if so then both are set to be equal
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


        day_of = datetime.today().strftime('%A')
        s_from_midnight = (self._now.hour * 3600) + (self._now.minute * 60) + self._now.second

        #finds the time for eight hours after the commute has been calculated
        eight_later = self._now.hour + 8
        if eight_later > 24:
            eight_later -= 24

        times = {
            "to_work": htw,
            "to_home": wth,
            "to_work_no_traffic": htw_no_traffic,
            "to_home_no_traffic": wth_no_traffic,
            "warnings_wth": warnings_wth,
            "warnings_htw": warnings_htw,
            "year": self._now.year,
            "month": self._now.month,
            "day": self._now.day,
            "hour": self._now.hour,
            "minute": self._now.minute,
            "second": self._now.second,
            "day_of": day_of,
            "eight_later": eight_later,
            "s_from_midnight": s_from_midnight
        }

        return times

    def show_output(self, dict) -> None:
        """
        Multiple print statements giving most pertinent info on the commute

        input - dictionary from the commute_time function
        output - print statements
        """
        lost_to_work = round((dict["to_work_no_traffic"] - dict["to_work"]) / 60, 3)
        lost_to_home = round((dict["to_home_no_traffic"] - dict["to_home"])/60, 3)

        print("-----------------------------------------------------------------")
        print(f'Date: {dict["month"]}/{dict["day"]}, {dict["day_of"]}')
        print(f'Time: {travel_times["hour"]}:{dict["minute"]}:{dict["second"]}')
        print(f'Commute to work: {dict["to_work"] / 60: .3} minutes')
        print(f'Commute to home: {dict["to_home"] / 60: .3} minutes')
        print(f'Time lost to traffic to work: {lost_to_work} minutes')
        print(f'Time lost to traffic to home: {lost_to_home} minutes')
        print(f'Total day if leaving now: '
              f'{dict["to_work"] / 3600 + dict["to_home"] / 3600 + 8 + 10 / 60: .3} hours')
        print("-----------------------------------------------------------------")

    def show_raw(self, dict):
        print(dict.keys())
        for i in dict.keys():
            print(f"{i}:{dict[i]}")





def save_to_json(list1, list2):
    data_to_save = [list1, list2]
    file_name = "fxntest" + str(list1["month"]) + "-" + str(list1["day"]) + "commute.json"
    if path.exists(file_name) is True:
        print("appending data to json")
        with open(file_name, 'r') as openfile:
            to_change = json.load(openfile)
            to_change.append(data_to_save)  # data to append here
            with open(file_name, "w") as outfile:
                json.dump(to_change, outfile)
    else:
        print("make new json")
        with open(file_name, "w") as outfile:
            json.dump([data_to_save], outfile)


if __name__ == '__main__':

    data_for_day = {}
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

        print("save to json running")
        save_to_json(travel_times, whats_weather)
        print("save to json ran?")

        def hehe():
            # saving the data for commmute and weather as JSON
            # format [[{commute}, {weather}], [{commute}, {weather}], ...]
            data_for_day.append([travel_times, whats_weather])
            save_file = "test" + str(travel_times["month"]) + "-" + str(travel_times["day"]) + "commute.json"
            print("saving file")
            with open(save_file, "w") as write_file:
                json.dump(data_for_day, write_file)

            print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
            save_to_json(travel_times, whats_weather)
            print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")

        def pandas_store():
        # storing the data in a pandas dataframe
            data = {
                "to_home": data_for_day[0][0]['to_home'],
                "to_work": data_for_day[0][0]['to_work']
            }
            df = pd.DataFrame(data, index=[data_for_day[0][0]['s_from_midnight']])

        print("waiting...")
        #run program every 5 minutes
        # time.sleep(300.0-((time.time() - start_time)%300.0))
        time.sleep(10.0-((time.time() - start_time)%10.0))

