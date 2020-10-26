import numpy as np
import json
import logging
import os
import tempfile
from pathlib import Path

import boto3
import joblib
logger = logging.getLogger()


def prediction_handler(event, context) -> json:

    x = np.array(event['data'])
    logger.info(f'Test data shape: {x.shape}, {y.shape}')

    model_path = 'mnist.pkl'
    endpoint = os.environ.get('ENDPOINT_S3', None)
    s3_resource = boto3.resource('s3', endpoint_url=endpoint)
    bucket = s3_resource.Bucket(os.environ['MODEL_BUCKET'])

    with tempfile.TemporaryFile() as fp:
        bucket.download_fileobj(Fileobj=fp, Key=model_path)
        fp.seek(0)
        model = joblib.load(fp)

    result = model.predict(x)

    result = {'result': result.tolist()}

    return result


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

    from src.utils.mnist_reader import load_mnist
    x, y = load_mnist(path=Path(__file__).parents[1] / Path('data/mnist'), kind='t10k')
    event = {'data': x.tolist()}
    res = prediction_handler(event, {})
