import json
from PIL import Image
import torchvision.transforms as transforms

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def preprocess_image(image_path):
    image = Image.open(image_path)
    return preprocess(image).numpy()

# Example of creating a dataset JSON file
dataset = []
for image_path, color_label in your_data:
    image_features = preprocess_image(image_path)
    dataset.append({'image': image_features.tolist(), 'label': color_label})

with open('dataset.json', 'w') as f:
    json.dump(dataset, f)