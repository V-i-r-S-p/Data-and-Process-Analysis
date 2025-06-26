from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms
import os
from alphabet import tokenize

class MathExprDataset(Dataset):
    def __init__(self, img_dir, lbl_dir, transform=None):
        self.samples = []

        print(f"Reading from:\n  Images: {img_dir}\n  Labels: {lbl_dir}")

        for fname in os.listdir(img_dir):
            if fname.lower().endswith(".jpg") or fname.lower().endswith(".png") or fname.lower().endswith(".bmp"):
                img_path = os.path.join(img_dir, fname)
                lbl_path = os.path.join(lbl_dir, fname.replace(".jpg", ".txt"))
                if fname.lower().endswith(".png"):
                    lbl_path = os.path.join(lbl_dir, fname.replace(".png", ".txt"))
                if fname.lower().endswith(".bmp"):
                    lbl_path = os.path.join(lbl_dir, fname.replace(".bmp", ".txt"))
                if os.path.exists(lbl_path):
                    self.samples.append((img_path, lbl_path))
                else:
                    print(f"Label missing for {fname}")

        print(f"Found {len(self.samples)} pairs.")

        self.transform = transform or transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((64, 256)),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, lbl_path = self.samples[idx]
        image = self.transform(Image.open(img_path).convert('RGB'))
        with open(lbl_path, 'r') as f:
            label = tokenize(f.read().strip())
        return image, label