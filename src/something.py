from vex import *
import math

# Initialize Brain, Controller, Competition, and Motors
brain = Brain()
controller = Controller()

# Motor setup
motor_left1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor_left2 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
motor_right1 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
motor_right2 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
motor_arm = Motor(Ports.PORT6, GearSetting.RATIO_6_1)  # Gear ratio added
left_group = MotorGroup(motor_left1, motor_left2)
right_group = MotorGroup(motor_right1, motor_right2)

AUTO_SPEED = 20  # Default speed for autonomous driving


def driving(input_speed, input_turn):
    left = input_speed + input_turn
    right = input_speed - input_turn
    return left, right


def driver():
    while True:
        input_speed = controller.axis3.position()  # Forward/backward
        input_turn = controller.axis1.position()  # Left/right turning
        left_speed, right_speed = driving(input_speed, input_turn)
        left_group.spin(FORWARD, left_speed, PERCENT)
        right_group.spin(FORWARD, right_speed, PERCENT)
        wait(10, MSEC)  # Prevent overloading the loop


def time_drive(time, direction):
    left_group.spin(direction, AUTO_SPEED, PERCENT)
    right_group.spin(direction, AUTO_SPEED, PERCENT)
    wait(time, MSEC)
    left_group.stop()
    right_group.stop()


def arm_control():
    controller.buttonL1.pressed(lambda: motor_arm.spin(FORWARD, 50, PERCENT))
    controller.buttonL2.pressed(lambda: motor_arm.spin(REVERSE, 50, PERCENT))
    controller.buttonL1.released(lambda: motor_arm.stop(HOLD))
    controller.buttonL2.released(lambda: motor_arm.stop(HOLD))


def driver_control():
    while competition.is_driver_control() and competition.is_enabled():
        display_kill_mode() 
        driver()


def autonomous():
    display_kill_mode()
    time_drive(2000, FORWARD)  # Example autonomous logic

def display_kill_mode():
    brain.screen.clear_screen()
    brain.screen.set_pen_color(Color.RED)
    brain.screen.set_pen_width(5)
    brain.screen.set_font(FontType.MONO15)
    text = "BATTLE MODE"
    
    # Calculate position for centering the text
    screen_width = 480 
    screen_height = 240  
    text_width = len(text) * 10  
    text_height = 20  # Approximate text height in pixels

    x_position = (screen_width - text_width) // 2
    y_position = (screen_height - text_height) // 2

    # Print the text at the calculated position
    brain.screen.set_cursor(1, 1)  # Reset cursor to avoid issues
    brain.screen.print(x_position, y_position, text)


# Initialize Competition
competition = Competition(driver_control, autonomous)

# Bind controller events
arm_control()
