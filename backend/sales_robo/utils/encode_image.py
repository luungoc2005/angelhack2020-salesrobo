from numpy.core.defchararray import encode
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
    

    if path.isfile(url):
        img_buffer = open(url, 'rb')
    else:
        # print(f"Retrieving and encoding image {url}")
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

    img_buffer.close()
    # print("Completed")
    return output


if __name__ == '__main__':
    print(encode_image("https://github.com/pytorch/hub/raw/master/images/dog.jpg"))
    print("One iphone vs multiple iphones")
    print(np.linalg.norm(
        encode_image("https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/iphone-12-family-select-2020?wid=940&amp;hei=1112&amp;fmt=jpeg&amp;qlt=80&amp;op_usm=0.5,0.5&amp;.v=1604343709000") -
        encode_image("https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/iphone11-select-2019-family?wid=882&hei=1058&fmt=jpeg&qlt=80&op_usm=0.5,0.5&.v=1567022175704")
    , axis=0))
    print("One iphone vs Samsung phone")
    print(np.linalg.norm(
        encode_image("https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/iphone-12-family-select-2020?wid=940&amp;hei=1112&amp;fmt=jpeg&amp;qlt=80&amp;op_usm=0.5,0.5&amp;.v=1604343709000") -
        encode_image("https://images.samsung.com/sg/smartphones/galaxy-note20/buy/001-note20series-productimage-mo-720.jpg")
    , axis=0))
    print("One iphone vs Dog")
    print(np.linalg.norm(
        encode_image("https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/iphone-12-family-select-2020?wid=940&amp;hei=1112&amp;fmt=jpeg&amp;qlt=80&amp;op_usm=0.5,0.5&amp;.v=1604343709000") -
        encode_image("https://github.com/pytorch/hub/raw/master/images/dog.jpg")
    , axis=0))
    print("Dog vs Cat")
    print(np.linalg.norm(
        encode_image("https://ichef.bbci.co.uk/news/1024/cpsprodpb/151AB/production/_111434468_gettyimages-1143489763.jpg") -
        encode_image("https://github.com/pytorch/hub/raw/master/images/dog.jpg")
    , axis=0))
    print("Cat vs Cat")
    print(np.linalg.norm(
        encode_image("https://ichef.bbci.co.uk/news/1024/cpsprodpb/151AB/production/_111434468_gettyimages-1143489763.jpg") -
        encode_image("https://image.cnbcfm.com/api/v1/image/105828578-1554223245858gettyimages-149052633.jpeg?v=1554223281")
    , axis=0))