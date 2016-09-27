import misc
import robot.relay
import robot.valves
import misc.constants
import logging.config

def temperature_fermenter():
    tempfile = open("/sys/bus/w1/devices/28-0416362bc6ff/w1_slave")
    thetext = tempfile.read()
    tempfile.close()
    tempdata = thetext.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:])
    temperature = temperature / 1000
    return temperature

def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
      f = open('/proc/cpuinfo','r')
      for line in f:
        if line[0:6]=='Serial':
          cpuserial = line[10:26]
      f.close()
    except:
      cpuserial = "ERROR000000000"

    return cpuserial



def main():
    import logging.config
    logging.config.fileConfig('')
    # program code    






##############################
## debut du programme initial
##
##
##############################
robot.relay.setup_relays()


while 1:
    temp = temperature_fermenter();
    print (temp);

    #if temp < 28:
    #test_relay();
    serial = getserial();
    print(serial);

    robot.valves.open_3valve()
    robot.valves.close_3valve()
    
robot.relay.cleanup_relays()

    
