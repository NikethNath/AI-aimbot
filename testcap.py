from screen_capture import capture_screen, close_capturer
import cv2
import time

def test_performance():
    print("Testing C++ screen capture performance...")
    
    # Test for 100 frames
    start_time = time.time()
    for i in range(100):
        frame = capture_screen()
        
        # Show frame
        cv2.imshow('Test Capture', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        if i % 10 == 0:
            print(f"Captured frame {i}")
    
    end_time = time.time()
    fps = 100 / (end_time - start_time)
    print(f"Average FPS: {fps:.2f}")
    
    close_capturer()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_performance()