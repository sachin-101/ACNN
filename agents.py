import torch
import torch.nn as nn


class ParallelNets(nn.Module):
    """Branches of the Network"""

    def __init__(self, net1_channels=(1, 10, 20),
                 net2_channels=(1, 10, 20, 30),
                 kernel_size=5, stride=1, padding=2,
                 junction_channels=30):
        """
        Init all variables for class
        """
        super(ParallelNets, self).__init__()
        self.net1conv1 = nn.Sequential(
            nn.Conv2d(net1_channels[0], net1_channels[1],
                      kernel_size=kernel_size, stride=stride, padding=padding),
            nn.ReLU()
        )
        self.net1conv2 = nn.Sequential(
            nn.Conv2d(net1_channels[1], net1_channels[2],
                      kernel_size=kernel_size, stride=stride, padding=padding),
            nn.ReLU()
        )
        self.net2conv1 = nn.Sequential(
            nn.Conv2d(net2_channels[0], net2_channels[1],
                      kernel_size=kernel_size, stride=stride, padding=padding),
            nn.ReLU()
        )
        self.net2conv2 = nn.Sequential(
            nn.Conv2d(net2_channels[1], net2_channels[2],
                      kernel_size=kernel_size, stride=stride, padding=padding),
            nn.ReLU()
        )
        self.net2conv3 = nn.Sequential(
            nn.Conv2d(net2_channels[2], net2_channels[3],
                      kernel_size=kernel_size, stride=stride, padding=padding),
            nn.ReLU()
        )
        self.junction = nn.Conv2d(in_channels=net1_channels[-1],
                                  out_channels=junction_channels,
                                  kernel_size=28,
                                  stride=stride,
                                  padding=padding,
                                  bias=False)
