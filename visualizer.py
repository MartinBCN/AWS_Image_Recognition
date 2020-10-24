import pandas as pd
import streamlit as st
from sklearn.metrics import confusion_matrix
from src.model.load_model import get_model
from src.utils.mnist_reader import load_mnist
import matplotlib.pyplot as plt
import numpy as np


def full_analysis(x, y, model):
    st.write('How does the test data set behave?')

    # Histogram of classes
    fig, ax = plt.subplots()
    ax.hist(y, bins=10)
    st.pyplot(fig)

    # Prediction
    y_hat = model.predict(x)
    score = model.score(x, y_hat)
    st.write(f'Test set accuracy: {score:.2f}')

    cm = confusion_matrix(y, y_hat)
    st.write(cm)


def examples(x, y, model):
    n = 4
    c = np.random.choice(x.shape[0], n)
    x = x[c, :]
    y = y[c]
    probabilities = model.predict_proba(x)

    fig, ax = plt.subplots(2, 4)
    for i in range(n):
        x0 = x[i, :].reshape(28, 28)
        ax[0, i].imshow(x0)
        ax[0, i].axis('off')

        df = pd.DataFrame({'Prob': probabilities[i], 'Label': range(10)})
        df = df.sort_values(by='Prob', ascending=False)
        df.index = range(10)
        df = df[:3]
        ax[1, i].bar(range(3), df['Prob'])
        ax[1, i].set_xticks(range(3))
        ax[1, i].set_xticklabels(list(df['Label']))

    plt.subplots_adjust(wspace=0.5)
    st.pyplot(fig)


def main():
    x, y = load_mnist('data/mnist', kind='t10k')
    model = get_model(s3=False)

    functions = {'Examples': examples, 'Dataset Analysis': full_analysis}
    fct = st.sidebar.selectbox('What would you like to do?', list(functions.keys()))
    fct = functions[fct]

    fct(x, y, model)


if __name__ == '__main__':
    main()
