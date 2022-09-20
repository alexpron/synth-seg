"""Replace the cortical grey matter (cGM) label of drawem9 segmentation using
the ribbon label derived from cGM/ white matter interface surface.

+ Ribbon is  a thinner than  the cortical grey matter label and more accurate
especially in the sulcus fundi. For further details about the ribbon
and cGM labels have a look at the dHCP preprocessing pipeline code
https://github.com/BioMedIA/dhcp-structural-pipeline and associated publication
(https://www.sciencedirect.com/science/article/abs/pii/S1053811918300545?via%3Dihub)
+ Since the ribbon is thinner, some voxels are left unlabelled.
These are considered as belonging to the cerebro-spinal fluid (CSF).

"""


import numpy as np
import nibabel as nib


def cgm_to_ribbon(drawem9, ribbon):
    """Replace the cortical grey matter (cGM) label of the drawem9 segmentation.
    :param drawem9: the drawem9 segmentation volume
    :type drawem9:  ndarray
    :param ribbon: the ribbon volume
    :type ribbon: ndarray
    :return:
    """

    result = drawem9.copy()
    # set old cortical grey matter (cGM) label to an impossible value
    result[drawem9 == 2] = 1000
    # set cortical ribbon value to cGM value for both hemispheres
    result[np.logical_or(ribbon == 3, ribbon == 42)] = 2
    # label the unlabelled
    result[result == 1000] = 1
    return result


def cgm_to_ribbon_volume(path_drawem, path_ribbon, path_fusion):
    """Volumic version of the cgm_to_ribbon function.

    :param path_drawem: path of the drawem9 seg volume
    :param path_ribbon: path of the cortical ribbon volume
    :param path_fusion: path of the fusion of both volume
    :return:
    """
    drawem9_vol = nib.load(path_drawem)
    drawem9 = drawem9_vol.get_fdata()
    ribbon_vol = nib.load(path_ribbon)
    ribbon = ribbon_vol.get_fdata()
    fusion = cgm_to_ribbon(drawem9, ribbon)
    nib.save(
        nib.Nifti1Image(fusion, drawem9_vol.affine, header=drawem9_vol.header),
        path_fusion,
    )
    pass


if __name__ == "__main__":

    import os
    import glob

    dir_dhcp = "/scratch/apron/data/datasets/dhcp"
    dir_fusion = "/scratch/apron/data/datasets"
    os.makedirs(dir_fusion, exist_ok=True)
    segmentations = glob.glob(
        os.path.join(dir_dhcp, "sub*", "ses*", "*desc-drawem9_space-T2w_dseg.nii.gz"),
        recursive=True,
    )
    print(len(segmentations))
    for seg in segmentations:
        ribbon = seg.replace("drawem9", "ribbon")
        if os.path.exists(ribbon) and os.path.exists(seg):
            filename = os.path.basename(ribbon)
            filename = filename.replace(
                "desc-drawem9_space-T2w_dseg", "desc-drawem9_modified_space-T2w_dseg"
            )
            path_fusion = os.path.join(dir_fusion, filename)
            try:
                cgm_to_ribbon_volume(seg, ribbon, path_fusion)
            except:
                print(filename, 'crashed')
