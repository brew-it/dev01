import re
import os
import data.config

import logging
logger = logging.getLogger(__name__)



def GetTempProbeFilename():
    try:
        for filename in os.listdir('/sys/bus/w1/devices/'):
            if re.match('28-*', filename):
                return filename
    except IOError:
            raise IOError


def GetFermenterTemperature():
    logging.debug("entering GetFermenterTemperature function")
    try:
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

    except:
        return -1

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


def GetBatchId():
    try:
        cur_batchid= data.config.GetConfig('batchinfo','batchid')
        return cur_batchid
    except:
        return "-1"

