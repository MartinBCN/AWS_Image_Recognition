import logging

from src.utils.mnist_reader import load_mnist


def train_handler(event, context) -> None:
    x, y = load_mnist('data/mnist', kind='train')
    return


if __name__ == '__main__':
    train_handler({}, {})
