import time
import cv2
from picamera2 import Picamera2
from pwn import remote

HOST = "20.197.53.199"  
PORT = 9999

def capture_jpeg_hex():
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration())
    picam2.start()         
    arr = picam2.capture_array()   
    picam2.stop()

    ok, buf = cv2.imencode('.jpg', arr)
    if not ok:
        raise RuntimeError("JPEG encoding failed")
    jpg_bytes = buf.tobytes()
    return jpg_bytes.hex()     

def main():
    while True:
        try:
            print(f"Connecting to {HOST}:{PORT} ...")
            conn = remote(HOST, PORT, timeout=20)
        except Exception as e:
            print("Connection failed:", e)
            time.sleep(3)
            continue

        try:
            
            conn.recvline() # Model loaded
            conn.recvline() # server up

            payload = capture_jpeg_hex()
            conn.sendline(str(len(payload)).encode())

            conn.sendline(payload.encode())

            reply = conn.recvline().decode().strip()
            print("Server reply:", reply)

        except Exception as e:
            print("Error during capture/send:", e)
    
        # small delay before next capture
        time.sleep(2)

if __name__ == "__main__":
    main()
