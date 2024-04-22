#!/usr/bin/env python3

import sys
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_D

from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor

P = float(sys.argv[2])
P_BACKWARDS = .6


def main():

    motor_right = LargeMotor(OUTPUT_D)
    motor_left = LargeMotor(OUTPUT_A)

    sensor_right = ColorSensor(INPUT_4)
    sensor_left = ColorSensor(INPUT_1)

    speed_base = -float(sys.argv[1])
    speed_left = speed_base
    speed_right = speed_base
    backwards_factor = float(sys.argv[3])
    slow_speed = -float(sys.argv[4])

    prev_left = sensor_left.color_name
    prev_right = sensor_right.color_name

    black_color = "Black"

    def set_speed_left(new_speed, p=P):
        nonlocal speed_left
        speed_left = new_speed * p + (1 - p) * speed_left

    def set_speed_right(new_speed, p=P):
        nonlocal speed_right
        speed_right = new_speed * p + (1 - p) * speed_right

    try:
        print("Robot initialized")

        while True:
            if (
                sensor_left.color_name == black_color
                and sensor_right.color_name != black_color
            ):
                set_speed_left(-backwards_factor * slow_speed)
                set_speed_right(slow_speed)
            elif (
                sensor_right.color_name == black_color
                and sensor_left.color_name != black_color
            ):
                set_speed_right(-backwards_factor * slow_speed)
                set_speed_left(slow_speed)
            elif (sensor_left.color_name == black_color and sensor_right.color_name == black_color and prev_left == black_color and prev_right != black_color):
                set_speed_left(-backwards_factor * slow_speed)
                set_speed_right(slow_speed)
            elif (sensor_left.color_name == black_color and sensor_right.color_name == black_color and prev_left != black_color and prev_right == black_color):
                set_speed_right(-backwards_factor * slow_speed)
                set_speed_left(slow_speed)
            elif (
                sensor_left.color_name != black_color
                and sensor_right.color_name != black_color
            ):
                set_speed_left(speed_base)
                set_speed_right(speed_base)

            motor_left.on(speed_left)
            motor_right.on(speed_right)

            prev_left = sensor_left.color_name
            prev_right = sensor_right.color_name

            # print("Speed left: " + str(speed_left))
            # print("Speed right: " + str(speed_right))
    finally:
        motor_left.off()
        motor_right.off()


if __name__ == "__main__":
    main()
