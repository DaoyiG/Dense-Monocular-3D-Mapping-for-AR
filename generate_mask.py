import cv2
import numpy as np

def generate_mask(img):

    img_single_channel = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, threshold = cv2.threshold(img_single_channel, 55, 255, cv2.THRESH_BINARY_INV)

    return threshold


# use deepfill v2 to do the image inpaint
if __name__ == '__main__':
    input_dir = 'data/tree_aug_sfmply.png'
    output_mask = 'data/tree_aug_mask.png'
    output_mask_resized = 'data/tree_aug_mask_resized.png'
    output_resized = 'data/tree_aug_resized.png'
    img_rgba = cv2.imread(input_dir, cv2.IMREAD_UNCHANGED)
    img_rgb = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2RGB)
    img_rgb_resized = cv2.resize(img_rgb, (680,512),interpolation=cv2.INTER_AREA)
    mask = generate_mask(img_rgb)
    mask_resized = cv2.resize(mask, (680,512), interpolation=cv2.INTER_AREA)
    cv2.imwrite(output_mask, mask)
    cv2.imwrite(output_resized, img_rgb_resized)
    cv2.imwrite(output_mask_resized, mask_resized)