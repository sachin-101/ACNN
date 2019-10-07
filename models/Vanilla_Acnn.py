import torch.nn as nn
# noinspection PyPep8Naming
from utilities.train_helpers import grouped_conv


class VanillaACNN(nn.Module):
    """Branches of the Network"""

    def __init__(self, net1_channels, net2_channels,
                 net1_kernels_size, net2_kernels_size,
                 net1_strides, net2_strides,
                 fc_units):

        super(VanillaACNN, self).__init__()


        # --------------------Features network------------------------#

        self.net1 = nn.Sequential()

        num_layers1 = len(net1_channels) - 1
        for i in range(num_layers1):
            self.net1.add_module(f'net1_conv{i}', nn.Conv2d(net1_channels[i],
                                                            net1_channels[i + 1],
                                                            net1_kernels_size[i],
                                                            stride=net1_strides[i]))
            self.net1.add_module(f'net1_relu{i}', nn.ReLU())

        # --------------------Filters network------------------------#

        self.net2 = nn.Sequential()

        num_layers2 = len(net2_channels) - 1
        for i in range(num_layers2):
            self.net2.add_module(f'net2_conv{i}', nn.Conv2d(net2_channels[i],
                                                            net2_channels[i + 1],
                                                            net2_kernels_size[i],
                                                            stride=net2_strides[i]))
            self.net2.add_module(f'net2_relu{i}', nn.ReLU())

        #-----------------------Grouped Conv-------------------------#

        self.bn = nn.Sequential(
            nn.BatchNorm2d(net2_channels[-1]),
            nn.ReLU()
        )

        # --------------------Classifier ---------------------------#

        self.fc = nn.Sequential()
        
        num_layers3 = len(fc_units) - 1
        for i in range(num_layers3):
            self.fc.add_module(f'fc_linear{i}', nn.Linear(fc_units[i],
                                                          fc_units[i + 1]))
            if i < num_layers3 - 1:
                self.fc.add_module(f'fc_relu{i}', nn.ReLU())
            else:
                self.fc.add_module(f'fc_softmax', nn.LogSoftmax(dim=1))

    # noinspection PyPep8Naming
    def forward(self, X):
        """
        Forward Prop
        :param X: Input dataset with batch dimension
        :return: Output of model and parameters
        """
        out1 = self.net1(X)
        out2 = self.net2(X)
        out = grouped_conv(out1, out2)
        out = self.bn(out.view(out2.shape[0], -1, out.shape[2], out.shape[3]))  # Batchnorm and relu
        out = self.fc(out.view(out2.shape[0], -1))
        return out
