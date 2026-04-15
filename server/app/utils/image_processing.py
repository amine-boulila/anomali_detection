"""Image preprocessing helpers reused by the ML and DL prediction flows."""

import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops

DEFAULT_ML_IMAGE_SIZE = (128, 128)
DEFAULT_DL_IMAGE_SIZE = (224, 224)


def decode_image_bytes(image_bytes: bytes) -> np.ndarray:
    """Decode uploaded bytes into an OpenCV BGR image."""
    array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError(
            "The uploaded file could not be decoded as an image. "
            "Please upload a valid JPG, PNG, BMP, or WEBP file."
        )

    return image


def resize_image(image_bgr: np.ndarray, target_size: tuple[int, int]) -> np.ndarray:
    """Resize images to the same dimensions used during training."""
    return cv2.resize(image_bgr, target_size, interpolation=cv2.INTER_AREA)


def gaussian_blur(image_bgr: np.ndarray) -> np.ndarray:
    """Reduce small image noise before feature extraction."""
    return cv2.GaussianBlur(image_bgr, (5, 5), 0)


def to_gray(image_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)


def to_hsv(image_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)


def hsv_segmentation(image_bgr: np.ndarray) -> np.ndarray:
    """
    Isolates the leaf region with the same HSV thresholds used in the notebook.

    TODO: update these bounds if your training notebook used different values.
    """
    hsv = to_hsv(image_bgr)
    lower = np.array([20, 20, 20])
    upper = np.array([95, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def largest_contour(mask: np.ndarray):
    """Find the main leaf contour for shape features."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return max(contours, key=cv2.contourArea) if contours else None


def preprocess_image_for_ml(
    image_bgr: np.ndarray,
    target_size: tuple[int, int] = DEFAULT_ML_IMAGE_SIZE,
) -> np.ndarray:
    """
    ML preprocessing step.

    This mirrors the notebook:
    - resize to 128x128
    - apply Gaussian blur
    """
    resized = resize_image(image_bgr, target_size)
    return gaussian_blur(resized)


def extract_hsv_hist_features(
    image_bgr: np.ndarray,
    bins: tuple[int, int, int] = (8, 8, 8),
) -> np.ndarray:
    """Color features from a normalized HSV histogram."""
    hsv = to_hsv(image_bgr)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
    return cv2.normalize(hist, hist).flatten().astype(np.float32)


def extract_glcm_features(image_bgr: np.ndarray) -> np.ndarray:
    """Texture features based on the notebook's GLCM configuration."""
    gray = cv2.resize(to_gray(image_bgr), (64, 64), interpolation=cv2.INTER_AREA)
    glcm = graycomatrix(
        gray,
        distances=[1, 2],
        angles=[0, np.pi / 4, np.pi / 2],
        levels=256,
        symmetric=True,
        normed=True,
    )

    features: list[float] = []
    for prop in ["contrast", "dissimilarity", "homogeneity", "energy", "correlation"]:
        features.extend(graycoprops(glcm, prop).flatten())
    return np.array(features, dtype=np.float32)


def extract_shape_features(image_bgr: np.ndarray) -> np.ndarray:
    """Shape descriptors based on the largest leaf contour."""
    mask = hsv_segmentation(image_bgr)
    contour = largest_contour(mask)

    if contour is None:
        return np.zeros(5, dtype=np.float32)

    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    _, _, width, height = cv2.boundingRect(contour)
    extent = area / max(width * height, 1)
    circularity = (4 * np.pi * area) / (perimeter**2) if perimeter > 0 else 0.0
    area_ratio = area / (image_bgr.shape[0] * image_bgr.shape[1])

    return np.array(
        [area, perimeter, extent, circularity, area_ratio],
        dtype=np.float32,
    )


def extract_ml_feature_vector(image_bgr: np.ndarray) -> np.ndarray:
    """
    Feature extraction step for the classical ML model.

    Notebook-derived feature vector:
    - HSV histogram
    - GLCM texture
    - contour shape
    """
    return np.concatenate(
        [
            extract_hsv_hist_features(image_bgr),
            extract_glcm_features(image_bgr),
            extract_shape_features(image_bgr),
        ]
    ).astype(np.float32)


def preprocess_image_for_dl(
    image_bgr: np.ndarray,
    target_size: tuple[int, int] = DEFAULT_DL_IMAGE_SIZE,
) -> np.ndarray:
    """
    DL preprocessing step.

    The saved DL model metadata says it expects 224x224 images.
    """
    resized = resize_image(image_bgr, target_size)
    rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    return rgb_image.astype(np.float32)
