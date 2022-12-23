import matplotlib.pyplot as plt
im = plt.imread(image_name)
implot = plt.imshow(im)

# put a blue dot at (10, 20)
plt.scatter()

# put a red dot, size 40, at 2 locations:
plt.scatter(x=[30, 40], y=[50, 60], c='r', s=40)

plt.show()
def load_image():
