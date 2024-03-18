import RPi.GPIO as GPIO
import time

# Define pins
s2 = 23
s3 = 24
signal = 25
NUM_CYCLES = 10

# Setup GPIO
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(s2, GPIO.OUT)
    GPIO.setup(s3, GPIO.OUT)
    print("\n")

# Normalize frequency to RGB
def freq_to_rgb(value, min_freq, max_freq):
    return int((value - min_freq) * 255 / (max_freq - min_freq))

# Simple color name approximation based on RGB values
def get_color_name(rgb):
    r, g, b = rgb
    if r > g and r > b:
        return 'Red'
    elif g > r and g > b:
        return 'Green'
    elif b > r and b > g:
        return 'Blue'
    else:
        return 'Unknown'

# Main loop
def loop():
    min_freq = 450  # Example minimum frequency (should be calibrated)
    max_freq = 27000  # Example maximum frequency (should be calibrated)
    
    while True:
        GPIO.output(s2, GPIO.LOW)
        GPIO.output(s3, GPIO.LOW)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        red_freq = NUM_CYCLES / duration
        red = freq_to_rgb(red_freq, min_freq, max_freq)

        GPIO.output(s2, GPIO.LOW)
        GPIO.output(s3, GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        blue_freq = NUM_CYCLES / duration
        blue = freq_to_rgb(blue_freq, min_freq, max_freq)

        GPIO.output(s2, GPIO.HIGH)
        GPIO.output(s3, GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        green_freq = NUM_CYCLES / duration
        green = freq_to_rgb(green_freq, min_freq, max_freq)

        color_name = get_color_name((red, green, blue))
        print(f"Detected color: {color_name}")

        time.sleep(2)

# Cleanup on exit
def endprogram():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        endprogram()
