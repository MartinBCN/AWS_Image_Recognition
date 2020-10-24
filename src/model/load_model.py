from pathlib import Path

import joblib


def get_model(s3: bool = True):
    """
    Wrapper for loading model. Purpose is to switch seamlessly between local development and production

    Parameters
    ----------
    s3

    Returns
    -------

    """
    if s3:
        model = None
    else:
        p = Path(__file__).parents[2] / Path('model/mnist.pkl')
        model = joblib.load(p)

    return model
