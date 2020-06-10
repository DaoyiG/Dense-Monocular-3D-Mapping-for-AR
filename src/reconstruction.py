import open3d as o3d
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import string
import os


def generate_inv_depth(depth_img):
    inv_depth = cv2.bitwise_not(depth_img)
    return inv_depth


def generate_pcd(color_img, depth_img, intrinsics, trans=np.eye(4, 4)):
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_img, depth_img, depth_scale=10, depth_trunc=0.09,
                                                                    convert_rgb_to_intensity=False)
    print(np.max(rgbd_image.depth))
    trans[0:3, 3] *= 5.0e-5
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, intrinsics, trans)
    # coordinates = np.asarray(pcd.points, dtype=np.float64)
    # pcd.transform(trans)
    return pcd


def get_intrinsics(file_path):
    intrinsics = []
    file = open(file_path, "r", encoding='utf-8')
    line = file.readlines()
    for elem in line[0].split():
        elem = float(elem.strip(string.whitespace))
        intrinsics.append(elem)
    return intrinsics


def generate_with_pose(frame_num, img_path, intrin, gt_global_poses, width, height):
    fx = intrin[0, 0]
    fy = intrin[1, 1]
    cx = intrin[0, 2]
    cy = intrin[1, 2]

    intrinsics = o3d.camera.PinholeCameraIntrinsic()
    intrinsics.set_intrinsics(width=width, height=height, fx=fx, fy=fy, cx=cx, cy=cy)

    pcds = o3d.geometry.PointCloud()

    for i in range(23, frame_num,1):
        print(img_path[i])
        depth_img = cv2.imread("assets/rectest/depth/" + img_path[i] + '.png')
        inv_depth = generate_inv_depth(depth_img)
        depth_img = o3d.geometry.Image(inv_depth)

        color_img = o3d.io.read_image("assets/rectest/rgb/" + img_path[i] + '.png')

        mat = gt_global_poses[i, :, :]
        inv_mat = np.linalg.inv(mat)
        pcd = generate_pcd(color_img, depth_img, intrinsics, inv_mat)
        pcd.estimate_normals()
        # if i == 0:
        #     pcd.paint_uniform_color([1, 0.706, 0])
        # if i == frame_num-1:
        #     pcd.paint_uniform_color([0, 0.706, 1])
        pcd_down = pcd.voxel_down_sample(voxel_size=5e-6)
        pcds += pcd_down

    pcds.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    return pcds


def generate():
    frame_num = 29

    gt_global_poses = np.loadtxt("assets/rectest/pose.txt").reshape(-1, 3, 4)
    gt_global_poses = gt_global_poses[0:frame_num + 1, :, :]
    gt_global_poses = np.concatenate(
        (gt_global_poses, np.zeros((gt_global_poses.shape[0], 1, 4))), 1)
    gt_global_poses[:, 3, 3] = 1

    intrin = np.asarray(get_intrinsics("assets/rectest/testintri.txt")).reshape(3, 3)
    intrin = np.concatenate((intrin, np.zeros((3, 1))), axis=1)
    intrin = np.concatenate((intrin, np.zeros((1, 4))), axis=0)
    intrin[3, 3] = 1

    img_path = os.listdir("assets/rectest/depth")
    for i in range(len(img_path)):
        img_path[i] = img_path[i].split('.')[0]
    img_path.sort()

    pcds = generate_with_pose(frame_num, img_path, intrin, gt_global_poses, width=1241, height=376)

    # pcds = generate_with_register(img_path, intrin, width=1241, height=376)

    o3d.io.write_point_cloud("assets/rectest/recon3.ply", pcds)
    o3d.visualization.draw_geometries([pcds])


if __name__ == "__main__":
    generate()
