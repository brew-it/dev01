import time
import datetime
import robot.valves

import data.config
import robot.relay
from suds.client import Client
from misc.constants import *

import robot.states.controller
import robot.states.fermenting
import robot.states.carbonating
import robot.states.prefermenting

import logging
logger = logging.getLogger(__name__) 

def GetCurrentStateName(value):
    logging.debug('asking  current state for ' + str(value))

    value = int(value)
    if  ( value == STATE_IDLE):
        return 'Idle'
    elif( value == STATE_STARTING):
        return 'Starting'
    elif( value == STATE_PREFERMENTING):
        return 'Prefermenting'
    elif( value == STATE_FERMENTING):
        return 'Fermenting'
    elif( value == STATE_CARBONATING):
        return 'Carbonating'
    elif( value == STATE_DISPENSING):
        return 'Dispensing'
    elif( value == STATE_PAUSING):
        return 'Pausing'
    elif( value == STATE_ENDPAUSE):
        return 'Ending pause'
    elif( value == STATE_STOPPING):
        return 'Dispensing'
    else:
        return str(value)


def MoveNextState(value):
    value = int(value)
    if  ( value == STATE_IDLE):
        SetCurrentState(STATE_IDLE)
    elif( value == STATE_STARTING):
        SetCurrentState(STATE_PREFERMENTING)
    elif( value == STATE_PREFERMENTING):
        SetCurrentState(STATE_FERMENTING)
    elif( value == STATE_FERMENTING):
        SetCurrentState(STATE_CARBONATING)
    elif( value == STATE_CARBONATING):
        SetCurrentState(STATE_DISPENSING)
    elif( value == STATE_DISPENSING):
        SetCurrentState(STATE_STOPPING)
    elif( value == STATE_STOPPING):
        SetCurrentState(STATE_IDLE)


def GetEOSTime():
    try:
        if(data.config.ConfigExists('STATES','EOS_VALUE')):
            return data.config.GetConfig('STATES','EOS_VALUE')
        else:
            return ""
    except IOError:
        return ""

def SetEOSTime(time_value):
    data.config.SetConfig('STATES','EOS_VALUE', time_value)
    logging.debug("setting EOS_VALUE to" + str(time_value))

def RemoveEOSTime():
    data.config.RemoveConfig('STATES','EOS_VALUE')

def EOSExists():
    return data.config.ConfigExists('STATES','EOS_VALUE')


def ValidateEOS(state_id):
    if(not EOSExists()):
        step_duration = GetDuration(state_id)
        logging.info("received value: " + step_duration)
        eos_time = datetime.datetime.now() + datetime.timedelta(seconds=int(step_duration))
        SetEOSTime(eos_time)

    eos_time = GetEOSTime()
    f ="%Y-%m-%d %H:%M:%S.%f"
    return datetime.datetime.strptime(eos_time, f)

def GetDuration(state_id):
    logging.debug(GetCurrentStateName(state_id) + " duration?")
  
    batch_id = robot.device_info.GetBatchId()
    cur_state_id = state_id
    parameter_name = 'DURATION'

    client = Client(data.config.GetApiUrl())
    try:
        duration = client.service.GetBatchParameter(batch_id, cur_state_id, parameter_name)
        return duration
    except:
        # if we receive anything from the server, we go with a default value
        return 60*60*24*7;




def GetCurrentState():
    try:
        current_state = data.config.GetConfig('STATES','CURRENT_STATE')
        logging.debug("return current state : " + robot.states.controller.GetCurrentStateName(current_state))
        return int(current_state)

        #config = ConfigParser.RawConfigParser()
        #config.read('brewit.cfg')
        #return config.getint('STATES', 'CURRENT_STATE')

    except IOError:
        return STATE_IDLE

def SetCurrentState(state_value):
    logging.info("setting current state to " + GetCurrentStateName(state_value))
    data.config.SetConfig('STATES','CURRENT_STATE', state_value)
#    config = ConfigParser.RawConfigParser()
#    config.read('brewit.cfg')
#    config.set('STATES', 'CURRENT_STATE', state_value)

#    with open('brewit.cfg','r+') as configfile:
#        config.write(configfile)












def IdleState():
    logging.info ("entering iddle mode...")
    time.sleep(DEFAULT_IDLE_DELAY)
    
    MoveNextState(STATE_IDLE)
    logging.info ("exiting iddle mode...")
    logging.info("")






def StartingState():
    logging.info ("entering starting mode...")
    time.sleep(DEFAULT_IDLE_DELAY)


    MoveNextState(STATE_STARTING)
    logging.info ("exiting starting mode...")
    logging.info("")






def PausingState():
    logging.info ("entering pausing mode...")

    current_state = robot.states.controller.GetCurrentState()
    while(current_state == STATE_PAUSING):
        logging.debug('device on pause for the next second...')
        time.sleep(1)
        current_state = robot.states.controller.GetCurrentState()

    logging.info ("exiting pausing mode...")
    logging.info("")






def EndPauseState():
    logging.info ("ending the pause mode...")
    last_state_id = data.config.GetConfig('STATES','paused_state')
    SetCurrentState(last_state_id)

    logging.info ("returning to the state..." + GetCurrentStateName(last_state_id))
    logging.info("")




def StoppingState():
    logging.info ("entering stopping mode...")

    time.sleep(DEFAULT_IDLE_DELAY)

    MoveNextState(STATE_STOPPING)
    logging.info ("exiting stopping mode...")
    logging.info("")




   

def PreFermentingState():
    logging.info ("entering prefermenting mode...")

    robot.states.prefermenting.Execute()
    
    current_state = robot.states.controller.GetCurrentState()
    if(current_state == STATE_PREFERMENTING):
            MoveNextState(STATE_PREFERMENTING)

    logging.info ("exiting prefermenting mode...")
    logging.info("")

    
def FermentingState():
    logging.info ("entering fermenting mode...")
    robot.states.fermenting.Execute()

    
    current_state = robot.states.controller.GetCurrentState()
    if(current_state == STATE_FERMENTING):
            MoveNextState(STATE_FERMENTING)

    logging.info ("exiting fermenting mode...")



    

def CarbonatingState():
    logging.info ("entering carbonating mode...%s", robot.states.controller.GetCurrentState())
    import robot.carbonating
    logging.info ("entering carbonating mode...%s", robot.states.controller.GetCurrentState())
    carbonating.Execute()
    
    current_state = robot.states.controller.GetCurrentState()
    if(current_state == STATE_CARBONATING):
        MoveNextState(STATE_CARBONATING)

    logging.info ("exiting carbonating mode...")
    logging.info("")



def DispensingState():
    logging.info ("entering dispensing mode...")
    time.sleep(DEFAULT_IDLE_DELAY)
    logging.info ("exiting dispensing mode...")
    logging.info("")
