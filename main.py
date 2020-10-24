from src.utils.mnist_reader import load_mnist

x, y = load_mnist('data/mnist', kind='t10k')

print(x.shape)