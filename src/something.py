from vex import *

# Initialize Brain, Controller, Competition, and Motors
brain = Brain()
controller = Controller()

# Motor setup
motor_left1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor_left2 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
motor_right1 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
motor_right2 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
motor_arm = Motor(Ports.PORT6)  # No gear ratio specified
drive_motors = {"motor_left1": left_1, "motor_left2": left_2, "motor_right1": right_1,
                "motor_right2": right_2}
left_group = MotorGroup(left_1, left_2)
right_group = MotorGroup(right_1, right_2)

AUTO_SPEED = 20  # Default speed for autonomous driving



def driving(input_speed, input_turn):
 # Calculate left and right motor speeds for arcade drive.
    left = input_speed + input_turn
    right = input_speed - input_turn
    return left, right


def driver():
# Manual control using controller axes.
    while True:
        input_speed = cal(control.axis3.position())  # Forward/backward
        input_turn = cal(control.axis1.position())     # Left/right turning
        left_speed, right_speed = driving(input_speed, input_turn)
        left_group.spin(FORWARD, left_speed, PERCENT)
        right_group.spin(FORWARD, right_speed, PERCENT)


def time_drive(time, direction):
  #Drive forward or reverse for a set time in autonomous.
    left_group.spin(direction, AUTO_SPEED, PERCENT)
    right_group.spin(direction, AUTO_SPEED, PERCENT)
    wait(time, MSEC)
    left_group.stop()
    right_group.stop()


def drive_set():
    left_group.spin(FORWARD, AUTO_SPEED, PERCENT)
    right_group.spin(FORWARD, AUTO_SPEED, PERCENT)


# Arm control
def arm_control():
    control.buttonL1.pressed(lambda: motor_arm.spin(FORWARD, 50, PERCENT))
    control.buttonL2.pressed(lambda: motor_arm.spin(REVERSE, 50, PERCENT))
    control.buttonL1.released(motor_arm.stop)
    control.buttonL2.released(motor_arm.stop)


# Driver control loop
def driver_control():
    while competition.is_driver_control() and competition.is_enabled():
        drive_control()
        wait(10, MSEC)
        
arm_control()

competition = Competition(driver_control, autonomous)
