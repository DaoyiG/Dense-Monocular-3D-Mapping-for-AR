import open3d as o3d
import numpy as np
import cv2

pcd = o3d.io.read_point_cloud("assets/play5.ply")
# pcd = o3d.io.read_point_cloud("./data/aug1.ply")

# pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
o3d.visualization.draw_geometries([pcd])

point = np.asarray(pcd.points).T
color = np.asarray(pcd.colors)
print(color.shape)
fx = 7.188560000000e+02
fy = 7.188560000000e+02
cx = 6.071928000000e+02
cy = 1.852157000000e+02

# pose = np.array([[9.999978e-01, 5.272628e-04, -2.066935e-03, -4.690294e-02],
#                  [-5.296506e-04, 9.999992e-01, -1.154865e-03, -2.839928e-02],
#                  [2.066324e-03, 1.155958e-03, 9.999971e-01, 8.586941e-01],
#                  [0, 0, 0 ,1]])
pose = np.eye(4)
intrinsic = np.array([[fx, 0., cx],
                      [0., fy, cy],
                      [0., 0., 1.]])
N = point.shape[1]
# print(N)
# point_homo = np.row_stack((point, np.ones([1, N])))

# print(np.max(point_homo[:,2]))

# X_trans = pose.dot(point_homo)
depth = point[2,:]
print(np.max(depth))
X_proj = point/depth
# print(X_proj)
height = 376
width = 1241
# X_trans = intrinsic.dot(X_trans)
# depth = X_trans[2,:]
image_coordinate = (intrinsic.dot(X_proj)[0:2, :]).T

u_coordinates = np.copy(image_coordinate[:, 0]).reshape(N).astype(np.int64)
v_coordinates = np.copy(image_coordinate[:, 1]).reshape(N).astype(np.int64)
u_coordinates = np.where(u_coordinates >= 1, u_coordinates, 0)
v_coordinates = np.where(v_coordinates >= 1, v_coordinates, 0)
u_coordinates = np.where(u_coordinates <= width-1, u_coordinates, 0)
v_coordinates = np.where(v_coordinates <= height-1, v_coordinates, 0)

# pixel_u >= 1 and pixel_u < width-1 and pixel_v >= 1 and pixel_v < height-1:
print(v_coordinates)
print(np.max(v_coordinates), np.min(v_coordinates))

image = np.ones([height, width, 3])
# for i in [1,0,-1]:
#     for j in [1,0, -1]:
image[list(v_coordinates), list(u_coordinates), :] = color * 255
print(image.shape)
# image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

cv2.imwrite("img.jpg", image)

# print(image)