import torch
from torchvision.models import resnet50

model = resnet50(pretrained=True)
model.eval()

def extract_features(image_path):
    image = Image.open(image_path)
    image = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        features = model(image)
    return features.numpy()
