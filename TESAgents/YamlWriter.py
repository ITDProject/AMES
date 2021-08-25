import os
import yaml

YAMLPath = "./YAMLFiles/"
TSAgent = 'ames' 
NBus = 2
IDSOAtBus = 1
NLSE = 2
NHours = 24

auction_datayaml = {}
auction_datayaml['name'] = TSAgent
auction_datayaml['time_delta'] = '1s'
auction_datayaml['broker'] = 'tcp://localhost:5570'
auction_datayaml['values'] = {}
#auction_datayaml['values']['LoadCheck'] = {'topic': 'player/LoadCheck', 'default': 1}

for k in range(NLSE):
	auction_datayaml['values']['loadforecastRTM_LSE'+str(k+1)] = {'topic': 'NetLoadForecastRTM/loadforecastRTM_LSE'+str(k+1), 'default': 1}
	for j in range(NHours):
		auction_datayaml['values']['loadforecastDAM_LSE'+str(k+1)+'_H'+str(j+1)] = {'topic': 'NetLoadForecastDAM/loadforecastDAM_LSE'+str(k+1)+'_H'+str(j+1), 'default': 1}

# for n in range(NBus):
    # if n == IDSOAtBus:
        # for j in range(NHours):
                # auction_datayaml['values']['DALoadForecast_IDSO_'+ str(IDSOAtBus) +'_H'+str(j+1)] = {'topic': 'IDSO_'+ str(IDSOAtBus)+'/DALoadForecast_IDSO_'+str(IDSOAtBus)+'_H'+str(j+1), 'default': 1}

with open( YAMLPath + TSAgent + '.yaml', 'w') as outfile: 
    yaml.dump(auction_datayaml, outfile, default_flow_style=False)