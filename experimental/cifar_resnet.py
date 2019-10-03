import torch
import torch.nn as nn
import torch.nn.functional as F


class CifarResNet(nn.Module):
    """
        All in one ResNet model for training on CIFAR dataset.
        Implements ResNet-20, ResNet-32, ResNet-44, ResNet-56, ResNet-110.
    """

    def __init__(self, n):
        """
        Init all variables for class
        """
        super(CifarResNet, self).__init__()

        if n not in [3, 5, 7, 9, 11]:
            raise NotImplementedError('Resnet 20/32/44/56/110 only implemented. \
                                            Contact Sharan or Sachin, if u need any other model')
        self.n = n

        l = 1  # keeps count of layers added

        self.model = nn.Sequential()
        self.model.add_module(f'conv{l}', nn.Conv2d(3, 16, 3, stride=1, padding=1, bias=False))
        self.model.add_module(f'bn{l}', nn.BatchNorm2d(16))
        self.model.add_module(f'relu{l}', nn.ReLU())
        l += 1

        for _ in range(2 * n):
            self.model.add_module(f'conv{l}', nn.Conv2d(16, 16, 3, stride=1, padding=1, bias=False))
            self.model.add_module(f'bn{l}', nn.BatchNorm2d(16))
            self.model.add_module(f'relu{l}', nn.ReLU())
            l += 1
            self.model.add_module(f'conv{l}', nn.Conv2d(16, 16, 3, stride=1, padding=1, bias=False))
            self.model.add_module(f'bn{l}', nn.BatchNorm2d(16))
            l += 1
        self.model.add_module(f'downsample_conv{l}', nn.Conv2d(16, 32, 1, stride=2, bias=False))
        self.model.add_module(f'downsample_bn{l}', nn.BatchNorm2d(32))
        l += 1

        for _ in range(2 * n - 1):
            self.model.add_module(f'conv{l}', nn.Conv2d(16, 32, 3, stride=2, padding=1, bias=False))
            self.model.add_module(f'bn{l}', nn.BatchNorm2d(32))
            self.model.add_module(f'relu{l}', nn.ReLU())
            l += 1
            self.model.add_module(f'conv{l}', nn.Conv2d(32, 32, 3, stride=1, padding=1, bias=False))
            self.model.add_module(f'bn{l}', nn.BatchNorm2d(32))
            l += 1
        self.model.add_module(f'downsample_conv{l}', nn.Conv2d(32, 64, 1, stride=2, bias=False))
        self.model.add_module(f'downsample_bn{l}', nn.BatchNorm2d(64))
        l += 1

        for _ in range(2 * n - 1):
            self.model.add_module(f'conv{l}', nn.Conv2d(32, 64, 3, stride=2, padding=1, bias=False))
            self.model.add_module(f'bn{l}', nn.BatchNorm2d(64))
            self.model.add_module(f'relu{l}', nn.ReLU())
            l += 1
            self.model.add_module(f'conv{l}', nn.Conv2d(64, 64, 3, stride=1, padding=1, bias=False))
            self.model.add_module(f'bn{l}', nn.BatchNorm2d(64))
            l += 1

        self.avgpool = nn.AdaptiveAvgPool2d(output_size=(1, 1))

        self.fc = nn.Sequential(
            nn.Linear(64, 10),
            nn.LogSoftmax(dim=1)
        )

    # noinspection PyPep8Naming
    def forward(self, X):
        """
        forward propagation logic
        """

        layers = {name: module for name, module in self.model.named_modules()}
        id_dict = {f'identity{i}': None for i in range(1, 6 * self.n + 1)}

        out = layers['conv1'](X)
        out = layers['bn1'](out)
        out = layers['relu1'](out)

        for i in range(2, 6 * self.n + 2):
            id_dict[f'identity{i - 1}'] = out
            out = layers[f'conv{i}'](out)
            out = layers[f'bn{i}'](out)

            try:
                out = layers[f'relu{2 * i}'](out)
            except:
                try:
                    out = layers[f'relu{2 * i + 1}'](out)
                except:
                    try:
                        out = layers[f'relu{2 * i + 2}'](out)
                    except:
                        raise IndexError

            if i < 6 * self.n + 1:
                out = layers[f'conv{i + 1}'](out)
                out = layers[f'bn{i + 1}'](out)
                try:
                    out += id_dict[f'identity{i - 1}']
                except:
                    id_dict[f'identity{i - 1}'] = layers[f'downsample_conv{i}'](id_dict[f'identity{i - 1}'])
                out = F.relu(out)

        out = self.avgpool(out)
        out = torch.flatten(out, 1)
        out = self.fc(out)

        return out


model = CifarResNet(5)
print(model(torch.rand((1, 3, 32, 32))))
