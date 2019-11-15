import os
import time
import datetime
import platform

def combine_date_and_time(date, time):
	hour = int(time.split(':')[0])
	minute = int(time.split(':')[1])
	return datetime.datetime(date.year, date.month, date.day, hour, minute)

def get_next_sunset():
	today = datetime.date.today()
	tomorrow = today + datetime.timedelta(days=1)
	today_sunset = None
	tomorow_sunset = None
	with open('sun.csv', 'r') as f:
		for line in f.readlines():
			tokens = line.strip().split(",")
			day = int(tokens[0])
			if day == today.day:
				today_sunset = combine_date_and_time(today, tokens[2*today.month])
			elif day == tomorrow.day:
				tomorrow_sunset = combine_date_and_time(tomorrow, tokens[2*today.month])
			else:
				continue
	now = datetime.datetime.now()
	if (today_sunset - now).total_seconds() < 0:
		return tomorrow_sunset
	return today_sunset

def shutdown():
    shutdown_command = ""
    if platform.system() == "Linux":
        shutdown_command = "shutdown -P now"
    elif platform.system() == "Windows":
        shutdown_command = "shutdown /s /f /t 30"
    else:
        return
    os.system(shutdown_command)
	
if __name__ == "__main__":
	now = datetime.datetime.now()	
        # shutdown one hour between real sunset - due to low light
	sunset = get_next_sunset() - datetime.timedelta(hours=1)    
        num_seconds_until_sunset = (sunset - now).total_seconds()
	print "Sunset:", sunset, "i. e. in", num_seconds_until_sunset, "seconds."
	time.sleep(num_seconds_until_sunset)
        shutdown()
