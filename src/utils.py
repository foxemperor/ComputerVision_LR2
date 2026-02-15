"""
Вспомогательные функции для обработки изображений и трекинга.
"""

import cv2
import numpy as np

def create_red_mask(hsv_image, lower1, upper1, lower2, upper2):
    """
    Создает маску для красного цвета с учетом двух диапазонов.
    
    Args:
        hsv_image: Изображение в HSV формате
        lower1, upper1: Первый диапазон красного (0-10)
        lower2, upper2: Второй диапазон красного (170-180)
    
    Returns:
        Объединенная маска
    """
    mask1 = cv2.inRange(hsv_image, np.array(lower1), np.array(upper1))
    mask2 = cv2.inRange(hsv_image, np.array(lower2), np.array(upper2))
    return cv2.bitwise_or(mask1, mask2)

def apply_morphology(mask, kernel, iterations=2):
    """
    Применяет морфологические операции открытия и закрытия.
    
    Args:
        mask: Бинарная маска
        kernel: Структурный элемент
        iterations: Количество итераций
    
    Returns:
        Обработанная маска
    """
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=iterations)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    return closing

def calculate_centroid(moments):
    """
    Вычисляет координаты центроида по моментам изображения.
    
    Args:
        moments: Словарь моментов изображения
    
    Returns:
        Tuple (cx, cy) или None если объект не найден
    """
    if moments["m00"] == 0:
        return None
    
    cx = int(moments["m10"] / moments["m00"])
    cy = int(moments["m01"] / moments["m00"])
    return (cx, cy)

def draw_tracking_info(frame, x, y, w, h, cx, cy, area):
    """
    Отрисовывает информацию о трекинге на кадре.
    
    Args:
        frame: Кадр для отрисовки
        x, y, w, h: Координаты и размеры прямоугольника
        cx, cy: Координаты центра
        area: Площадь объекта
    """
    # Черный прямоугольник вокруг объекта
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
    
    # Зеленая точка в центре
    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
    
    # Текстовая информация
    cv2.putText(frame, f"Area: {int(area)}", (x, y - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(frame, f"Center: ({cx}, {cy})", (x, y + h + 20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

def setup_windows(positions):
    """
    Настраивает позиции окон для отображения.
    
    Args:
        positions: Словарь с названиями окон и их позициями
    """
    for window_name, (x, y) in positions.items():
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(window_name, x, y)
