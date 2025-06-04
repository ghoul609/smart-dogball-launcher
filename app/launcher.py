#!/usr/bin/env python3

import pigpio
import time
from servo import servo

# Define pin numbers
DIR1 = 17  # Direction pin for motor 1
PWM1 = 12  # PWM pin for motor 1
DIR2 = 22  # Direction pin for motor 2
PWM2 = 13  # PWM pin for motor 2

# PWM settings
PWM_FREQ = 10000  # 9kHz frequency
MAX_SPEED = 255   # Maximum PWM value
TARGET_SPEED = 125  # 80% of maximum (target speed)

def setup_motors():
    # Initialize pigpio
    pi = pigpio.pi()
    if not pi.connected:
        print("Failed to connect to pigpio daemon!")
        return None

    # Set up direction pins as output
    pi.set_mode(DIR1, pigpio.OUTPUT)
    pi.set_mode(DIR2, pigpio.OUTPUT)

    # Set up PWM pins as output
    pi.set_mode(PWM1, pigpio.OUTPUT)
    pi.set_mode(PWM2, pigpio.OUTPUT)

    # Set PWM frequency
    pi.set_PWM_frequency(PWM1, PWM_FREQ)
    pi.set_PWM_frequency(PWM2, PWM_FREQ)

    # Initialize with motors stopped
    pi.set_PWM_dutycycle(PWM1, 0)
    pi.set_PWM_dutycycle(PWM2, 0)

    return pi

def set_motor_directions(pi, dir1, dir2):
    """Set direction pins for both motors"""
    pi.write(DIR1, dir1)
    pi.write(DIR2, dir2)

def set_motor_speeds(pi, speed1, speed2):
    """Set PWM speed for both motors"""
    pi.set_PWM_dutycycle(PWM1, speed1)
    pi.set_PWM_dutycycle(PWM2, speed2)

def accelerate_motors(pi, target_speed=TARGET_SPEED, accel_time=1.0):
    """Gradually accelerate motors to target speed"""
    steps = 20  # Number of steps for acceleration
    delay = accel_time / steps

    for i in range(steps + 1):
        # Calculate current speed in acceleration ramp
        current_speed = (target_speed * i) / steps
        set_motor_speeds(pi, current_speed, current_speed)
        time.sleep(delay)

    print(f"Motors reached target speed of {int(target_speed/MAX_SPEED*100)}%")

def decelerate_motors(pi, start_speed=TARGET_SPEED, decel_time=1.0):
    """Gradually decelerate motors to stop"""
    steps = 20  # Number of steps for deceleration
    delay = decel_time / steps

    for i in range(steps, -1, -1):
        # Calculate current speed in deceleration ramp
        current_speed = (start_speed * i) / steps
        set_motor_speeds(pi, current_speed, current_speed)
        time.sleep(delay)

    print("Motors stopped")

def run_motors_opposite_smooth(pi, target_speed=TARGET_SPEED, run_time=5):
    """Run motors in opposite directions with smooth start and stop"""
    # Set motor directions (opposite to each other)
    set_motor_directions(pi, 1, 0)  # Motor 1 forward, Motor 2 backward

    # Start with motors stopped
    set_motor_speeds(pi, 0, 0)

    print("Starting motors in opposite directions...")

    # Accelerate motors
    accelerate_motors(pi, target_speed)
    
    # Move servo to launch position
    print("Moving servo to launch position...")
    servo()  # Call the servo function to move the servo

    # Run at constant speed
    print(f"Running at {int(target_speed/MAX_SPEED*100)}% speed for {run_time} seconds")
    time.sleep(run_time)  # Note: This was duplicated in the original code # Decelerate motors
    print("Slowing down motors...")
    decelerate_motors(pi, target_speed)

def cleanup(pi):
    """Clean up resources"""
    # Ensure motors are stopped
    set_motor_speeds(pi, 0, 0)
    # Close pigpio connection
    pi.stop()
    print("pigpio resources cleaned up")

def launchBall(TARGET_SPEED: int):
    try:
        # Initialize pigpio
        pi = setup_motors()
        if pi is None:
            exit(1)

        # Run sequence with smooth acceleration/deceleration
        run_motors_opposite_smooth(pi, TARGET_SPEED, 5)

    except KeyboardInterrupt:
        print("\nProgram stopped by user")

    finally:
        # Always clean up resources
        if 'pi' in locals() and pi is not None:
            cleanup(pi)
