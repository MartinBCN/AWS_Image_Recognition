from sklearn.base import BaseEstimator
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
import numpy as np
import logging

from sklearn.model_selection import train_test_split

logger = logging.getLogger()


def train(x: np.array, y: np.array) -> BaseEstimator:
    """
    Receive training data, try different models, return best-performing one

    Parameters
    ----------
    x
    y

    Returns
    -------

    """

    # For now I'm using a simple gbm with default values. This can be extended to a selection of models plus
    # hyper-parameter tuning

    logger.info(f'Shape x: {x.shape}, shape y: {y.shape}')

    # Split into train and validation set
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.9, random_state=42)
    logger.info(f'Shape x_train: {x_train.shape}, shape y_train: {y_train.shape}')
    logger.info(f'Shape x_test: {x_train.shape}, shape y_test: {y_test.shape}')
    logger.info(f'Classes: {np.unique(y)}')

    # Fit our model and check the validation score
    model = GradientBoostingClassifier()
    model.fit(x_train, y_train)

    score_train = model.score(x_train, y_train)
    logger.info(f'Score train: {score_train:.2f}')

    score_test = model.score(x_test, y_test)
    logger.info(f'Score train: {score_test:.2f}')

    return model
