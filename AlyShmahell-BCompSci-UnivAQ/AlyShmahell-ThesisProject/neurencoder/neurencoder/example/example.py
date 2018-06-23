from PIL import Image
import numpy as np
from grey_audio import *


if __name__ == '__main__':
	img = Image.open("italy_map_greyscale.png").convert("L")
	imgplot = plt.imshow(img)
	plt.show()
	
