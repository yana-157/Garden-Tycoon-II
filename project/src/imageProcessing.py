import numpy as np
from PIL import Image
import matplotlib.pyplot as plt #source: ChatGPT

def getMask(imagePath, threshold=128):
    image = Image.open(imagePath).convert("L") #source: https://thecleverprogrammer.com/2021/06/08/convert-image-to-array-using-python/
    imageArray = np.array(image) #source: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html
    mask = (imageArray > threshold).astype(int) #source: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html#numpy.ndarray.astype
    return mask

# flowerMask = getMask('assets/simplePinkFlower.jpeg', threshold=215)
# plt.imshow(flowerMask, cmap='gray') #source: ChatGPT
# plt.show() #source: ChatGPT
