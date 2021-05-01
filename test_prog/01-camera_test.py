from picamera import PiCamera
from time import sleep

# Initialize Camera object
camera = PiCamera()
camera.resolution = (640, 480)
sleep(1)  # Warmup

# Show preview of camera for 5 seconds
camera.start_preview()
sleep(5)
camera.stop_preview()

camera.capture('/home/pi/Desktop/image.jpg')
print(f"Captured image! Stored here -> {'/home/pi/Desktop/image.jpg'}")

camera.close()
