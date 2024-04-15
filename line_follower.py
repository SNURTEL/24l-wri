#!/usr/bin/env python3

from time import sleep
import sys
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D

from ev3dev2.sensor import INPUT_1, INPUT_2,INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor

def main():
    motor_right = LargeMotor(OUTPUT_A)
    motor_left = LargeMotor(OUTPUT_D)

    sensor_right = ColorSensor(INPUT_1)
    sensor_left = ColorSensor(INPUT_4)

    interval = 1 / 50.0
    speed_base = float(sys.argv[1])
    speed_left = speed_base
    speed_right = speed_base
    speed_delta = speed_base * .5
    max_speed = 2.5 * speed_base
    black_color = "Black"

    previous_left = 0
    previous_right = 0

    try:
        print("Robot initialized")

        while True:

            # motor_left.on(speed_base)
            # motor_right.on(speed_base)
        
            if sensor_left.color_name == black_color:
                speed_left = -speed_base
            elif sensor_right.color_name == black_color: 
                speed_right = -speed_base
            else:
                speed_left = speed_base
                speed_right = speed_base

            # speed_left = max(-max_speed, min(max_speed, speed_left))
            # speed_right = max(-max_speed, min(max_speed, speed_right))

            motor_left.on(speed_left)
            motor_right.on(speed_right)

            # print('Color 1 ' + str(sensor_left.rgb) + ' detected as ' + str(sensor_left.color_name) + '.')
            # print('Color 2 ' + str(sensor_right.rgb) + ' detected as ' + str(sensor_right.color_name) + '.')
            print("Speed left: " + str(speed_left))
            print("Speed right: " + str(speed_right))
            #sleep(interval)

    finally:
        motor_left.off()
        motor_right.off()


if __name__ == "__main__":
    main()

