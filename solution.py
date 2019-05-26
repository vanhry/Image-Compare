import os
import argparse
import numpy as np
from PIL import Image


parser = argparse.ArgumentParser(description='Test task on images similarity.')
parser.add_argument("--path", help="Path to dataset with images")
args = parser.parse_args()

dataset = args.path

quantize = 16 # for histogram
hash_size = 8 # for avg_hash function

def findpeaks(y):
    """
    Generate the indices of the peaks in a data line

    :param y: :class:`numpy.ndarray` histogram values
    :return: :class:`numpy.ndarray` the index values of the ridges in the line
    """

    dy = np.diff(y)

    dy_2 = np.array(np.where(dy == 0))
    if dy.size == dy_2.size:
        return []

    dy_a1 = np.append(dy, [0])
    dy_a2 = np.append([1], dy)

    index_a1 = np.array((dy_a1 <= 0).nonzero())
    index_a2 = np.array((dy_a2 > 0).nonzero())

    index = np.intersect1d(index_a1, index_a2)
    if len(index) == 0:
        return index

    if index[0] == 0:
        if dy[0] == 0:
            nonzero_index = (dy != 0).nonzero()

            if dy[nonzero_index[0][0]] > 0:
                index = index[1:]

    if index[-1] == np.size(y):
        if dy[-1] == 0:

            nonzero_index = (dy != 0).nonzero()
            if dy[nonzero_index[0][-1]] < 0:
                index = index[0:-2]

    # Get the values that are at the start of plateaus, or are peaks
    index_v = np.append([0], np.diff(index))
    index = np.compress(index_v != 1, index)

    return index

def avg_hash(img):
    """
    Return binary hash of image using average of pixels

    :param img: PIL image
    :return: class 'numpy.ndarray' with shape (hash_size**2,)
    """
    image = img.convert("L").resize((8, 8), Image.ANTIALIAS)
    pixels = np.asarray(image)
    avg = pixels.mean()
    bin_hash = pixels > avg
    return bin_hash.ravel()


def compare_avg_hash(hash_1, hash_2):
    """
    Return result of compare two hash arrays

    :param hash_1: class:`numpy.ndarray` with shape (hash_size**2,)
    :param hash_2: class:`numpy.ndarray` with shape (hash_size**2,)
    :return: class: 'int' count of difference element between two arrays
    """
    return np.count_nonzero(avg_hash(hash_1) != avg_hash(hash_2))


def hist_hash(img):
    """
    Return values of np histogram

    :param img: Pillow image
    :return: numpy array
    """
    return np.histogram(np.asarray(img).flatten(), bins=16)[0]


if __name__ == '__main__':

    all_images = os.listdir(dataset)
    for filename in all_images:
        current = Image.open(os.path.join(dataset, filename))
        for other_file in all_images:
            compare = Image.open(os.path.join(dataset, other_file))
            if filename == other_file:
                continue
            # for duplicate
            elif np.array_equal(current, compare):
                print(filename, other_file)
            # for modification
            elif compare_avg_hash(current, compare) == 0:
                print(filename, other_file)
            # for similar
            elif np.array_equal(findpeaks(hist_hash(current)), findpeaks(hist_hash(compare))):  # \
                # and np.array_equal(np.argsort(findpeaks(hist_hash(current))),np.argsort(findpeaks(hist_hash(compare)))):
                print(filename, other_file)
        all_images.remove(filename)
