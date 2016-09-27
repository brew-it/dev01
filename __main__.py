import misc
import robot.relay
import robot.valves
import robot.device_info
import logging.config

def main():
    import logging.config
    logging.config.fileConfig('logging.conf')
    # program code

    logging.debug("1")
    logging.info("2")
    logging.warn("3")
    logging.error("4")
    logging.critical("5")

if __name__ == '__main__':
        main()


##############################
## debut du programme initial
##
##############################
robot.relay.setup_relays()

while 1:
    temp = robot.device_info.GetFermenterTemperature();
    serial = robot.device_info.GetDeviceID();
    robot.device_info.GetTempProbeFilename()

    #if temp < 28:
    #test_relay();

    robot.valves.open_3valve()
    robot.valves.close_3valve()
    
robot.relay.cleanup_relays()

    
