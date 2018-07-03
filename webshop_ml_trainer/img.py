import cv2
import glob

desired_width = 455
desired_height = 700
input_folder = '/home/pcmill/Documenten/good-bad/data/training/normal'
output_folder = '/home/pcmill/Documenten/good-bad/new_data/training/normal'

def resize(image, width, height, key):
    im = cv2.imread(image)
    old_size = im.shape[:2] # old_size is in (height, width) format

    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    # new_size should be in (width, height) format

    im = cv2.resize(im, (new_size[1], new_size[0]))

    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)

    color = [0, 0, 0]
    new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    cv2.imwrite( output_folder + '/imageresized_{}.jpg'.format(key), new_im )

def resize_with_pad(imageFolder, height, width, i):
    def get_padding_size(image):
        h, w, _ = image.shape
        longest_edge = max(h, w)
        top, bottom, left, right = (0, 0, 0, 0)
        if h < longest_edge:
            dh = longest_edge - h
            top = dh // 2
            bottom = dh - top
        elif w < longest_edge:
            dw = longest_edge - w
            left = dw // 2
            right = dw - left
        else:
            pass
        return top, bottom, left, right

    image = cv2.imread(imageFolder)
    top, bottom, left, right = get_padding_size(image)
    BLACK = [0, 0, 0]
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)

    resized_image = cv2.resize(constant, (width, height))

    cv2.imwrite( output_folder + '/imageresized_{}.jpg'.format(i), resized_image )

for (i, image_file) in enumerate(glob.iglob(input_folder + '/*.png')):
        resize_with_pad(image_file, desired_height, desired_width, i)
