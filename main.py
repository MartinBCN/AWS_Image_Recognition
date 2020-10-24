from pathlib import Path

import joblib

from src.model.train import train
from src.utils.mnist_reader import load_mnist
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    # DataLoader: to be replaced with S3
    x, y = load_mnist('data/mnist', kind='train')

    # Train: to be replaced with lambda
    model = train(x, y)
    model_path = Path('model/mnist.pkl')
    model_path.parents[0].mkdir(exist_ok=True, parents=True)

    # Again to be replaced with S3
    joblib.dump(model, model_path)


if __name__ == "__main__":
    main()