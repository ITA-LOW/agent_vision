import RPi.GPIO as GPIO
import time

# GPIO setup
SERVO_1 = 17  # First servo on GPIO 17
SERVO_2 = 18  # Second servo on GPIO 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_1, GPIO.OUT)
GPIO.setup(SERVO_2, GPIO.OUT)

# Set up PWM (50Hz is standard for servos)
pwm1 = GPIO.PWM(SERVO_1, 50)
pwm2 = GPIO.PWM(SERVO_2, 50)

pwm1.start(0)
pwm2.start(0)

def set_angle(servo, angle):
    """ Convert angle (0-180) to duty cycle and move servo """
    duty = (angle / 18) + 2  # Convert angle to duty cycle
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)  # Stop sending signal to prevent jitter

try:
    while True:
        set_angle(pwm1, 0)   # Move Servo 1 to 0°
        set_angle(pwm2, 0)   # Move Servo 2 to 0°
        time.sleep(1)

        set_angle(pwm1, 90)  # Move Servo 1 to 90°
        set_angle(pwm2, 90)  # Move Servo 2 to 90°
        time.sleep(1)

        set_angle(pwm1, 180) # Move Servo 1 to 180°
        set_angle(pwm2, 180) # Move Servo 2 to 180°
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping...")
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
