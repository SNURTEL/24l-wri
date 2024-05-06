#!/usr/bin/env python3

import sys
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_D

from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor

P = float(sys.argv[2])
P_BACKWARDS = .6

DEFAULT = 0
LEFT_TURN = 1
RIGHT_TURN = 2

BLACK = "Black"
RED = "Red"
GREEN = "Green"


def main():

    motor_right = LargeMotor(OUTPUT_D)
    motor_left = LargeMotor(OUTPUT_A)

    sensor_right = ColorSensor(INPUT_4)
    sensor_left = ColorSensor(INPUT_1)

    speed_base = float(sys.argv[1])
    speed_left = speed_base
    speed_right = speed_base
    backwards_factor_base = float(sys.argv[3])
    backwards_factor_color = backwards_factor_base * 1.5
    backwards_factor = backwards_factor_base
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

    def update_main_color():
        nonlocal main_color
        nonlocal sensor_left
        nonlocal sensor_right
        nonlocal backwards_factor, backwards_factor_color, backwards_factor_base

        if sensor_left.color_name == RED or sensor_right.color_name == RED:
            main_color = RED
            backwards_factor = backwards_factor_color
        elif sensor_left.color_name == GREEN or sensor_right.color_name == GREEN:
            main_color = GREEN
            backwards_factor = backwards_factor_color
        else:
            main_color = BLACK
            backwards_factor = backwards_factor_base

    try:
        print("Robot initialized")

        while True:
            update_main_color()

            if (
                sensor_left.color_name == main_color
                and sensor_right.color_name != main_color and previous_movement_state != RIGHT_TURN
            ):
                set_speed_left(-backwards_factor * slow_speed)
                set_speed_right(slow_speed)
                set_movement_state(LEFT_TURN)
            elif (
                sensor_right.color_name == main_color
                and sensor_left.color_name != main_color and previous_movement_state != LEFT_TURN
            ):
                set_speed_right(-backwards_factor * slow_speed)
                set_speed_left(slow_speed)
                set_movement_state(RIGHT_TURN)
            elif (
                sensor_left.color_name != main_color
                and sensor_right.color_name != main_color
            ):
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
