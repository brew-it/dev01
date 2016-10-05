import RPi.GPIO as GPIO
import logging
import time
logger = logging.getLogger(__name__)


DELAY_CLOSING_THREEWAYVALVE = 8
RELAY1 = 17;
RELAY2 = 10;
RELAY3 = 9;
RELAY4 = 5;
RELAY5 = 6;
RELAY6 = 13;
RELAY7 = 19;
RELAY8 = 26;

RELAY9 = 7;
RELAY10 = 20;
RELAY11 = 16;
RELAY12 = 12;
RELAY13 = 25;
RELAY14 = 18;
RELAY15 = 15;
RELAY16 = 14;

relays = [RELAY1, RELAY2, RELAY3, RELAY4, RELAY5, RELAY6, RELAY7, RELAY8, RELAY9, RELAY10, RELAY11, RELAY12, RELAY13, RELAY14, RELAY15, RELAY16]
relays18 = [RELAY1, RELAY2, RELAY3, RELAY4, RELAY5, RELAY6, RELAY7, RELAY8];
relays916 = [RELAY9, RELAY10, RELAY11, RELAY12, RELAY13, RELAY14, RELAY15, RELAY16];


def test_relay():
    time = 10;
    while i     < 1000:
        for relay in relays:
            GPIO.output(relay,GPIO.HIGH)
        time.sleep(time)
        logging.debug('open')


        for relay in relays:
            GPIO.output(relay,GPIO.LOW)
        sleep(time/2)
        logging.debug('closed')


def cleanup_relays():    
    GPIO.cleanup()

def setup_relays():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    i = 0

    for relay in relays:
        GPIO.setup(relay, GPIO.OUT, initial=GPIO.LOW)
