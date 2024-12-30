import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from torchvision.transforms import Resize

# Neural Network Class
class ImageEnhancementNet(nn.Module):
    def __init__(self):
        super(ImageEnhancementNet, self).__init__()
        # Encoder
        self.enc1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1)
        self.enc2 = nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1)
        self.enc3 = nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1)
        # Decoder
        self.dec1 = nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, output_padding=0)
        self.dec2 = nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=0)
        self.dec3 = nn.Conv2d(64, 3, kernel_size=3, stride=1, padding=1)
        # Batch Normalization
        self.bn1 = nn.BatchNorm2d(64)
        self.bn2 = nn.BatchNorm2d(128)
        self.bn3 = nn.BatchNorm2d(256)

    def forward(self, x):
        # Encoder
        x = F.relu(self.bn1(self.enc1(x)))
        x = F.relu(self.bn2(self.enc2(x)))
        x = F.relu(self.bn3(self.enc3(x)))
        # Decoder
        x = F.relu(self.dec1(x, output_size=(x.shape[2]*2, x.shape[3]*2)))
        x = F.relu(self.dec2(x, output_size=(x.shape[2]*2, x.shape[3]*2)))
        x = torch.sigmoid(self.dec3(x))
        return x


    
# Custom Dataset Class
class ImageEnhancementDataset(Dataset):
    def __init__(self, x_data, y_data):
        self.x_data = torch.tensor(x_data, dtype=torch.float32).permute(0, 3, 1, 2)  # NHWC to NCHW
        self.y_data = torch.tensor(y_data, dtype=torch.float32).permute(0, 3, 1, 2)
        self.resize = Resize((180, 220))  # Match model's output size

    def __getitem__(self, idx):
        x = self.x_data[idx]
        y = self.y_data[idx]
        y_resized = self.resize(y)
        return x, y_resized

    def __len__(self):
        return len(self.x_data)
    