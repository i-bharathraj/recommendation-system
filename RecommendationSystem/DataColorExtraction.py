import colorgram

def extract_dominant_color(image_path):
    colors = colorgram.extract(image_path, 1)
    return colors[0].rgb
