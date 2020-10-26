from io import BytesIO
from unittest import mock

import boto3
import os
import gzip
import numpy as np
import logging
logger = logging.getLogger()


def load_mnist(path, kind='train'):
    """Load MNIST data from `path`"""
    labels_path = os.path.join(path,
                               '%s-labels-idx1-ubyte.gz'
                               % kind)
    images_path = os.path.join(path,
                               '%s-images-idx3-ubyte.gz'
                               % kind)

    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8,
                               offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8,
                               offset=16).reshape(len(labels), 784)

    return images, labels


def mnist_s3(kind: str = 'train') -> (np.array, np.array):
    """
    Download MNIST from S3 Bucket

    Parameters
    ----------
    kind

    Returns
    -------

    """

    logger.info(f'Load mnist data from S3 bucket')

    # Note: endpoint url is only necessary in local development mode
    #   if we pass None AWS constructs the correct URL. For the local test pipeline it needs to be in the
    #   env variables
    endpoint = os.environ.get('ENDPOINT_S3', None)
    s3 = boto3.resource('s3', endpoint_url=endpoint)
    bucket = s3.Bucket(os.environ['DATA_BUCKET'])
    logger.info(f'Load data from {bucket}, endpoint {endpoint}')

    # Prefix depends on region and profile type
    prefix = f''
    logger.info(f'Getting file list in {prefix}')

    fn = f'mnist/{kind}-labels-idx1-ubyte.gz'
    obj = s3.Object(os.environ['DATA_BUCKET'], fn)
    n = obj.get()['Body'].read()
    gzipfile = gzip.GzipFile(fileobj=BytesIO(n))
    content = gzipfile.read()
    labels = np.frombuffer(content, dtype=np.uint8, offset=8)

    fn = f'mnist/{kind}-images-idx3-ubyte.gz'
    obj = s3.Object(os.environ['DATA_BUCKET'], fn)
    n = obj.get()['Body'].read()
    gzipfile = gzip.GzipFile(fileobj=BytesIO(n))
    content = gzipfile.read()
    images = np.frombuffer(content, dtype=np.uint8, offset=8)

    return images, labels


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    os.environ['ENDPOINT_S3'] = 'http://localhost:4566'
    os.environ['DATA_BUCKET'] = 'data'

    x, y = mnist_s3()

