import torch
import numpy as np
import pickle
import requests
import io
from torchvision import transforms
from PIL import Image
from os import path

MODEL = None
DATA_FILE = path.join(path.dirname(__file__), 'image_encoded_cache.pickle')
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0',
    }
)
transform_test = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

class Flatten(torch.nn.Module):
    """A flatten module to squeeze single dimensions."""
    def __init__(self):
        super().__init__()

    def forward(self, x):
        return x.view(x.size(0), -1)


def encode_image(url):
    global MODEL
    if MODEL is None:
        MODEL = torch.hub.load('pytorch/vision:v0.6.0', 'mobilenet_v2', pretrained=True)
        MODEL.classifier = Flatten()
        MODEL.eval()

    data = {}
    if path.isfile(DATA_FILE):
        with open(DATA_FILE, 'rb') as fp:
            data = pickle.load(fp)

        
    if url in data:
        return data[url]
    

    print(f"Retrieving and encoding image {url}")
    img_req = requests.get(url, headers=headers, stream=True, timeout=5)
    if img_req.status_code != 200:
        return None

    img_buffer = io.BytesIO()
    for chunk in img_req:
        img_buffer.write(chunk)
    img_buffer.seek(0)

    img = Image.open(img_buffer)
    input_tensor = transform_test(img)
    input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

    # move the input and model to GPU for speed if available
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        MODEL.to('cuda')

    with torch.no_grad():
        output = MODEL(input_batch)[0]

    output = output.cpu().numpy()
    data[url] = output

    # save to cache
    with open(DATA_FILE, 'wb') as fp:
        pickle.dump(data, fp)

    print("Completed")
    return output


if __name__ == '__main__':
    print(encode_image("https://github.com/pytorch/hub/raw/master/images/dog.jpg"))