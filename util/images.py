import cv2
import numpy as np

def load_image(image_path: str) -> np.ndarray:
    """Load an image from a file path and return it as a numpy array."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image not found at {image_path}")
    return image

def save_image(image: np.ndarray, image_path: str) -> None:
    """Save a numpy array as an image to a file path."""
    cv2.imwrite(image_path, image)