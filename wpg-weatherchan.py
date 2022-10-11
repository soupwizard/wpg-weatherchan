# Retro Winnipeg Weather Channel
# By probnot
# V0.0.17

from tkinter import *
import time
import datetime
from env_canada import ECWeather
import feedparser
import requests
import json
import asyncio

# clock Updater

def clock():
    current = time.strftime("%I:%M:%S")
    timeText.configure(text=current)
    root.after(1000, clock) # run every 1sec
    
# main weather pages
    
def weather_page():
    # pull in current seconds and minutes -- to be used to cycle the middle section every 30sec
    time_sec = time.localtime().tm_sec
    time_min = time.localtime().tm_min
    
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    months = [" ", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"] 
  
    #
    ### Create summary forecast
    #

    # read in day1 text summary forecast
    wsum_day1 = ec_en.conditions["text_summary"]["value"] 
    
    # padding for final string, to move fill remaining line and next line
    len_pad_day1 = len(wsum_day1) % 35 
    w_pad_day1 = ""
    for r in range(35*2-len_pad_day1):
        w_pad_day1 = w_pad_day1 + " " 
    
    # read in day2 text summary forecast
    wsum_day2 =  ec_en.daily_forecasts[2]["period"] + ". " + ec_en.daily_forecasts[2]["text_summary"] 
    
    # padding for final string, to move fill remaining line and next line
    len_pad_day2 = len(wsum_day2) % 35 
    w_pad_day2 = ""
    for r in range(35*2-len_pad_day2):
        w_pad_day2 = w_pad_day2 + " "
    
    # read in day3 text summary forecast
    wsum_day3 = ec_en.daily_forecasts[3]["period"] + ". " + ec_en.daily_forecasts[3]["text_summary"] 
    
    # padding for final string, to move fill remaining line and next line
    len_pad_day3 = len(wsum_day3) % 35 
    w_pad_day3 = ""
    for r in range(35*2-len_pad_day3):
        w_pad_day3 = w_pad_day3 + " "
    
    # read in day4 text summary forecast
    wsum_day4 = ec_en.daily_forecasts[4]["period"] + ". " + ec_en.daily_forecasts[4]["text_summary"] 

    # padding for final string, to move fill remaining line and next line
    len_pad_day4 = len(wsum_day4) % 35 
    w_pad_day4 = ""
    for r in range(35*2-len_pad_day4):
        w_pad_day4 = w_pad_day4 + " "

    wsum_day5 = ec_en.daily_forecasts[5]["period"] + ". " + ec_en.daily_forecasts[5]["text_summary"] # read in day4 text summary forecast

    s = wsum_day1.upper() + w_pad_day1 + wsum_day2.upper() + w_pad_day2 + wsum_day3.upper() + w_pad_day3 + wsum_day4.upper() + w_pad_day4 + wsum_day5.upper()
    

    #
    ### Update middle screen info
    #

    if time_sec < 30:

        weathercol = "Blue"
        if (time_min % 2) == 0: # screen 1 -- text summary forecasts
            print(time.strftime("%H:%M:%S"), 'Displaying screen 1 - forecast summary part 1')
        
            s1 = s[:35]
            s2 = s[35:70]
            s3 = s[70:105]
            s4 = s[105:140]
            s5 = s[140:175]
            s6 = s[175:210]
            s7 = s[210:245]
            s8 = s[245:280]
        else: # screen 3 -- Today's day/date + specific weather conditions
            print(time.strftime("%H:%M:%S"), 'Displaying screen 3 - current weather')
               
            ######################
            # S1 Today's Weather
            ######################

            today = datetime.datetime.today()
            year    = str(today.year)
            month   = str(today.month)
            day     = str(today.day)
            weekday = today.weekday()

            # forecast time is a datetime.datetime
            minute = str(ec_en.forecast_time.minute).zfill(2)
            hour = ec_en.forecast_time.hour
            if (hour > 12):
                hour = str(hour - 12)
                ampm = "PM"
            else:
                hour = str(hour)
                ampm = "AM"

            # s1 example: "WINNIPEG - FRI,FEB.14/2020"
            s1 = station_name.upper() + " - " + days[weekday] + ", " + months[int(month)] + "." + day + "/" + year + " " + hour + ":" + minute + " " + ampm

            ######################
            # S2 Today's Weather
            ######################
            s2 = " "

            ##########################
            # S3 & S4 Today's Weather
            ##########################

            temp_c       = str(ec_en.conditions["temperature"]["value"])
            tendency     = ec_en.conditions["tendency"]["value"]
            if "value" in ec_en.conditions["wind_chill"]:
                wind_chill_c = ec_en.conditions["wind_chill"]["value"]
                if wind_chill_c:
                    wind_chill_c = str(wind_chill_c)
                    s3 = "TEMP " + temp_c + "C (FEELS LIKE " + wind_chill_c + "C)"
                else:
                    s3 = "TEMP " + temp_c + "C"
                s4 = ".. AND " + tendency.upper()
            else:
                s3 = "TEMPERATURE " + temp_c + "C" + " .. AND " + tendency.upper()
                s4 = ""

            ######################
            # S5 Today's Weather
            ######################
            
            high_of_c = str(ec_en.conditions["high_temp"]["value"])
            low_of_c  = str(ec_en.conditions["low_temp"]["value"])
            s5 = "HIGH OF " + high_of_c + "C     " + "LOW OF " + low_of_c + "C"

            #############################
            # S6, S7, S8 Today's Weather
            #############################

            humidity     = str(ec_en.conditions["humidity"]["value"])
            dewpoint_c   = str(ec_en.conditions["dewpoint"]["value"])
            pressure_kpa = str(ec_en.conditions["pressure"]["value"])

            humidity_dewpoint_line = "HUMIDITY " + humidity + "%    DEWPOINT " + dewpoint_c + "C"
            pressure_line          = "PRESSURE " + pressure_kpa + "KPA"

            if "value" in ec_en.conditions["wind_dir"]:
                wind_dir       = str(ec_en.conditions["wind_dir"]["value"])
                wind_speed_kph = str(ec_en.conditions["wind_speed"]["value"])
                visibility_km  = str(ec_en.conditions["visibility"]["value"])
                s6 = "WIND " + wind_dir + " " + wind_speed_kph + " KMH   VISIBILITY " + visibility_km + "KM"
                s7 = humidity_dewpoint_line 
                s8 = pressure_line
            elif "value" in ec_en.conditions["visibility"]:
                visibility_km  = str(ec_en.conditions["visibility"]["value"])
                s6 = "VISIBILITY " + visibility_km + "KM"
                s7 = humidity_dewpoint_line 
                s8 = pressure_line
            else:
                s6 = humidity_dewpoint_line 
                s7 = pressure_line
                s8 = ""


    if time_sec >= 30:
        weathercol = "Red"
        if (time_min % 2) == 0: # screen 2 -- text summary forecasts continued
            print(time.strftime("%H:%M:%S"), 'Displaying screen 2 - forecast summary part 2')
            s1 = s[280:315]
            s2 = s[315:350]
            s3 = s[350:385]
            s4 = s[385:420]
            s5 = s[420:455]
            s6 = s[455:490]
            s7 = s[490:525]
            s8 = s[525:560]
        else: # screen 4 -- static channel listing page
            print(time.strftime("%H:%M:%S"), 'Displaying screen 4 - channel listing')
            
            # update weather info between weather screens
            print("Updating weather")
            asyncio.run(ec_en.update())

            s1 = "==========CHANNEL LISTING=========="
            s2 = "3.1  SRC(CBWFT)    20   SEINFELD"
            s3 = "6.1  CBC(CBWT)     22   WEATHER"
            s4 = "7.1  CTV(CKY)      35.1 JOYTV(CIIT)"
            s5 = "9.1  GLOBAL(CKND)"
            s6 = "13.1 CITY(CHMI)" 
            s7 = "14   THE SIMPSONS"
            s8 = "18   LOONEY TUNES"


    # create the canvas for middle page text
    weather = Canvas(root, height=270, width=720, bg=weathercol)
    weather.place(x=0, y=100)
    weather.config(highlightbackground=weathercol)
    
    # place the 8 lines of text
    weather.create_text(85, 15, anchor='nw', text=s1, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 45, anchor='nw', text=s2, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 75, anchor='nw', text=s3, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 105, anchor='nw', text=s4, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 135, anchor='nw', text=s5, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 165, anchor='nw', text=s6, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 195, anchor='nw', text=s7, font=('VCR OSD Mono', 20, "bold"), fill="white") 
    weather.create_text(85, 225, anchor='nw', text=s8, font=('VCR OSD Mono', 20, "bold"), fill="white") 
    
    root.after(30000, weather_page) # re-run every 30sec from program launch

#####################################################################################################

# setup main stuff

root = Tk()
root.attributes('-fullscreen',False)
root.geometry("720x480")
root.config(cursor="none", bg="green")
root.wm_title("wpg-weatherchan_V0.0.17")

# Clock - Top RIGHT

timeText = Label(root, text="", font=("VCR OSD Mono", 36), fg="white", bg="green")
timeText.place(x=425, y=40)
clock()

# Title - Top LEFT

Title = Label(root, text="ENVIRONMENT CANADA", font=("VCR OSD Mono", 22), fg="white", bg="green")
Title.place(x=80, y=55)

# use ECWeather to gather weather data, station_id is from the csv file provided with ECDada -- homepage: https://github.com/michaeldavie/env_canada

toronto  = ('Toronto',  'ON/s0000458')
winnipeg = ('Winnipeg', 'MB/s0000193')

# SET STATION HERE
station = toronto

station_name = station[0] 
station_id   = station[1]

ec_en = ECWeather(station_id=station_id, language='english')
print("Updating weather at start, location:", station_id)
asyncio.run(ec_en.update())

# Middle Section (Cycling weather pages, every 30sec)
weather_page()

# scrolling text canvas

marquee = Canvas(root, height=120, width=580, bg="green")
marquee.config(highlightbackground="green")
marquee.place(x=80, y=375)

# read in RSS data and prepare it

width = 35
pad = ""
for r in range(width): #create an empty string of 35 characters
    pad = pad + " " 

url = "https://winnipeg.ca/interhom/RSS/RSSNewsTopTen.xml"
wpg = feedparser.parse(url)

# use the first 8 entries on the wpg news RSS feed
wpg_desc = wpg.entries[0]["description"] + pad + wpg.entries[1]["description"] + pad + wpg.entries[2]["description"] + pad + wpg.entries[3]["description"] + pad + wpg.entries[4]["description"] + pad + wpg.entries[5]["description"] + pad + wpg.entries[6]["description"] + pad + wpg.entries[7]["description"]
mrq_msg = wpg_desc.upper()

# use the length of the news feeds to determine the total pixels in the scrolling section
marquee_length = len(mrq_msg)
if (marquee_length * 24)<31000:
    pixels = marquee_length * 24 # roughly 24px per char
else:
    pixels = 31000

# setup scrolling text

text = marquee.create_text(1, 2, anchor='nw', text=pad + mrq_msg + pad + pad, font=('VCR OSD Mono', 25,), fill="white")

restart_marquee = True # 
while restart_marquee:
    restart_marquee = False
    for p in range(pixels+601):
        marquee.move(text, -1, 0) #shift the canvas to the left by 1 pixel
        marquee.update()
        time.sleep(0.005) # scroll every 5ms
        if (p == pixels+600): # once the canvas has finished scrolling
            restart_marquee = True
            marquee.move(text, pixels+600, 0) # reset the location
            p = 0 # keep the for loop from ending
    
root.mainloop()
