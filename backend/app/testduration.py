from datetime import datetime

def fcn(flight):
	depart_date = flight['dep']['date'].split("00:00:00")[0].split(" ")
	depart_mth = monthdic[depart_date[1]]
	depart_day = depart_date[2]
	depart_yr = depart_date[3]
	depart_hr = int(flight['dep']['time'].split(':')[0])
	int_depart_hr = depart_hr
	depart_min = flight['dep']['time'].split(':')[1]
	depart_ampm = 'AM'
	if depart_hr >= 12:
		depart_hr-=12
		depart_ampm = 'PM'
	depart_datetime = depart_yr+depart_mth+depart_day+' '+str(depart_hr)+':'+depart_min+':00'+depart_ampm
	dt_depart_datetime = datetime(int(depart_yr),int(depart_mth),int(depart_day),int_depart_hr,int(depart_min))


	arr_date = flight['arr']['date'].split("00:00:00")[0].split(" ")
	arr_mth = monthdic[arr_date[1]]
	arr_day = arr_date[2]
	arr_yr = arr_date[3]
	arr_hr = int(flight['arr']['time'].split(':')[0])
	int_arr_hr = arr_hr
	arr_min = flight['arr']['time'].split(':')[1]
	arr_ampm = 'AM'
	if arr_hr >= 12:
		arr_hr-=12
		arr_ampm = 'PM'
	arrival_datetime = arr_yr+arr_mth+arr_day+' '+str(arr_hr)+':'+arr_min+':00 '+arr_ampm
	dt_arr_datetime = datetime(int(arr_yr),int(arr_mth),int(arr_day),int_arr_hr,int(arr_min))

	duration = (dt_arr_datetime-dt_depart_datetime).seconds//60
	offset_mins = -(float(arrival_tz)-float(depart_tz))*60
	duration += offset_mins

    return duration

flight = {}
flight['dep']={}
flight['dep']['date']= "Sat Nov 30 2019 00:00:00 GMT-0500 (Eastern Standard Time)"
flight['dep']['time']= "17:00"
flight['dep']['airport']="TUS"
flight['arr']={}
flight['arr']['date']= "Sun Dec 01 2019 00:00:00 GMT-0500 (Eastern Standard Time)"
flight['arr']['time']= "05:00"
flight['arr']['airport']= "MIA"
monthdic = {'Jan':'01', 'Feb':'02','Mar':'03', 'Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
arrival_tz = 5
depart_tz=-2

print(fcn(flight))
