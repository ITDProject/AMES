import sys
import json

from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
import fncs

FileName = 'NetLoadScData.2BusTestCase.RTM.json'
FilePath = './forecast/data/'

def NetLoadScenarioDataJsonFormat(filename):
	NLSE = 0
	NDay = 0
	f = open(FilePath + filename,'r')
	NetLoadScenarioData = json.load(f)
	NLSE = len(NetLoadScenarioData)
	NDay = [len(val) for key, val in NetLoadScenarioData[0].items()]
	return NDay[0], NLSE, NetLoadScenarioData

def loadforecast_RP(h, d, filename):
	time = []
	NDay, NLSE, NetLoadScenarioData = NetLoadScenarioDataJsonFormat(filename)
	ListLSENodes = []
	loadforecastRTM = [[] for i in range(3)]
	loadforecastDAM = []
	unit = 1 #1000000000
	for ele in NetLoadScenarioData:
		for k in ele:
			ListLSENodes.append(k)
	#print('ListLSENodes:', ListLSENodes)
	if h ==22:
		h1 = 24
		d2 = d-1
	elif h ==23:
		h1 = 1
		d2 = d
	else:
		h1 = h+2
		d2 = d-1
	#h1 = 0 if h == 23 else h+1
	#d2 = d if h == 23 else d-1
	d2 = 0 if d2 >= NDay else d2
	
	print('d, h:', d, h)
	#print('NLSE:'+str(NLSE))
	#RTM
	#y = (h* hour_len)*unit + (d)*(day_len)*unit + M*min_len*unit #- 1*unit #10*10*1000000000
	#y = ((h+1) * hour_len) * unit + (d) * (day_len) * unit - M * min_len * unit #- 1*unit #10*10*1000000000
	#print('RTM:',y)
	NSteps = (int) (hour_len / (M * min_len))
	print('NSteps:', NSteps)
	for count in range(NSteps):
		y = ((h+1) * hour_len) * unit + (d) * (day_len) * unit - M * min_len * unit + count * M * min_len * unit #- 1*unit #10*10*1000000000
		print('RTM y:', y)
		for i in range(NLSE):
			load.append((y, 'loadforecastRTM_LSE'+str(i+1), float(NetLoadScenarioData[i][ListLSENodes[i]][d2][h1-1])))
			print('d2, h1:', d2, h1, float(NetLoadScenarioData[i][ListLSENodes[i]][d2][h1-1]))
	return None

def get_number(value):
	return float(''.join(ele for ele in value if ele.isdigit() or ele == '.'))

if len(sys.argv) == 3:
	tmax = int(sys.argv[1])
	RTOPDur = int(sys.argv[2])
elif len(sys.argv) == 1:
	tmax = 2 * 24 * 3600 #172800
	RTOPDur = 5
else:
	print ('usage: python loadforecast.py [tmax deltaT]')
	sys.exit()

fncs.initialize()

ts = 0
timeSim = 0

min_len = 60
hour_len = 60 * min_len #100 # in s
day_len = 24* hour_len # in s
prev_hour = 0
prev_day = 0

deltaT = RTOPDur * min_len
M = RTOPDur
#M = (int) (deltaT/ min_len)
print('M:', M)

load = []

while ts <= tmax:
	print ('time step: ',ts, flush = True)
	day = int(ts / day_len)# - ts % 2400 # day = 24*100s $ day_len = 2400s
	hour = int((ts - (day * day_len)) / hour_len)
	minute = (ts - (day * day_len) - hour * hour_len)/60
	#print ('day:', day, 'hour:', hour, 'minute:', minute, flush= True)


	if prev_hour != hour:
		if hour == 22 or 23:
			loadforecast_RP(hour, day, FileName)
		elif day>0:
			loadforecast_RP(hour, day, FileName)

	#print ('ts3: ',ts, flush = True)
	if(len(load)!=0):
		#print ('ts3: ',ts, flush = True)
		for i in range(len(load)):
			#print('ts3:', ts, 'load[i][0]:', load[i][0], flush=True)
			if(ts >= load[i][0]):
				#print ('ts4: ',ts, flush = True)
				if(ts == load[i][0]):
					print('Publishing load forecast to AMES: ', str(load[i][0]), str(load[i][1]), load[i][2], flush = True)
					fncs.publish(str(load[i][1]), load[i][2])
			else:
				break
	if(ts < (timeSim + deltaT)) :
		ts = fncs.time_request(timeSim + deltaT)
	else:
		#print('time_granted2:', ts, flush = True)
		timeSim = timeSim + deltaT
		ts = fncs.time_request(timeSim + deltaT)

	#print('Day:', day, 'Hour:', hour, flush=True)
	prev_day = day
	prev_hour = hour


fncs.finalize()