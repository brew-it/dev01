import configparser
import misc.constants

def GetConfig(section, item):
    try:
        config = configparser.RawConfigParser()
        config.read('brewit.cfg')
        return config.get(section, item)
    except IOError:
        return robot.states.STATE_IDLE

def ConfigExists(section, item):
    try:
        config = configparser.RawConfigParser()
        config.read('brewit.cfg')
        return config.has_option(section, item)
    except IOError:
        return False

def RemoveConfig(section, item):
    try:
        config = configparser.RawConfigParser()
        config.read('brewit.cfg')
        if(config.has_section(section)):
            config.remove_option(section, item)

        with open('brewit.cfg','w+') as configfile:
            config.write(configfile)

    except IOError:
        return robot.states.STATE_IDLE
    
    
def SetConfig(section, item, value):
    try:
        config = configparser.RawConfigParser()
        config.read('brewit.cfg')
        if(not config.has_section(section)):
            config.add_section(section)

        config.set(section, item, value)

        with open('brewit.cfg','w+') as configfile:
            config.write(configfile)

    except IOError:
        return robot.states.STATE_IDLE

    
def GetApiUrl():
    if(GetConfig('DEVICE', 'DEVICE_ENVIRONMENT') == 'test'):
           return misc.constants.API_URL_TEST
    else:
           return misc.constants.API_URL_PROD
       
