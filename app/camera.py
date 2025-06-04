#!/usr/bin/env python3
from picamera2 import Picamera2
import cv2
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def camera_feed():
    picam2 = None
    try:
        # Initialize the camera
        picam2 = Picamera2()
        picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
        picam2.start()
        
        logger.info("Camera started successfully")
        
        while True:
            try:
                # Capture frame with timeout protection
                frame = picam2.capture_array()
                
                if frame is None:
                    logger.warning("Received empty frame, skipping...")
                    time.sleep(0.1)
                    continue
                
                # Encode frame
                success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                
                if not success:
                    logger.warning("Failed to encode frame")
                    time.sleep(0.1)
                    continue
                
                frame_bytes = buffer.tobytes()
                
                # Clear buffer to prevent memory buildup
                del buffer
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
            except Exception as e:
                logger.error(f"Error capturing frame: {e}")
                time.sleep(0.5)  # Wait before retrying
                
                # Try to restart camera if needed
                if "Camera is not running" in str(e) or "Camera is closed" in str(e):
                    logger.info("Attempting to restart camera...")
                    try:
                        if picam2:
                            picam2.stop()
                            picam2.close()
                        time.sleep(5)
                        picam2 = Picamera2()
                        picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
                        picam2.start()
                        logger.info("Camera restarted successfully")
                    except Exception as restart_error:
                        logger.error(f"Failed to restart camera: {restart_error}")
                        break
                        
    except Exception as e:
        logger.error(f"Fatal camera error: {e}")
    finally:
        # Cleanup camera resources
        if picam2:
            try:
                picam2.stop()
                picam2.close()
                logger.info("Camera resources cleaned up")
            except:
                pass

# Alternative version with automatic restart capability
def robust_camera_feed():
    """More robust version that can handle camera disconnections"""
    while True:
        try:
            logger.info("Starting camera feed...")
            for frame_data in camera_feed():
                yield frame_data
        except Exception as e:
            logger.error(f"Camera feed crashed: {e}")
            logger.info("Restarting camera feed in 5 seconds...")
            time.sleep(10)
