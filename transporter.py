#!/usr/bin/env python3

import sys
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D

from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from time import sleep


P = float(sys.argv[2])

DEFAULT = 0
LEFT_TURN = 1
RIGHT_TURN = 2

BLACK = "Black"
RED = "Red"
GREEN = "Green"
WHITE = "White"
BLUE = "Blue"


def main():

    motor_right = LargeMotor(OUTPUT_D)
    motor_left = LargeMotor(OUTPUT_A)

    sensor_right = ColorSensor(INPUT_4)
    sensor_left = ColorSensor(INPUT_1)

    left_color = None
    right_color = None

    speed_base = float(sys.argv[1])
    speed_left = speed_base
    speed_right = speed_base
    backwards_factor = float(sys.argv[3])
    slow_speed = float(sys.argv[4])

    movement_state = DEFAULT
    previous_movement_state = None

    main_color = BLACK

    def set_speed_left(new_speed, p=P):
        nonlocal speed_left
        speed_left = new_speed * p + (1 - p) * speed_left

    def set_speed_right(new_speed, p=P):
        nonlocal speed_right
        speed_right = new_speed * p + (1 - p) * speed_right

    def set_movement_state(state):
        nonlocal previous_movement_state
        nonlocal movement_state
        previous_movement_state = movement_state
        movement_state = state

    def init_state():
        nonlocal main_color
        nonlocal left_color, right_color
        nonlocal backwards_factor

        if (left_color == GREEN or right_color == GREEN):
            sleep(15 / speed_base)
            motor_left.on(-40)
            motor_right.on(40)
            sleep(0.85)
            motor_left.on(speed_left)
            motor_right.on(speed_right)
            green_sequence()

        elif (left_color == RED or right_color == RED):
            sleep(15 / speed_base)
            motor_left.on(40)
            motor_right.on(-40)
            sleep(0.875)
            motor_left.on(speed_left)
            motor_right.on(speed_right)
            red_sequence()

    def green_sequence():
        nonlocal motor_left, motor_right
        print('Entering green sequence...')
        motor_left.on(speed_base)
        motor_right.on(speed_base)
        sleep(30 / speed_base)
        motor_left.on(-speed_base)
        motor_right.on(-speed_base)
        sleep(60 / speed_base)
        motor_left.off()
        motor_right.off()
        exit()

    def red_sequence():
        nonlocal motor_left, motor_right
        print('Entering red sequence...')
        motor_left.on(speed_base)
        motor_right.on(speed_base)
        sleep(80 / speed_base)
        motor_left.on(20)
        motor_right.on(-20)
        sleep(3.5)
        motor_left.on(speed_base)
        motor_right.on(speed_base)
        sleep(77.5 / speed_base)
        motor_left.on(40)
        motor_right.on(-40)
        sleep(0.85)
        motor_left.on(speed_left)
        motor_right.on(speed_right)

    def get_current_color(sensor, calibrated):
        counter = 0
        prev_color = "NoColor"
        while True:
            color = get_current_color_calibrated(sensor) if calibrated else sensor.color_name

            if color == GREEN:
                counter = min(2, counter + 1)
            else:
                counter = max(0, counter - 1)

            if color == GREEN:
                if counter == 2:
                    prev_color = GREEN
                    yield GREEN
                else:
                    yield prev_color
            else:
                if prev_color == GREEN and counter > 0:
                    yield GREEN
                else:
                    prev_color = color
                    yield color

    
    def get_current_color_calibrated(sensor):
        hsv = sensor.hsv

        if abs(hsv[0] - 0.4) < 0.2 and hsv[1] > 0.55 and hsv[2] > 35:
            color = GREEN
        elif abs(min(hsv[0], 1-hsv[0])) < 0.2 and hsv[1] > 0.55 and hsv[2] > 35:
            color = RED
        elif hsv[2] <= 150:
            color = BLACK
        else:
            color = WHITE

        return color

    try:
        print("Robot initialized")
        
        left_generator = get_current_color(sensor_left, False)
        right_generator = get_current_color(sensor_right, True)

        while True:
            left_color = next(left_generator)
            right_color = next(right_generator)

            init_state()

            if (
                left_color == main_color
                and right_color != main_color and previous_movement_state != RIGHT_TURN
            ):
                set_speed_left(-backwards_factor * slow_speed)
                set_speed_right(slow_speed)
                set_movement_state(LEFT_TURN)
            elif (
                right_color == main_color
                and left_color != main_color and previous_movement_state != LEFT_TURN
            ):
                set_speed_right(-backwards_factor * slow_speed)
                set_speed_left(slow_speed)
                set_movement_state(RIGHT_TURN)
            elif (
                left_color != main_color
                and right_color != main_color
            ):
                set_speed_left(speed_base)
                set_speed_right(speed_base)
                set_movement_state(DEFAULT)
            else:
                if previous_movement_state == DEFAULT:
                    set_speed_left(speed_base)
                    set_speed_right(speed_base)

                set_movement_state(DEFAULT)
            
            motor_left.on(speed_left)
            motor_right.on(speed_right)

    finally:
        motor_left.off()
        motor_right.off()


if __name__ == "__main__":
    main()
