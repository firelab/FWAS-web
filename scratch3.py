# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 15:50:57 2017

@author: tanner
"""

import send

Alert='Fire Weather Alert:\n\nThe following thresholds have been reached. All observations were taken within a 12 mile radius of your location, All times are: America/Denver.\n\nTHE TEMPERATURE THRESHOLD HAS BEEN EXCEEDED FROM THE FOLLOWING SOURCES.\nStation KMSO, 0.4 miles at 80.8 degrees E from your location reported a temperature of 59.0 F at 11:35 2017-06-16 UTC-06:00\nStation TS934, 6.9 miles at 180.4 degrees S from your location reported a temperature of 58.0 F at 11:01 2017-06-16 UTC-06:00\nStation PNTM8, 10.0 miles at 32.5 degrees NNE from your location reported a temperature of 38.0 F at 10:59 2017-06-16 UTC-06:00\nStation TR266, 8.7 miles at 356.3 degrees N from your location reported a temperature of 55.0 F at 11:28 2017-06-16 UTC-06:00\nThe temperature is FORECASTED to exceed 5 F from 10:00, 2017-06-16 to 16:00, 2017-06-16\n\nTHRESHOLDS FOR WIND SPEED HAVE BEEN EXCEEDED FROM THE FOLLOWING SOURCES.\nStation KMSO, 0.4 miles at 80.8 degrees E from your location reported a wind speed of 8.1 mph at 11:35 2017-06-16 UTC-06:00\nStation PNTM8, 10.0 miles at 32.5 degrees NNE from your location reported a wind speed of 21.0 G 33.0 mph at 10:59 2017-06-16 UTC-06:00\nThe wind speed is FORECASTED to exceed 2 mph from 10:00, 2017-06-16 to 16:00, 2017-06-16\n\nTHRESHOLDS FOR RELATIVE HUMIDITY HAVE BEEN EXCEEDED FROM THE FOLLOWING SOURCES.\nStation KMSO, 0.4 miles at 80.8 degrees E from your location reported a relative humidity of 67.4 % at 11:35 2017-06-16 UTC-06:00\nThe relative humidity is FORECASTED to be less than 75 % from 10:00, 2017-06-16 to 16:00, 2017-06-16\n\nHRRR RADAR FORECAST:\nWeather Intensity in the general area is FORECASTED to be\nLight from 10:00, 2017-06-16 to 16:00, 2017-06-16\nClosest to Your Location: \nLight to moderate from 10:00, 2017-06-16 to 16:00, 2017-06-16\n\nHRRR PRECIP FORECAST:\nPrecipitation in the general area is FORECASTED to be greater than 0.01 inches/hour from 14:00, 2017-06-16 to 16:00, 2017-06-16\n\nPRECIP ALERT:\nStation KMSO, 0.4 miles at 80.8 degrees E from your location reported 0.001 inches of liquid precip within the last hour.\n\nSet thresholds are:\nwind_speed: 2 mph. relative_humidity: 75 %. wind_gust: 10 mph. temperature: 5 F. \n'

q=Alert.split('\n')

#for i in range(len(q)):
#    if q[i]=='':
#        q.pop(i)

qA=[x for x in q if x!='']


headerLib={'alert_name': 'Alert',
 'alert_time': '2017-06-16 14:11:56',
 'carrier': 'NaN',
 'email': 'fsweather1@usa.com',
 'expires_after': '24',
 'latitude': '46.92',
 'limit': '0',
 'longitude': '-114.1',
 'phone': 'NaN',
 'radius': '12',
 'time_zone': '2'}

d=len(qA) 
for i in range(len(qA)):
    aName=headerLib['alert_name']+' '+str(i)+'/'+str(d)
    send.sendEmailAlert(qA[i],headerLib['email'],aName)