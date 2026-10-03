import io
import pytest
from PIL import Image
from backend.core.image_classifier import FridgeScanner

def test_scanner_with_red_image():
    # Create red test image (mimicking tomatoes / red chillies)
    img = Image.new("RGB", (200, 200), color=(220, 40, 30))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    detections = FridgeScanner.process_image_bytes(buf.getvalue())

    assert len(detections) > 0
    names = [d["name"].lower() for d in detections]
    assert any("tomato" in n for n in names)

def test_scanner_with_green_image():
    # Create green test image (mimicking coriander / green chillies / spinach)
    img = Image.new("RGB", (200, 200), color=(35, 160, 50))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    detections = FridgeScanner.process_image_bytes(buf.getvalue())

    assert len(detections) > 0
    names = [d["name"].lower() for d in detections]
    assert any("coriander" in n or "green" in n or "spinach" in n for n in names)
