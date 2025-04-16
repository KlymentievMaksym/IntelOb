import cv2
import matplotlib.pyplot as plt
import os
import pprint


def show_image(img):
    # plt.imshow(np.array(img))
    plt.imshow(img)
    plt.title(str(obj_id))
    plt.axis("off")
    plt.show()
    label = input("[!] Enter a descriptive name for this object: \n>>> ")
    return label


coil_dict = {}
for obj_id in range(1, 101):
    filename = f"obj{obj_id}__{0}.png"
    filepath = os.path.join(f"./Lab3/Data/coil-100/{filename}")
    img = cv2.imread(filepath)
    img = cv2.resize(img, (64, 64))
    img = img / 255.0
    coil_dict[obj_id] = show_image(img)

pprint.pprint(coil_dict)
