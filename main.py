import argparse
import errno
import game_dataset
import os
import torch
import torch.nn.functional as F
import renderScreen
import util


def train(device, model, train_loader, test_split, optimizer, epoch, args):
    model.train()
    num_pixelwise_correct_train = 0.
    num_correct_train = 0.
    batch_loss = 0.

    for batch_idx, (data, target) in enumerate(train_loader):
        # Forward
        data, target = data.to(device), target.to(device)
        out = model(data)  # raw output
        pred = out.argmax(dim=-1, keepdim=True)  # get pred latent state

        # Eval / Backward
        num_pixelwise_correct_train += pred.eq(target.view_as(pred)).sum().item() / 25.
        num_correct_train += pred.eq(target.view_as(pred)).all().item()
        loss = F.nll_loss(out.permute(0, 3, 1, 2), target, reduction='mean')
        batch_loss += loss.item()
        loss.backward()
        optimizer.step()

        # Periodically report loss and output example image
        if batch_idx % 100 == 0:
            print("BATCH: ", batch_idx)
            print("loss: ", batch_loss)
            batch_loss = 0

            prefix = "./data/eval/" + args.model + "/" + args.experiment + "/"
            try:
                os.makedirs(prefix)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(prefix):
                    pass
                else:
                    raise

            stimulus_directory = prefix + str(epoch) + "_" + str(batch_idx) + 'in.png'
            renderScreen.render_from_latent(target.cpu().numpy()[0, :, :], stimulus_directory)
            stimulus_directory = prefix + str(epoch) + "_" + str(batch_idx) + 'out.png'
            renderScreen.render_from_latent(pred.cpu().numpy()[0, :, :, 0], stimulus_directory)

    # Report epoch training acc
    print("\nPixelwise Train Acc: ", num_pixelwise_correct_train / ((1 - test_split) * len(train_loader.dataset)),
          " (", num_pixelwise_correct_train, "/", ((1 - test_split) * len(train_loader.dataset)), ")")
    print("Train Acc: ", num_correct_train / ((1 - test_split) * len(train_loader.dataset)),
          " (", num_correct_train, "/", ((1 - test_split) * len(train_loader.dataset)), ")\n")


def test(device, model, test_loader, test_split):
    model.eval()
    num_pixelwise_correct_test = 0.
    num_correct_test = 0.

    for batch_idx, (data, target) in enumerate(test_loader):
        data, target = data.to(device), target.to(device)
        out = model(data)
        pred = out.argmax(dim=-1, keepdim=True)
        num_pixelwise_correct_test += pred.eq(target.view_as(pred)).sum().item() / 25.
        num_correct_test += pred.eq(target.view_as(pred)).all().item()

    print("Pixelwise Test Acc: ", num_pixelwise_correct_test / (test_split * len(test_loader.dataset)),
          " (", num_pixelwise_correct_test, "/", (test_split * len(test_loader.dataset)), ")")
    print("Test Acc: ", num_correct_test / (test_split * len(test_loader.dataset)),
          " (", num_correct_test, "/", (test_split * len(test_loader.dataset)), ")\n\n\n")


def main():
    # Parse cmd line args
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True, help='the name of the desired model configuration')
    parser.add_argument('--experiment', type=str, required=True, help='the name of the desired experiment config')
    parser.add_argument('--batch_size', type=int, required=False, default=8, help='the train/test batch size')
    parser.add_argument('--test_split', type=float, required=False, default=0.2, help='the pct of data used for test')
    parser.add_argument('--epochs', type=int, required=False, default=5, help='the pct of data used for test')
    args = parser.parse_args()
    print(args.model)
    print(args.experiment)

    # Get model, optimizer and data
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("DEVICE:", device)
    model = util.models[args.model].to(device)
    optimizer = util.get_optimizer(model, args)

    train_loader, test_loader = \
        util.get_data_loaders(game_dataset.GameDataset(None, "./data/"),
                              args.batch_size,
                              args.test_split)

    # Train and evaluate
    for epoch in range(args.epochs):
        print("EPOCH", epoch)
        train(device, model, train_loader, args.test_split, optimizer, epoch, args)
        test(device, model, test_loader, args.test_split)


if __name__ == '__main__':
    main()
