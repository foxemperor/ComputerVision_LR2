import cv2
import numpy as np
import sys

def test_opencv():
    """Тест установки OpenCV"""
    print("="*60)
    print(f"OpenCV версия: {cv2.__version__}")
    print(f"Python версия: {sys.version}")
    print(f"NumPy версия: {np.__version__}")
    print("="*60)
    print("✅ OpenCV успешно установлен!")
    
if __name__ == "__main__":
    test_opencv()
