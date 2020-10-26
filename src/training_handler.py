import logging
import os
import tempfile

import boto3
import joblib

from src.model.train import train
from src.utils.mnist_reader import mnist_s3

logger = logging.getLogger()


def train_handler(event, context) -> None:
    x, y = mnist_s3(kind='train')

    logger.info(f'Training data shape: {x.shape}, {y.shape}')

    model = train(x, y)
    model_path = 'mnist.pkl'

    endpoint = os.environ.get('ENDPOINT_S3', None)
    s3_resource = boto3.resource('s3', endpoint_url=endpoint)
    bucket = s3_resource.Bucket(os.environ['MODEL_BUCKET'])

    with tempfile.TemporaryFile() as fp:
        joblib.dump(model, fp)
        fp.seek(0)
        bucket.put_object(Key=model_path, Body=fp.read())

    logger.info(f'Saved model as {model_path} to bucket {bucket}')

    return


if __name__ == '__main__':

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    os.environ['ENDPOINT_S3'] = 'http://localhost:4566'
    os.environ['DATA_BUCKET'] = 'data'
    os.environ['MODEL_BUCKET'] = 'models'
    train_handler({}, {})
