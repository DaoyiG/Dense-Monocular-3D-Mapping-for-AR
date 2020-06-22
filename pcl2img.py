import open3d as o3d
import numpy as np
import cv2

pcd = o3d.io.read_point_cloud("./data/fined_pcds.ply")
# pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
# o3d.visualization.draw_geometries([pcd])

point = np.asarray(pcd.points).T
colors = np.asarray(pcd.colors)

fx = 7.188560000000e+02;
fy = 7.188560000000e+02;
cx = 6.071928000000e+02;
cy = 1.852157000000e+02;

pose = np.array([[9.999978e-01, 5.272628e-04, -2.066935e-03, -4.690294e-02],
                 [-5.296506e-04, 9.999992e-01, -1.154865e-03, -2.839928e-02],
                 [2.066324e-03, 1.155958e-03, 9.999971e-01, 8.586941e-01],
                 [0, 0, 0 ,1]])

intrinsic = np.array([[fx, 0., cx, 0],
                      [0., fy, cy, 0],
                      [0., 0., 1., 0]])
N = point.shape[1]
point_homo = np.row_stack((point, np.ones([1, N])))

print(np.min(point_homo[:,2]))

X_trans = pose.dot(point_homo)
X_trans = intrinsic.dot(X_trans)
depth = X_trans[2,:]
image_coordinate = ((X_trans/depth)[0:2,:]).T

# print(np.max(image_coordinate))

height = 376
width = 1241
image = np.zeros([height, width, 3])

for v in range(height):
    for u in range(width):
        pixel = image_coordinate[u*v, :]
        if int(pixel[0]) >= 0 and int(pixel[0]) < width and int(pixel[1]) >= 0 and int(pixel[1]) < height:
            image[v][u][:] = colors[u*v, :] * 255

cv2.imwrite("img.jpg",image)

# print(image)