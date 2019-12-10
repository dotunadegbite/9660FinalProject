import fnmatch
import numpy as np
import os
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms


class GameDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, csv_file, root_dir, transform=None):
        self.stimulus_dir = root_dir + "stimuli/"
        self.label_dir = root_dir + "labels/"
        self.len = len(fnmatch.filter(os.listdir(self.label_dir), '*.npy'))
        self.transform = transform

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        stimulus = np.load(self.stimulus_dir + str(idx) + ".npy")
        label = np.load(self.label_dir + str(idx) + ".npy")

        if self.transform:
            stimulus = self.transform(stimulus)
        img = Image.fromarray(stimulus)

        return transforms.ToTensor()(img), torch.tensor(label)
