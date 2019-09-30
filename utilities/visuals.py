import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import os
from PIL import Image
from torch.utils.data import DataLoader


def visualize(model, device, dataset, save_dir,
              num_visualize, features_resize=(28, 28),
              filters_resize=(12, 12)):
    """
    Generates images of output from first net(features network) and
    second net(filters network), and saves them in a directory
    """
    model.eval()
    data_loader = DataLoader(dataset=dataset, batch_size=1, shuffle=True)
    num_visualize = min(num_visualize, 10)  # Since too many images may fill up your disk

    with torch.no_grad():
        for i, (data, target) in enumerate(data_loader):
            if i == num_visualize:
                break
            data, target = data.to(device), target.to(device)
            output, params = model(data, return_ff=True)
            features, filters = params['features'], params['filters']
            save(features, filters, data, save_dir, features_resize, filters_resize)


# noinspection PyShadowingBuiltins
def save(features, filters, data, dir, features_resize, filters_resize):
    """
    saves the features and filters as images
    """

    batch_size = data.shape[0]
    num_features, num_filters = features.shape[1], filters.shape[1]

    for i in range(batch_size):
        img_dir = os.path.join(dir, f'Image_{i}')
        features_dir = os.path.join(img_dir, 'features_net1')
        filters_dir = os.path.join(img_dir, 'filters_net2')

        try:
            os.mkdir(img_dir)
        except FileExistsError:
            pass
        try:
            os.mkdir(features_dir)
        except FileExistsError:
            pass
        try:
            os.mkdir(filters_dir)
        except FileExistsError:
            pass

        img = Image.fromarray(np.uint8(data[i, 0].cpu().numpy() * 255))
        img.save(f'{img_dir}/img.jpg')

        for k in range(num_features):
            f_i = Image.fromarray(np.uint8(features[i, k].cpu().numpy() * 255))
            f_i = f_i.resize(features_resize)
            f_i.save(f'{features_dir}/feature_{k}.jpg')

        for j in range(num_filters):
            f_i = Image.fromarray(np.uint8(filters[i, j].cpu().numpy() * 255))
            f_i = f_i.resize(filters_resize)
            f_i.save(f'{filters_dir}/filter_{j}.jpg')


def plot_logs(logger, training_dir, test=False):
        
    file_name = "test" if test else "train"
    step, _, _ = logger  # Unpack values
    
    plt.figure(figsize=(5, 10))  # Make a 1:2 figure

    plt.subplot(211)
    plt.plot(logger[0], logger[1])
    plt.xlabel('Steps')
    plt.ylabel('Loss')
    plt.title('Test Loss' if test else 'Train Loss')
    # plt.text()    # TODO: Add name and hyperparams
    plt.axis([0, step[-1], 0, 1.5])
    plt.grid(True)

    plt.subplot(212)
    plt.plot(logger[0], logger[2])
    plt.xlabel('Steps')
    plt.ylabel('Acc')
    plt.title('Test Accuracy' if test else 'Train Accuracy')
    # plt.text()    # TODO: Add name and hyperparams
    plt.axis([0, step[-1], 85, 100])
    plt.grid(True)

    plt.savefig(f'{training_dir}/{file_name}')  # Write to PNG


def write_csv(logger, train_dir, test=False):
    file_name = "test" if test else "train"
    step, loss, accuracy = logger  # Unpack values
    logs = np.hstack((step, loss, accuracy))   
    log_df = pd.DataFrame(logs) 
    log_df.to_csv(f'{train_dir}/{file_name}.csv',
                    columns=['step', 'loss', 'accuracy'])  # Write to CSV