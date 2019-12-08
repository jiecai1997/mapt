def deg2rad(deg):
  return abs(deg * (math.pi/180))

def LatLonToMiles(lat1,lon1,lat2,lon2):
  R = 3958.8 #Radius of the earth in miles
  dLat = deg2rad(lat2-lat1)
  dLon = deg2rad(lon2-lon1)
  a = math.sin(dLat/2)**2 + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2)**2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c #Distance in miles
  return int(d)

depart_lat = 35.87760162
depart_long = -78.78749847
arrival_lat = 40.63980103
arrival_long = -73.77890015

mileage = LatLonToMiles(depart_lat,depart_long,arrival_lat,arrival_long)
print(mileage)
