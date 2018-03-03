import time
import mss
from PIL import Image

start = time.time()
monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
sct_img = mss.mss().grab(monitor)
img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
end = time.time()
print(end-start)

