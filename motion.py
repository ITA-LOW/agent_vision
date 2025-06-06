import RPi.GPIO as GPIO
import time

# GPIO setup
SERVO_1 = 17  # First servo on GPIO 17
SERVO_2 = 27  # Second servo on GPIO 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_1, GPIO.OUT)
GPIO.setup(SERVO_2, GPIO.OUT)

# Set up PWM (50Hz is standard for servos)
pwm1 = GPIO.PWM(SERVO_1, 50)
pwm2 = GPIO.PWM(SERVO_2, 50)

pwm1.start(0)
pwm2.start(0)

position_to_angle = {
    "top_left": (135, 180), "top_center": (90, 180), "top_right": (45, 180),
    "middle_left": (135, 160), "middle_center": (90, 160), "middle_right": (45, 160),
    "bottom_left": (135, 135), "bottom_center": (90, 135), "bottom_right": (45, 135)
}

def reset_pos():
    """ Reset servos to the middle position at startup. """
    print("Resetting servos to middle position...")
    look_at("middle_center")

def angle_to_duty_cycle(angle):
    """ Convert angle (0-180) to duty cycle for 50Hz PWM (2-12% range). """
    return (angle / 18) + 2

def look_at(position):
    """ Move both servos to the specified position. """
    if position not in position_to_angle:
        print(f"Invalid position: {position}")
        return

    angle1, angle2 = position_to_angle[position]

    duty1 = angle_to_duty_cycle(angle1)
    duty2 = angle_to_duty_cycle(angle2)

    pwm1.ChangeDutyCycle(duty1)
    pwm2.ChangeDutyCycle(duty2)

    time.sleep(0.1)  # Allow servos to move

    pwm1.ChangeDutyCycle(0)  # Stop signal to prevent jitter
    pwm2.ChangeDutyCycle(0)

def cleanup():
    """ Cleanup GPIO resources (should be called before exiting). """
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
