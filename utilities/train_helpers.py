import torch
import torch.nn as nn
# noinspection PyPep8Naming
import torch.nn.functional as F
from torch.utils.data import DataLoader


def train(model: nn.Module, device,
          train_loader: torch.utils.data.DataLoader,
          optimizer: torch.optim.SGD,
          epoch, log_interval):
    """
    Performs one epoch of training on model
    :param model: Model class
    :param device: Device to train on. Use 'cuda:0' for GPU acceleration
    :param train_loader: Iterable dataset
    :param optimizer: Training agent for performing backprop
    :param epoch: Epoch number for logging purpose
    :param log_interval: Print stats for every
    :return:
    """
    model.train()
    running_loss = 0.0
    correct = 0
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
        correct += pred.eq(target.view_as(pred)).sum().item()
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        if batch_idx % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset), 100. * batch_idx / len(train_loader),
                loss.item()))

            # writer.add_scalar('training loss',  # writing to tensorboard
            #                   running_loss / log_interval,
            #                   (epoch - 1) * len(train_loader) + batch_idx)
            running_loss = 0.0

    print('\nTraining Accuracy: {}/{} ({:.4f}%)'.format(correct, len(train_loader.dataset),
                                                        100. * correct / len(train_loader.dataset)))


def test(model: nn.Module, device, test_loader: torch.utils.data.DataLoader):
    """
    Performs evaluation on dataset
    :param model: Model Class
    :param device: Device to test on. Use 'cuda:0' for GPU acceleration
    :param test_loader: Iterable Dataset
    :return:
    """
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))