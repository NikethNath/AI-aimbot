import ctypes
import numpy as np
import cv2
import sys
import os

class CppScreenCapturer:
    def __init__(self, x=0, y=0, width=None, height=None):
        try:
            # Load the C++ DLL
            dll_path = './screen_capture.dll'
            if not os.path.exists(dll_path):
                raise FileNotFoundError(f"DLL not found at {dll_path}")
                
            self.cpp_lib = ctypes.CDLL(dll_path)
            
            # Set up function prototypes
            self.cpp_lib.initialize_capture.restype = ctypes.c_bool
            self.cpp_lib.initialize_capture.argtypes = [
                ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int
            ]
            
            self.cpp_lib.capture_screen.restype = ctypes.c_bool
            self.cpp_lib.capture_screen.argtypes = [
                np.ctypeslib.ndpointer(dtype=np.uint8, flags='C_CONTIGUOUS'),
                ctypes.c_int
            ]
            
            self.cpp_lib.get_screen_dimensions.argtypes = [
                ctypes.POINTER(ctypes.c_int),
                ctypes.POINTER(ctypes.c_int)
            ]
            
            self.cpp_lib.cleanup_capture.restype = None
            
            # Get screen dimensions if not provided
            if width is None or height is None:
                width = ctypes.windll.user32.GetSystemMetrics(0)
                height = ctypes.windll.user32.GetSystemMetrics(1)
            
            self.width = width
            self.height = height
            
            # Initialize C++ capture
            if not self.cpp_lib.initialize_capture(x, y, width, height):
                raise RuntimeError("Failed to initialize C++ screen capture")
            
            # Pre-allocate buffer
            self.buffer = np.zeros((self.height, self.width, 4), dtype=np.uint8)
            
            print(f"C++ Screen capture initialized: {self.width}x{self.height}")
            
        except Exception as e:
            print(f"Failed to initialize C++ capture: {e}")
            print("Falling back to Python MSS...")
            self.fallback_to_python()
    
    def fallback_to_python(self):
        """Fallback to Python MSS if C++ fails"""
        import mss
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]
        self.buffer = np.zeros((self.monitor["height"], self.monitor["width"], 4), dtype=np.uint8)
        self._capture = self._capture_python
        self._close = self._close_python
        print("Using Python MSS fallback")
    
    def _capture_cpp(self):
        buffer_size = self.buffer.nbytes
        success = self.cpp_lib.capture_screen(self.buffer, buffer_size)
        if not success:
            raise RuntimeError("C++ screen capture failed")
        return cv2.cvtColor(self.buffer, cv2.COLOR_BGRA2BGR)
    
    def _capture_python(self):
        img = np.array(self.sct.grab(self.monitor))
        np.copyto(self.buffer, np.asarray(img))
        return cv2.cvtColor(self.buffer, cv2.COLOR_BGRA2BGR)
    
    def capture_screen(self):
        return self._capture()
    
    def _close_cpp(self):
        self.cpp_lib.cleanup_capture()
    
    def _close_python(self):
        self.sct.close()
    
    def close(self):
        self._close()

# Global instance for easy import
_capturer = None

def init_capturer(x=0, y=0, width=None, height=None):
    global _capturer
    if _capturer is None:
        _capturer = CppScreenCapturer(x, y, width, height)

def capture_screen():
    global _capturer
    if _capturer is None:
        init_capturer()
    return _capturer.capture_screen()

def close_capturer():
    global _capturer
    if _capturer is not None:
        _capturer.close()
        _capturer = None

# Auto-initialize when imported
init_capturer()