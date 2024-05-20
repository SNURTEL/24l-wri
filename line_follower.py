#!/usr/bin/env python3

import sys
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_D

from ev3dev2.sensor import INPUT_1, INPUT_3, INPUT_4
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
WHITE = "White"
BLUE = "Blue"

TURN_ITER_BLOCK = 10
TICK_SINCE_FIRST = 10

def main():

    motor_right = LargeMotor(OUTPUT_D)
    motor_left = LargeMotor(OUTPUT_A)

    sensor_right = ColorSensor(INPUT_4)
    sensor_left = ColorSensor(INPUT_1)

    button = TouchSensor(INPUT_3)

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
    tick_since_first_seen_red = TICK_SINCE_FIRST
    tick_since_first_seen_green = TICK_SINCE_FIRST
    has_seen_red = False
    has_seen_green = False

    main_color = BLACK

    def reset():
        nonlocal speed_base, speed_left, speed_right, backwards_factor_base, backwards_factor_color, backwards_factor, slow_speed, movement_state, previous_movement_state
        nonlocal turn_iter_counter, tick_since_first_seen_red, tick_since_first_seen_green, has_seen_red, has_seen_green, main_color, left_color, right_color
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
        tick_since_first_seen_red = TICK_SINCE_FIRST
        tick_since_first_seen_green = TICK_SINCE_FIRST
        has_seen_red = False
        has_seen_green = False

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
        nonlocal has_seen_red, has_seen_green
        nonlocal tick_since_first_seen_red, tick_since_first_seen_green

        turn_iter_counter = max(0, turn_iter_counter - 1)

        if has_seen_green:
            tick_since_first_seen_green = max(0, tick_since_first_seen_green - 1)
        elif has_seen_red:
            tick_since_first_seen_red = max(0, tick_since_first_seen_red - 1)

        if tick_since_first_seen_red == 0 and left_color == RED and right_color == RED:
            red_sequence()
            tick_since_first_seen_red = float('inf')
        elif tick_since_first_seen_green == 0 and left_color == GREEN and right_color == GREEN:
            green_sequence()
            tick_since_first_seen_green = float('inf')

        if (left_color == GREEN or right_color == GREEN) and has_seen_red and not has_seen_green: #and has_seen_green:
            has_seen_green = True
            turn_iter_counter = TURN_ITER_BLOCK
            turn_factor = 1 if left_color == GREEN and right_color != GREEN else -1
            sleep(15 / speed_base)
            motor_left.on(-turn_factor * 40)
            motor_right.on(turn_factor * 40)
            sleep(0.9)
            motor_left.on(speed_left)
            motor_right.on(speed_right)

        elif (left_color == RED or right_color == RED) and not has_seen_red:
            has_seen_red = True
            turn_iter_counter = TURN_ITER_BLOCK
            turn_factor = 1 if left_color == RED and right_color != RED else -1
            sleep(15 / speed_base)
            motor_left.on(-turn_factor * 40)
            motor_right.on(turn_factor * 40)
            sleep(0.9)
            motor_left.on(speed_left)
            motor_right.on(speed_right)

        elif turn_iter_counter == 0:
        # else:
            main_color = BLACK
            backwards_factor = backwards_factor_base

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
        sleep(30 / speed_base)
        motor_left.on(40)
        motor_right.on(-40)
        sleep(1.75)
        motor_left.on(speed_base)
        motor_right.on(speed_base)
        sleep(15 / speed_base)

    def get_current_color(sensor, calibrated):
        counter = 0
        prev_color = "NoColor"
        while True:
            color = get_current_color_calibrated(sensor) if calibrated else sensor.color_name
            # print("RGB: " + str(sensor.rgb) + " HSV: " + str(sensor.hsv) + " name: " + color)

            if color == GREEN:
                counter = min(1, counter + 1)
            else:
                counter = max(0, counter - 1)

            # print("Generator color: " + color + ", counter: " + str(counter))                    

            if color == GREEN:
                if counter == 1:
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
        
        #print("[SENSOR RIGHT] RGB: " + str(sensor.rgb) + " HSV: " + str(sensor.hsv) + " name: " + color)
        return color

    

    def get_current_color_simple(sensor):
        while True:
            yield sensor.color


    try:
        print("Robot initialized")
        
        left_generator = get_current_color(sensor_left, False)
        right_generator = get_current_color(sensor_right, True)

        while True:
            if button.is_pressed:
                reset()
                continue

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
