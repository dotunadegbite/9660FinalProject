import numpy as np
import torch
import torch.nn.functional as F
import torch.nn as nn
from torchvision.models import *
import torch.optim as optim


class Reshape(nn.Module):
    def __init__(self, *args):
        super(Reshape, self).__init__()
        self.shape = args

    def forward(self, x):
        return F.log_softmax(x.view(self.shape), -1)


models = {
    "resnet18": nn.Sequential(resnet18(pretrained=False), nn.Linear(1000, 150), Reshape(-1, 5, 5, 6)),
    "resnet50": nn.Sequential(resnet50(pretrained=False), nn.Linear(1000, 150), Reshape(-1, 5, 5, 6)),
    "alexnet": nn.Sequential(alexnet(pretrained=False, num_classes=150), Reshape(-1, 5, 5, 6)),
    # "inception_v3": nn.Sequential(inception_v3(pretrained=False, num_classes=150), Reshape(-1, 5, 5, 6)),
    'vgg11': nn.Sequential(vgg11_bn(pretrained=False, num_classes=150), Reshape(-1, 5, 5, 6)),
    'vgg13': nn.Sequential(vgg13_bn(pretrained=False, num_classes=150), Reshape(-1, 5, 5, 6)),
    'vgg16': nn.Sequential(vgg16_bn(pretrained=False, num_classes=150), Reshape(-1, 5, 5, 6)),
    'vgg19':  nn.Sequential(vgg19_bn(pretrained=False, num_classes=150), Reshape(-1, 5, 5, 6)),
    'vgg11_bn': nn.Sequential(vgg11_bn(pretrained=False, num_classes=150), Reshape(-1, 5, 5, 6)),
    'vgg13_bn': nn.Sequential(vgg13_bn(pretrained=False, num_classes=150), Reshape(-1, 5, 5, 6)),
    'vgg16_bn': nn.Sequential(vgg16_bn(pretrained=False, num_classes=150), Reshape(-1, 5, 5, 6)),
    'vgg19_bn':  nn.Sequential(vgg19_bn(pretrained=False, num_classes=150), Reshape(-1, 5, 5, 6)),
}


def get_data_loaders(dataset, batch_size, test_split, shuffle_dataset=True):
    # Creating data indices for training and validation splits:
    dataset_size = len(dataset)
    print("DATASET SIZE", dataset_size)
    indices = list(range(dataset_size))
    split = int(np.floor(test_split * dataset_size))
    if shuffle_dataset:
        np.random.shuffle(indices)
    train_indices, test_indices = indices[split:], indices[:split]

    # Creating PT data samplers and loaders:
    train_sampler = torch.utils.data.SubsetRandomSampler(train_indices)
    test_sampler = torch.utils.data.SubsetRandomSampler(test_indices)

    train_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                               sampler=train_sampler)
    test_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                                    sampler=test_sampler)
    return train_loader, test_loader


def get_optimizer(model, args):
    if args.experiment == 'a001':
        optimizer = optim.Adam(model.parameters(), lr=0.001)
    elif args.experiment == 'a0001':
        optimizer = optim.Adam(model.parameters(), lr=0.0001)
    elif args.experiment == 's01':
        optimizer = optim.SGD(model.parameters(), lr=0.01)
    elif args.experiment == 's001':
        optimizer = optim.SGD(model.parameters(), lr=0.001)
    elif args.experiment == 's0001':
        optimizer = optim.SGD(model.parameters(), lr=0.0001)
    elif args.experiment == 's00005':
        optimizer = optim.SGD(model.parameters(), lr=0.00005)
    else:
        raise Exception("Specify a valid experiment")
    return optimizer
