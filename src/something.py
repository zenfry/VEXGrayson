from vex import *

# Initialize Brain, Controller, and Motors
Brain = Brain()
Controller = Controller()

# Motor setup for the left and right sides
motor_left1 = Motor(Ports.PORT1, True)   # Clockwise
motor_left2 = Motor(Ports.PORT2, True)   # Clockwise
motor_right1 = Motor(Ports.PORT9)        # Counterclockwise
motor_right2 = Motor(Ports.PORT10)       # Counterclockwise

# Motor setup for the arm
motor_arm = Motor(Ports.PORT7)           # Controls arm up/down

# Speed variable for the wheels
wheel_speed = 50  # Start with an initial speed of 50%
autonomous_mode = False  # Tracks if the robot is in autonomous mode

# Function to adjust wheel speed based on button presses
def adjust_speed():
    global wheel_speed
    
    # Increase speed with L1, capped at 100%
    if Controller.buttonL1.pressing():
        wheel_speed = min(100, wheel_speed + 5)
        Brain.screen.print("Speed increased to: {}".format(wheel_speed))
    
    # Decrease speed with L2, capped at 0%
    if Controller.buttonL2.pressing():
        wheel_speed = max(0, wheel_speed - 5)
        Brain.screen.print("Speed decreased to: {}".format(wheel_speed))
    
    # Stop all wheel motors when R1 is pressed
    if Controller.buttonR1.pressing():
        motor_left1.stop()
        motor_left2.stop()
        motor_right1.stop()
        motor_right2.stop()
        Brain.screen.print("Motors stopped")
        return  # Exit function to prevent further spinning of motors

# Function for controlling the robot wheels using the left joystick
def drive_control():
    # Forward/backward speed from Axis 3 (left vertical stick)
    forward_speed = Controller.axis3.position()
    
    # Turning control from Axis 4 (left horizontal stick)
    turn_speed = Controller.axis4.position()
    
    # Calculate speed for each side (left and right)
    left_speed = (forward_speed + turn_speed) * (wheel_speed / 100)
    right_speed = (forward_speed - turn_speed) * (wheel_speed / 100)
    
    # Set motor velocities with direction adjustments
    motor_left1.spin(FORWARD, left_speed, PERCENT)
    motor_left2.spin(FORWARD, left_speed, PERCENT)
    motor_right1.spin(FORWARD, right_speed, PERCENT)
    motor_right2.spin(FORWARD, right_speed, PERCENT)

# Function for controlling the arm using the right joystick
def arm_control():
    # Up/down control from Axis 2 (right vertical stick)
    arm_speed = Controller.axis2.position()
    

# Function to start autonomous mode
def start_autonomous_mode():
    global autonomous_mode
    autonomous_mode = True
    Brain.screen.print("Autonomous mode activated")
    
    # Autonomous actions (replace with your specific autonomous code)
    motor_left1.spin(FORWARD, 50, PERCENT)
    motor_left2.spin(FORWARD, 50, PERCENT)
    motor_right1.spin(FORWARD, 50, PERCENT)
    motor_right2.spin(FORWARD, 50, PERCENT)

    # Wait for 17 seconds (autonomous mode duration)
    wait(17, SECONDS)
    
    # Stop all motors after autonomous period
    motor_left1.stop()
    motor_left2.stop()
    motor_right1.stop()
    motor_right2.stop()
    
    # Return to driver control
    autonomous_mode = False
    Brain.screen.print("Returning to driver control")

# Function to handle button actions
def button_actions():
    # Trigger autonomous mode with Button A
    if Controller.buttonA.pressing() and not autonomous_mode:
        start_autonomous_mode()

# Driver control task function
def driver_control():
    while competition.is_driver_control() and competition.is_enabled():
        if not autonomous_mode:  # Only allow control if not in autonomous mode
            adjust_speed()    # Adjust wheel speed with L1/L2 or stop with R1
            drive_control()   # Use joystick to drive the wheels
            arm_control()     # Use joystick to control the arm
            button_actions()  # Handle button presses (for autonomous trigger)
        wait(20, MSEC)

# Competition instance
competition = Competition(driver_control, autonomous)
