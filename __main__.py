from misc.constants import *
from robot.states.controller import *

import robot.relay
import robot.valves
import robot.device_info
import robot.states
import logging.config
import sys


def main():
    import logging.config
    logging.config.fileConfig('logging.cfg')
    # program code

#    GetCurrentState()
#    SetCurrentState(0)


if __name__ == '__main__':
        main()


##############################
## debut du programme initial
##############################

#config of the relays
try:
    robot.relay.setup_relays()
    while 1:
            # getting current states from the server
            current_state = GetCurrentState()

            # swiching config based on current state
            if   current_state == STATE_IDLE:
                IdleState()
            elif current_state == STATE_STARTING:
                StartingState()
            elif current_state == STATE_PAUSING:
                PausingState()
            elif current_state == STATE_ENDPAUSE:
                EndPauseState()
            elif current_state == STATE_PREFERMENTING:
                PreFermentingState()
            elif current_state == STATE_FERMENTING:
                FermentingState()
            elif current_state == STATE_CARBONATING:
                CarbonatingState()
            elif current_state == STATE_DISPENSING:
                DispensingState()
            elif current_state == STATE_STOPPING:
                StoppingState()
            else:
                IdleState()
                
    # cleaning relay after use
    robot.relay.cleanup_relays()
except:
    try:
        logging.error("fatal error:" +  str(sys.exc_info()[:2]))
        # cleaning relay after use
        robot.relay.cleanup_relays()

    except:
        print("fatal error: " + str(sys.exc_info()[:2]))
            

    
