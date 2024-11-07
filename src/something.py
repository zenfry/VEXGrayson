from vex import *

# Initialize Brain, Inertial, Controller, and Motors
Brain = Brain()
Controller = Controller()

# Motor setup for the left and right sides
motor_left1 = Motor(Ports.PORT1)
motor_left2 = Motor(Ports.PORT2)
motor_left3 = Motor(Ports.PORT3)

motor_right1 = Motor(Ports.PORT4, True)  # Reverse polarity for right side
motor_right2 = Motor(Ports.PORT5, True)
motor_right3 = Motor(Ports.PORT6, True)

# Motor setup for the arm
motor_arm = Motor(Ports.PORT7)  # Port 7, or any available port for the arm

# Competition instance

# Sample variable to demonstrate button actions
myVariable = 0

# Function for button events
def button_actions():
    global myVariable

    # Button A - Example action
    if Controller.buttonA.pressing():
        myVariable += 1
        Brain.screen.print("Button A pressed: {}".format(myVariable))

    # Button B - Example action
    if Controller.buttonB.pressing():
        myVariable -= 1
        Brain.screen.print("Button B pressed: {}".format(myVariable))

    # Button X - Example action
    if Controller.buttonX.pressing():
        Brain.screen.print("Button X pressed")

    # Button Y - Example action
    if Controller.buttonY.pressing():
        Brain.screen.print("Button Y pressed")

    # Left Shoulder Button (L1) - Example action
    if Controller.buttonL1.pressing():
        Brain.screen.print("L1 pressed")

    # Left Shoulder Button (L2) - Example action
    if Controller.buttonL2.pressing():
        Brain.screen.print("L2 pressed")

    # Right Shoulder Button (R1) - Example action
    if Controller.buttonR1.pressing():
        Brain.screen.print("R1 pressed")

    # Right Shoulder Button (R2) - Example action
    if Controller.buttonR2.pressing():
        Brain.screen.print("R2 pressed")

# Function for controlling the robot wheels using joystick
def drive_control():
    # Left side uses Axis3 (left vertical stick)
    left_speed = Controller.axis3.position()
    
    # Right side uses Axis2 (right vertical stick)
    right_speed = Controller.axis2.position()
    
    # Set motor velocities
    motor_left1.spin(FORWARD, left_speed, PERCENT)
    motor_left2.spin(FORWARD, left_speed, PERCENT)
    motor_left3.spin(FORWARD, left_speed, PERCENT)

    motor_right1.spin(FORWARD, right_speed, PERCENT)
    motor_right2.spin(FORWARD, right_speed, PERCENT)
    motor_right3.spin(FORWARD, right_speed, PERCENT)

# Function for controlling the arm using joystick
def arm_control():
    # Use Axis4 (right horizontal stick) for arm control
    arm_speed = Controller.axis4.position()
    
    # Set arm motor velocity based on joystick position
    motor_arm.spin(FORWARD, arm_speed, PERCENT)

# Autonomous task function (to be planned)
def autonomous():
    while competition.is_autonomous() and competition.is_enabled():
        wait(10, MSEC)

# Driver control task function
def driver_control():
    while competition.is_driver_control() and competition.is_enabled():
        drive_control()   # Use joystick to drive the wheels
        arm_control()     # Use joystick to control the arm
        button_actions()  # Handle button presses
        wait(20, MSEC)

competition = Competition(driver_control,autonomous)