
from PIL import Image
import numpy as np

try:
    import PySpin
except:
    print('WARNING: PySpin is not intalled')
try:
    import thorlabs_apt as apt
except:
    print('WARNING: thorlabs_apt is not intalled')
try:
    import MMCorePy
except:
    print('WARNING: Micro-Manager is not installed')

def start_cam():
    ''' Get a camera instance for the Flir CM3 
    
    returns:
        camera instance
    '''
    system = PySpin.System.GetInstance()
    cam = system.GetCameras()[0]
    cam.Init()
    cam.BeginAcquisition()
    return cam

def close_cam(cam):
    cam.EndAcquisition()
    cam.DeInit()
    del cam

def get_frame():
    cam = start_cam()
    frame = cam.GetNextImage().GetNDArray()
    close_cam(cam)
    return frame

def get_mmc(cfg="../../config/scope_stage.cfg"):
    mmc = MMCorePy.CMMCore()
    mmc.loadSystemConfiguration(cfg)
    #mmc.setFocusDevice('FocusDrive')
    return mmc

def start_nr360s(motornumber=90917763):
    motor = apt.Motor(motornumber)
    # Set the Hardware Limit Switches 
    #   - Limit switch is activated when electrical
    #     continuity is broken in the reverse direction 
    #   - No Limit Switch in forward direction for NR360S
    motor.set_hardware_limit_switches(rev=3, fwd=1)
    motor.set_motor_parameters(steps_per_rev=200,
                                gear_box_ratio=1)
    # Set Stage Info
    #   - Min and Max pos limited to 0 and 360 degrees
    #   - units = mm
    #   - pitch = 5.4546 (from device manual)
    motor.set_stage_axis_info(min_pos=0.0,
                            max_pos=360.0,
                            units=1,
                            pitch=5.4546)
    # Set Homing Parameters
    #   - Homing direction is reverse
    #   - Limit Switch is reverse
    motor.set_move_home_parameters(direction=2,
                                lim_switch=1,
                                velocity=6,
                                zero_offset=0.6)
    motor.set_velocity_parameters(min_vel=0.0,
                                accn=2.7,
                                max_vel=5.4545)

    return motor

def start_mlj150(motornumber=49914180):
    motor = apt.Motor(motornumber)
    # Set the Hardware Limit Switches 
    #   - Limit switch is activated when electrical
    #     continuity is broken in the reverse direction 
    #     in both directions
    motor.set_hardware_limit_switches(rev=3, fwd=3)
    motor.set_motor_parameters(steps_per_rev=200,
                                gear_box_ratio=3)
    # Set Stage Info
    #   - Min and Max pos limited to 0 and 360 degrees
    #   - units = mm
    #   - pitch = 1 (from device manual)
    motor.set_stage_axis_info(min_pos=0.0,
                            max_pos=50.0,
                            units=1,
                            pitch=1)
    # Set Homing Parameters
    #   - Homing direction is reverse
    #   - Limit Switch is reverse
    motor.set_move_home_parameters(direction=2,
                                lim_switch=1,
                                velocity=5,
                                zero_offset=0.1)
    motor.set_velocity_parameters(min_vel=0.0,
                                accn=5,
                                max_vel=5)

    return motor

def bmp_from_poslist(positions, name, path,
                     radius=20,
                     image_width=1920,
                     image_height=1080):
    ''' Generates a 1-bit .bmp file

    args:
        positions: a PositionList() of the locations 
                   to illuminate
        name: name of the file
        path: location to save the .bmp file
        radius: radius of illuminated point
        image_width: number of pixels
        image_height: number of pixels
    '''
    bmp = np.zeros((1080,1920))
    for posit in positions:
        for i in range(image_height):
            for j in range(image_width):
                if ((np.abs(i-posit.y) < radius) and
                    (np.abs(j-posit.x) < radius)):
                    bmp[i][j] = 255

    im = Image.fromarray(bmp)
    im = im.convert('1')
    im.save(path+'/'+name+'.bmp')