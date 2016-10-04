import RPi.GPIO as GPIO
import robot.relay
import time

import logging
logger = logging.getLogger(__name__)


def open_3valve():
            GPIO.output(robot.relay.RELAY2,GPIO.HIGH)
            GPIO.output(robot.relay.RELAY3,GPIO.LOW)
            logging.debug("valve opening")
            time.sleep(robot.relay.DELAY_CLOSING_THREEWAYVALVE)
            GPIO.output(robot.relay.RELAY2,GPIO.HIGH)
            GPIO.output(robot.relay.RELAY3,GPIO.HIGH)
            logging.debug("valve opened")

            
def close_3valve():
            GPIO.output(robot.relay.RELAY2,GPIO.LOW)
            GPIO.output(robot.relay.RELAY3,GPIO.LOW)
            logging.debug("valve closing")
            time.sleep(robot.relay.DELAY_CLOSING_THREEWAYVALVE)
            GPIO.output(robot.relay.RELAY2,GPIO.HIGH)
            GPIO.output(robot.relay.RELAY3,GPIO.HIGH)
            logging.debug("valve closed")
