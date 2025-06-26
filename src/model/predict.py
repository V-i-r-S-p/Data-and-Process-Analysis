import torch
from torchvision import transforms
from PIL import Image
import os
from train import CRNN  
from alphabet import VOCAB, detokenize  

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = CRNN(num_classes=len(VOCAB)).to(device)
model.load_state_dict(torch.load("model_epoch77.pth", map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((64, 256)),
    transforms.ToTensor()
])

def predict_image(img_path):
    image = Image.open(img_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device) 

    with torch.no_grad():
        output = model(image)  
        output = output.softmax(2)
        output = output.argmax(2)[:, 0]  

    tokens = output.cpu().numpy()

    result = []
    prev = -1
    for t in tokens:
        if t != prev and t != VOCAB.index('<PAD>'):
            result.append(t)
        prev = t

    return detokenize(result)

if __name__ == "__main__":
    test_dir = "test_images" 
    for fname in os.listdir(test_dir):
        if fname.endswith(".png"):
            path = os.path.join(test_dir, fname)
            prediction = predict_image(path)
            print(f"{fname}: {prediction}")