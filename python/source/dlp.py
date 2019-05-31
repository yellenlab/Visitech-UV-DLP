
import numpy as np

import align
import uv_utils


def main():
    mmc = uv_utils.get_mmc()
    theta_stage = uv_utils.start_nr360s() 
    # First we need to find the alignment marks
    pl = align.find_corners(mmc)
    # Find the rotation angle of the chip
    rotation = align.get_rotation_angle(pl[:1])
    theta_stage.move_to(theta_stage.position + np.rad2deg(rotation))

    

if __name__ == '__main__':
    main()