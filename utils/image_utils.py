# will contains all the image utils functions
from PIL import Image

# function to load image and resize it to 224x224 as docs of models 
def process_image(image_path, size=(224, 224)):
    image = Image.open(image_path).convert("RGB")
    image = image.resize(size)
    return image