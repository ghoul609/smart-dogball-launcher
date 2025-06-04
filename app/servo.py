#!/usr/bin/env python3

import pigpio
import time

def set_pulse(pi, SERVO_PIN, pulse_width):
    # Servo configuration
    SERVO_MIN_PULSE = 500  # Minimum pulse width
    SERVO_MAX_PULSE = 2500  # Maximum pulse width

    if not pi.connected:
        print("Failed to connect to pigpio daemon!")
        return None

    # Clamp to safe range
    pulse_width = max(SERVO_MIN_PULSE, min(SERVO_MAX_PULSE, pulse_width))

    # Move servo
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
    current_pulse = pulse_width

    return current_pulse

def servo():
    try:
        pi = pigpio.pi()
        SERVO_PIN = 18  # GPIO 18
        PULSE_WIDTH_1 = 1800
        PULSE_WIDTH_2 = 2050 

        # Move to first position
        print(f"Moving to Position 1: {PULSE_WIDTH_1} μs")
        set_pulse(pi, SERVO_PIN, PULSE_WIDTH_1)
        time.sleep(0.15)

        # Move to second position
        print(f"Moving to Position 2: {PULSE_WIDTH_2} μs")
        set_pulse(pi, SERVO_PIN, PULSE_WIDTH_2)
        time.sleep(0.15)

        # Back to first position
        print(f"Back to Position 1: {PULSE_WIDTH_1} μs")
        set_pulse(pi, SERVO_PIN, PULSE_WIDTH_1)
        time.sleep(0.15)
    finally:
        # Cleanup
        pi.set_servo_pulsewidth(SERVO_PIN, 0)
        pi.stop()
        print("Servo stopped")

if __name__ == "__main__":
    servo()
    print("Servo operation completed")
