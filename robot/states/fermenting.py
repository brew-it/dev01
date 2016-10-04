from suds.client import Client
from misc.constants import *
import robot.states.controller
import data.config
import robot.device_info
import robot.states
import misc.constants
import datetime
import time
import logging

logger = logging.getLogger(__name__) 

STATE_NAME = "FERMENTING"
STATE_ID = STATE_FERMENTING


def GetWorkingTemp():
    logging.debug(STATE_NAME + " temperature?")
   
    batch_id = robot.device_info.GetBatchId()
    state_id = STATE_ID
    parameter_name = 'TEMPERATURE'

    client = Client(data.config.GetApiUrl())
    try:
        temperature = client.service.GetBatchParameter(batch_id, state_id, parameter_name)
        return float(temperature)
    except:
        # if we receive anything from the server, we go with a default value
        return 24;
    


def Execute():
    logging.debug('Entering execute() for %s', STATE_NAME)
    logging.info("current state %s", robot.states.controller.GetCurrentState())

    #print('sleeping for 30 seconds...')
    #time.sleep(30)
    eos_time = robot.states.controller.ValidateEOS(STATE_ID)
    logging.info("operation ending at " + str(eos_time))   

    robot.valves.open_3valve()

    current_state = robot.states.controller.GetCurrentState()
    logging.info("current state %s", robot.states.controller.GetCurrentState())

    while ((datetime.datetime.now()<eos_time) and (current_state == STATE_ID)):
        logging.info("waiting for the end of " + STATE_NAME + "...")
        cur_temp = robot.device_info.GetFermenterTemperature()
        recipe_temp = GetWorkingTemp()
        if(cur_temp< recipe_temp):
            logging.info('we will have to heat... current temp:' + str(cur_temp) +' recipe temp: ' + str(recipe_temp))
        else:
            logging.info('temp is ok ' + str(cur_temp))

        
        current_state = robot.states.controller.GetCurrentState()
        time.sleep(1)

    robot.valves.close_3valve()
    
    robot.states.controller.RemoveEOSTime()


