# Send gamepad/joystick actions to Scratch via Scratch-RSP

import pygame
import scratchRSP
import time
import sys
import struct
import unicodedata
from decimal import Decimal, ROUND_HALF_UP

# Possible joystick actions
JOYSTICK_ACTIONS = (
    pygame.JOYAXISMOTION,
    pygame.JOYBUTTONDOWN,
    pygame.JOYBUTTONUP,
    pygame.JOYHATMOTION
)


def send_joystick(scratch, event):
    """
    Receive events of joystick actions and send 'broadcast'
    or 'sensor-update' messages to Scratch.
    """
    if event.type == pygame.JOYBUTTONDOWN:
        sensor_name = str(event.joy) \
                      + "_Button_{:0>2}".format(str(event.button))
        scratch.broadcast(sensor_name + "_on")
        sensor_value = "True"
        return scratch.sensor_update(sensor_name, sensor_value)
    if event.type == pygame.JOYBUTTONUP:
        sensor_name = str(event.joy) \
                      + "_Button_{:0>2}".format(str(event.button))
        scratch.broadcast(sensor_name + "_off")
        sensor_value = "False"
        return scratch.sensor_update(sensor_name, sensor_value)
    if event.type == pygame.JOYAXISMOTION:
        sensor_name = str(event.joy) + "_" + "Axis_" + str(event.axis)
        sensor_value = axis_value(event.value)
        return scratch.sensor_update(sensor_name, sensor_value)
    if event.type == pygame.JOYHATMOTION:
        msg = str(event.joy) + "_" + "Hat_" + str(event.value)
        scratch.broadcast(msg)
        hat_x, hat_y = event.value
        hat_x = str(hat_x)
        hat_y = str(hat_y)
        sensor_name = str(event.joy) + "_" + "Hat_X"
        sensor_value = hat_x
        scratch.sensor_update(sensor_name, sensor_value)
        sensor_name = str(event.joy) + "_" + "Hat_Y"
        sensor_value = hat_y
        return scratch.sensor_update(sensor_name, sensor_value)


def axis_value(value):
    """ Normalize values from analog stick  """
    if value > 0.995:
        value = 1.0
    elif 0.005 > value > -0.005:
        value = 0.0
    elif value < -0.995:
        value = -1.0
    value *= 100.0
    value = Decimal(str(value)).quantize(Decimal('0.01'),
                                         rounding=ROUND_HALF_UP)
    return str(value)
