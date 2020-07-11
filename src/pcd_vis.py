import os
import sys
import numpy as np
import glob
import argparse
import open3d as o3d


def parse_args():
    parser = argparse.ArgumentParser(description='Visualize Reconstructed Scene')

    parser.add_argument('--scene_path', type=str,
                        help='path to a ply or obj file', required=True)
    parser.add_argument('--ext', type=str,
                        help='file extension', required=True)

    return parser.parse_args()


def visualization(args):
    assert args.scene_path is not None, \
        "You must specify the --scene_path parameter"
    if args.ext == 'ply':
        pcd = o3d.io.read_point_cloud(args.scene_path, format='ply')
        o3d.visualization.draw_geometries([pcd], window_name='Open3d Reconstruction')
    elif args.ext == 'obj':
        mesh = o3d.io.read_triangle_mesh(args.scene_path)
        o3d.visualization.draw_geometries([mesh], window_name='InfiniTAM Reconstruction')
    else:
        raise Exception("Unsupported file format: {}".format(args.ext))


if __name__ == "__main__":
    args = parse_args()
    visualization(args)
