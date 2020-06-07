import open3d as o3d
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import string


# im1 = Image.open(r'assets/depth.png')
# im1.save(r'assets/depth2.png')
def generate_pcd(color_img, depth_img, intrinsics):
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_img, depth_img, convert_rgb_to_intensity=False)
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, intrinsics)

    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    return pcd

def get_intrinsics(file_path):
    intrinsics = []
    file = open(file_path,"r", encoding='utf-8')
    line = file.readlines()
    for elem in line[0].split():
        elem = float(elem.strip(string.whitespace))
        intrinsics.append(elem)
    return intrinsics


if __name__ == "__main__":

    color_img = o3d.io.read_image("assets/rgb.png")
    depth_img = o3d.io.read_image("assets/depth2.png")
    intrinsics_list = get_intrinsics("assets/testintri.txt")

    fx = intrinsics_list[0]
    fy = intrinsics_list[4]
    cx = intrinsics_list[2]
    cy = intrinsics_list[5]
    width = 1392
    height = 512

    intrinsics = o3d.camera.PinholeCameraIntrinsic()
    intrinsics.set_intrinsics(width=width, height=height, fx=fx, fy=fy, cx=cx,cy=cy)

    pcd = generate_pcd(color_img, depth_img, intrinsics)
    o3d.io.write_point_cloud("assets/test.ply", pcd)

    o3d.visualization.draw_geometries([pcd])
