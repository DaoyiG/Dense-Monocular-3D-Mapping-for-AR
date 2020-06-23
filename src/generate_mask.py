import cv2
import numpy as np
import numpy.ma as npm

def generate_mask(img):

    img_single_channel = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    cv2.imwrite("data/gray.png", img_single_channel)
    _, threshold = cv2.threshold(img_single_channel, 180, 255, cv2.THRESH_BINARY)
    _, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    h, w, _ = img.shape
    c_max = []
    max_area = 0
    max_cnt = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if (area > max_area):
            if (max_area != 0):
                c_min = []
                c_min.append(max_cnt)
                cv2.drawContours(threshold, c_min, -1,(0, 0, 0), cv2.FILLED)
            max_area = area
            max_cnt = cnt
        else:
            c_min = []
            c_min.append(cnt)
            cv2.drawContours(threshold, c_min,-1, (0,0,0), cv2.FILLED)
        # if (area < (h/200 * w/200)):
        #     c_min = []
        #     c_min.append(cnt)
        #
        #     cv2.drawContours(threshold, c_min, -1, (0, 0, 0), thickness=-1)
        #     continue

    c_max.append(cnt)

    cv2.drawContours(threshold, c_max, -1, (255, 255, 255), thickness=-1)
    mask_resized = cv2.resize(threshold, (680, 512), interpolation=cv2.INTER_AREA)
    cv2.imwrite("data/mask.png", mask_resized)
    return threshold



# use deepfill v2 to do the image inpaint
if __name__ == '__main__':
    input_dir = 'data/tree_aug_sfmply.png'
    output_mask = 'data/tree_aug_mask.png'
    output_mask_resized = 'data/tree_aug_mask_resized.png'
    output_resized = 'data/tree_aug_resized.png'

    mask2 = cv2.imread('data/mask2.PNG')
    mask3 = cv2.cvtColor(mask2, cv2.COLOR_RGB2GRAY)
    cv2.imwrite('data/mask3.png', mask3)
    img_rgba = cv2.imread(input_dir, cv2.IMREAD_UNCHANGED)

    img_rgb = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2RGB)
    img_rgb_resized = cv2.resize(img_rgb, (680,512),interpolation=cv2.INTER_AREA)
    mask = generate_mask(img_rgba)
    mask_resized = cv2.resize(mask, (680,512), interpolation=cv2.INTER_AREA)

    cv2.imwrite(output_mask, mask)
    cv2.imwrite(output_resized, img_rgb_resized)
    cv2.imwrite(output_mask_resized, mask_resized)