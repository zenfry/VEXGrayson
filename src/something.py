from vex import *

# Initialize Brain, Controller, Competition, and Motors
brain = Brain()
controller = Controller()

# Motor setup
motor_left1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1)
motor_left2 = Motor(Ports.PORT9, GearSetting.RATIO_18_1)
motor_right1 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True )
motor_right2 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
motor_arm = Motor(Ports.PORT6, GearSetting.RATIO_18_1)

# Function to drive forward
def drive_forward(speed, duration):
    motor_left1.spin(FORWARD, speed, PERCENT)
    motor_left2.spin(FORWARD, speed, PERCENT)
    motor_right1.spin(FORWARD, speed, PERCENT)
    motor_right2.spin(FORWARD, speed, PERCENT)
    wait(duration, SECONDS)
    motor_left1.stop() 
    motor_left2.stop()
    motor_right1.stop()
    motor_right2.stop()

# Function to turn
def turn(direction, speed, duration):
    if direction == "left":
        motor_left1.spin(REVERSE, speed, PERCENT)
        motor_left2.spin(REVERSE, speed, PERCENT)
        motor_right1.spin(FORWARD, speed, PERCENT)
        motor_right2.spin(FORWARD, speed, PERCENT)
    elif direction == "right":
        motor_left1.spin(FORWARD, speed, PERCENT)
        motor_left2.spin(FORWARD, speed, PERCENT)
        motor_right1.spin(REVERSE, speed, PERCENT)
        motor_right2.spin(REVERSE, speed, PERCENT)
    wait(duration, SECONDS)
    motor_left1.stop()
    motor_left2.stop()
    motor_right1.stop()
    motor_right2.stop()

# Arm control
def move_arm(position, speed, duration):
    if controller.buttonR1.pressed() == "up":
        motor_arm.spin(FORWARD, speed, PERCENT)
    elif controller.buttonL1.pressed() == "down":
        motor_arm.spin(REVERSE, speed, PERCENT)
    wait(duration, SECONDS)
    motor_arm.stop()

# Joystick drive control
def drive_control():
    left_speed = controller.axis3.position()
    right_speed = controller.axis2.position()
    motor_left1.spin(FORWARD, left_speed, PERCENT)
    motor_left2.spin(FORWARD, left_speed, PERCENT)
    motor_right1.spin(FORWARD, right_speed, PERCENT)
    motor_right2.spin(FORWARD, right_speed, PERCENT)

# Arm joystick control
def arm_control():
    arm_speed = controller.buttonR1.pressed()
    motor_arm.spin(FORWARD, arm_speed, PERCENT)
    
    arm_speed = controller.buttonL1.pressed()
    motor_arm.spin(REVERSE, arm_speed, PERCENT)

# Autonomous routine
def autonomous():
    drive_forward(60, 1)
    move_arm("up", 50, 1)
    drive_forward(50, 1.5)
    move_arm("down", 50, 1)
    turn("left", 50, 0.7)
    drive_forward(50, 1)
    move_arm("up", 50, 1)
    drive_forward(50, 1.5)
    move_arm("down", 50, 1)
    drive_forward(-50, 1)

# Driver control loop
def driver_control():
    while competition.is_driver_control() and competition.is_enabled():
        drive_control()
        arm_control()
        wait(10, MSEC)

# Run competition
competition = Competition(driver_control, autonomous)
