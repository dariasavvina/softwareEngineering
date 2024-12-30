from ultralytics import YOLO
from PIL import Image
from model import ImageObjectsResponse
import io


def yolo_predict(image_data):
    image = Image.open(io.BytesIO(image_data))
    model = YOLO("yolo11n.pt")
    predictions = model.predict(image)

    return ImageObjectsResponse(response = {model.names[int(cls)] for cls in predictions[0].boxes.cls})