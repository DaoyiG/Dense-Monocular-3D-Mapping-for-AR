# Monodepth2

This is the reference PyTorch implementation for training and testing depth estimation models using the method described in

> **Digging into Self-Supervised Monocular Depth Prediction**
>
> [Clément Godard](http://www0.cs.ucl.ac.uk/staff/C.Godard/), [Oisin Mac Aodha](http://vision.caltech.edu/~macaodha/), [Michael Firman](http://www.michaelfirman.co.uk) and [Gabriel J. Brostow](http://www0.cs.ucl.ac.uk/staff/g.brostow/)  
>
> [ICCV 2019](https://arxiv.org/abs/1806.01260)

This code is for non-commercial use; please see the [license file](LICENSE) for terms.

If you find our work useful in your research please consider citing our paper:

```
@article{monodepth2,
  title     = {Digging into Self-Supervised Monocular Depth Prediction},
  author    = {Cl{\'{e}}ment Godard and
               Oisin {Mac Aodha} and
               Michael Firman and
               Gabriel J. Brostow},
  booktitle = {The International Conference on Computer Vision (ICCV)},
  month = {October},
year = {2019}
}
```



## 🖼️ Prediction for a single image

You can predict depth for a single image with:
```shell
  python test_simple.py --image_path assets/test_images/0000.png --output_depth assets/output_depth_rendering/ \
    --output_npy assets/output_npy_mono/ \
    --output_depth_o3d assets/output_depth_o3d/ \
    --output_depth_infi assets/output_depth_infinitam/ \
    --model_name mono_1024x320 \
    --no_cuda
```

On its first run this will download the `mono+stereo_1024x320` pretrained model into the `models/` folder.
We provide the following  options for `--model_name`:


| `--model_name`          | Training modality | Imagenet pretrained? | Model resolution  | KITTI abs. rel. error |  delta < 1.25  |
|-------------------------|-------------------|--------------------------|-----------------|------|----------------|
| [`mono_1024x320`](https://storage.googleapis.com/niantic-lon-static/research/monodepth2/mono_1024x320.zip)         | Mono              | Yes | 1024 x 320               | 0.115                 | 0.879          |


## 👩‍⚖️ License
Copyright © Niantic, Inc. 2019. Patent Pending.
All rights reserved.
Please see the [license file](LICENSE) for terms.
