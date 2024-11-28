import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def getMask(imagePath, threshold=128):
    image = Image.open(imagePath).convert("L")
    imageArray = np.array(image)
    mask = (imageArray > threshold).astype(int)
    return mask

# flowerMask = getMask('assets/simplePinkFlower.jpeg', threshold=215)
# plt.imshow(flowerMask, cmap='gray')
# plt.show()