import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from torch.optim import Adam
import os
from dataset import MathExprDataset
from alphabet import VOCAB  

class CRNN(nn.Module):
    def __init__(self, num_classes):
        super(CRNN, self).__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1), nn.ReLU(), nn.MaxPool2d((2, 1)),
            nn.Conv2d(256, 512, 3, padding=1), nn.BatchNorm2d(512), nn.ReLU(),
            nn.Conv2d(512, 512, 3, padding=1), nn.BatchNorm2d(512), nn.ReLU(), nn.MaxPool2d((2, 1))
        )
        
        self.lstm1 = nn.LSTM(input_size=512, hidden_size=256, bidirectional=True, batch_first=True)
        self.lstm2 = nn.LSTM(input_size=512, hidden_size=256, bidirectional=True, batch_first=True)
        
        self.fc = nn.Linear(512, num_classes)

    def forward(self, x):
        x = self.cnn(x)  
        b, c, h, w = x.size()

        # Усредняем по высоте
        x = torch.mean(x, dim=2)  
        x = x.permute(0, 2, 1)    

        x, _ = self.lstm1(x)
        x, _ = self.lstm2(x)

        x = self.fc(x)           
        x = x.permute(1, 0, 2)   
        return x

def collate_fn(batch):
    imgs, labels = zip(*batch)
    imgs = torch.stack(imgs)
    label_lens = torch.tensor([len(l) for l in labels])
    labels = pad_sequence([torch.tensor(l) for l in labels], batch_first=True, padding_value=VOCAB.index('<PAD>'))
    return imgs, labels, label_lens

def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_dir = os.path.join(base_dir, 'data', 'images')
    label_dir = os.path.join(base_dir, 'data', 'labels')

    if not os.path.exists(image_dir) or not os.path.exists(label_dir):
        raise FileNotFoundError("Не найдены папки data/images или data/labels")

    dataset = MathExprDataset(image_dir, label_dir)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True, collate_fn=collate_fn)

    model = CRNN(num_classes=len(VOCAB)).to(device)
    optimizer = Adam(model.parameters(), lr=0.001)
    criterion = nn.CTCLoss(blank=VOCAB.index('<PAD>'), zero_infinity=True)

    for epoch in range(50):
        model.train()
        epoch_loss = 0
        for imgs, labels, label_lens in dataloader:
            imgs, labels, label_lens = imgs.to(device), labels.to(device), label_lens.to(device)
            optimizer.zero_grad()
            output = model(imgs)  
            input_lens = torch.full((imgs.size(0),), output.size(0), dtype=torch.long).to(device)
            loss = criterion(output, labels, input_lens, label_lens)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        print(f"Epoch {epoch+1}: Loss = {epoch_loss / len(dataloader):.4f}")
        torch.save(model.state_dict(), os.path.join(base_dir, 'model', f"model_epoch{epoch+1}.pth"))

if __name__ == '__main__':
    train()
