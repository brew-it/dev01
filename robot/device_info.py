import re
import os
import logging
logger = logging.getLogger(__name__)



def GetTempProbeFilename():
    for filename in os.listdir('/sys/bus/w1/devices/'):
        if re.match('28-*', filename):
            return filename
       
    return "PROBENOTFOUND"


def GetFermenterTemperature():
    probe_filename = "/sys/bus/w1/devices/" + GetTempProbeFilename() + "/w1_slave"
    logging.debug("file used for temp probe: " + probe_filename)

    probe_file = open(probe_filename)
    thetext = probe_file.read()
    probe_file.close()
    tempdata = thetext.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:])
    temperature = temperature / 1000
    logging.info ("fermenting temperature: " + str(temperature));

    return temperature

def GetDeviceID():
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

    logging.info ("ID of the device: " + str(cpuserial));
    return cpuserial
