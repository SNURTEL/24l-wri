#!/usr/bin/env python3

import sys
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_D

from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from time import sleep

P = float(sys.argv[2])
P_BACKWARDS = .6

DEFAULT = 0
LEFT_TURN = 1
RIGHT_TURN = 2

BLACK = "Black"
RED = "Red"
GREEN = "Green"

TURN_ITER_BLOCK = 10
TICK_SINCE_FIRST = 10

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
    backwards_factor_base = float(sys.argv[3])
    backwards_factor_color = backwards_factor_base * 1.5
    backwards_factor = backwards_factor_base
    slow_speed = float(sys.argv[4])

    movement_state = DEFAULT
    previous_movement_state = None

    turn_iter_counter = 0
    tick_since_first_seen_green = TICK_SINCE_FIRST
    tick_since_first_seen_red = TICK_SINCE_FIRST
    has_seen_green = False
    has_seen_red = False 

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
        nonlocal backwards_factor, backwards_factor_color, backwards_factor_base
        nonlocal turn_iter_counter
        nonlocal has_seen_green, has_seen_red
        nonlocal tick_since_first_seen_green, tick_since_first_seen_red

        turn_iter_counter = max(0, turn_iter_counter - 1)

        # if has_seen_green:
        #     tick_since_first_seen_green = max(0, tick_since_first_seen_green - 1)
        # elif has_seen_red:
        #     tick_since_first_seen_red = max(0, tick_since_first_seen_red - 1)

        # if tick_since_first_seen_green == 0 and sensor_left.color_name == GREEN and sensor_right.color_name == GREEN:
        #     green_sequence()
        #     tick_since_first_seen_green = float('inf')
        # elif tick_since_first_seen_red == 0 and sensor_left.color_name == RED and sensor_right.color_name == RED:
        #     red_sequence()
        #     tick_since_first_seen_red = float('inf')

        if (left_color == RED or right_color == RED): #and has_seen_green:
            #has_seen_red = True
            turn_iter_counter = TURN_ITER_BLOCK
            main_color = RED
            #backwards_factor = backwards_factor_color
        elif left_color == GREEN or right_color == GREEN:
            #has_seen_green = True
            turn_iter_counter = TURN_ITER_BLOCK
            main_color = GREEN
            #backwards_factor = backwards_factor_color
        elif turn_iter_counter == 0:
        # else:
            main_color = BLACK
            #backwards_factor = backwards_factor_base

    def green_sequence():
        motor_left.on(speed_base)
        motor_right.on(-speed_base)
        sleep(9999)

    def red_sequence():
        motor_left.on(0)
        motor_right.on(speed_base)
        sleep(9999)

    def get_current_color(sensor):
        counter = 0
        prev_color = "NoColor"
        while True:
            color = sensor.color_name
            if color == GREEN:
                counter = min(2, counter + 1)
            else:
                counter = max(0, counter - 1)

            # print("Generator color: " + color + ", counter: " + str(counter))                    

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



    try:
        print("Robot initialized")

        left_generator = get_current_color(sensor_left)
        right_generator = get_current_color(sensor_right)

        while True:
            left_color = next(left_generator)
            right_color = next(right_generator)

            init_state()

            if (
                left_color == main_color
                and right_color != main_color #and previous_movement_state != RIGHT_TURN
            ):
                set_speed_left(-backwards_factor * slow_speed)
                set_speed_right(slow_speed)
                set_movement_state(LEFT_TURN)
            elif (
                right_color == main_color
                and left_color != main_color #and previous_movement_state != LEFT_TURN
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
            
            motor_left.on(speed_left)
            motor_right.on(speed_right)

            # print("Color left: " + left_color + ", color right: " + right_color + ", main color: " + main_color)
    finally:
        motor_left.off()
        motor_right.off()


if __name__ == "__main__":
    main()
