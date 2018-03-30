import csv
import datetime
import os
import time
import requests # this library makes html requests much simpler


# add your API key (from wunderground) here
api_key = "insert API key here"
station_ids = ["choose your station", ] # add more stations here if required


for station_id in station_ids:
	print ("Fetching data for station ID: %s" % station_id)
	try:
		# initialise your csv file
		with open('%s.csv' % station_id, 'w') as outfile:
			writer = csv.writer(outfile)
			headers = ['date','temperature'] # edit these as required
			writer.writerow(headers)

			# enter the first and last day required here
			start_date = datetime.date(2017,1,1)
			end_date = datetime.date(2018,2,28)

			date = start_date
			call_count = 1
			while date <= end_date:
				# format the date as YYYYMMDD
				date_string = date.strftime('%Y%m%d')
				# build the url
				url = ("http://api.wunderground.com/api/%s/history_%s/q/%s.json" %(api_key, date_string, station_id))
				# make the request and parse json
				data = requests.get(url).json()
				# build your row
				for history in data['history']['observations']:
					row = []
					row.append(str(history['date']['pretty']))
					row.append(str(history['tempm']))       
					writer.writerow(row)
				# increment the day by one
				date += datetime.timedelta(days=1)
				call_count = call_count + 1
				print("Call Count: ",call_count)
				if call_count == 10:
					print("API Call Count = ",call_count,". Pausing for 1 minute")
					call_count = 1
					time.sleep(60)
                                        
	except Exception:
		# tidy up
		os.remove(outfile)
		
print ("Done!")


