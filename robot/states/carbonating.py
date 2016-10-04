from suds.client import Client
import data.config
import robot.device_info
import robot.states
import misc.constants
from misc.constants import *
import datetime
import time
import logging
logger = logging.getLogger(__name__) 

STATE_NAME = "CARBONATING"
STATE_ID = STATE_CARBONATING


def GetWorkingTemp():
    logging.debug(STATE_NAME + " temperature?")
   
    batch_id = robot.device_info.GetBatchId()
    cur_state_id = STATE_ID
    parameter_name = 'TEMPERATURE'

    client = Client(data.config.GetApiUrl())
    try:
        temperature = client.service.GetBatchParameter(batch_id, cur_state_id, parameter_name)
        return temperature
    except:
        # if we receive anything from the server, we o with a default value
        return 24;
    


def Execute():
    logging.info('Entering execute() for ' + STATE_NAME)
    logging.info("current state %s", robot.states.GetCurrentState())

    eos_time = robot.states.controller.ValidateEOS(STATE_ID)
    logging.info("operation ending at %s",str(eos_time))

    current_state = robot.states.controller.GetCurrentState()
    logging.info("current state %s", robot.states.controller.GetCurrentState())
    while ((datetime.datetime.now()<eos_time) and (current_state == STATE_ID)):
        logging.info("waiting for the end of " + STATE_NAME + "...")
        current_state = robot.states.controller.GetCurrentState()
        time.sleep(1)

    robot.states.controller.RemoveEOSTime()


