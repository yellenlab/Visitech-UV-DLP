
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import json
from collections import defaultdict
from collections import OrderedDict
import time
import os


class PositionList:

    def __init__(self, sp=None, positions=None):
        if positions is not None:
            self.positions = positions
        else:
            self.positions = []
        if sp is not None and isinstance(sp, StagePosition):
            self.append(sp)
    
    def __len__(self):
        return len(self.positions)
    
    def __add__(self, other):
        posits = self.positions + other.positions
        return PositionList(positions=posits)
    
    def __iter__(self):
        return iter(self.positions)

    def __getitem__(self, key):
        return self.positions[key]
    
    def __setitem__(self, key, val):
        self.positions[key] = val
    
    def __delitem__(self, key):
        del self.positions[key]
    
    def __str__(self):
        string = ''
        for p in self.positions:
            string = string + str(p) + '\n'
        return string
    
    def append(self, item):
        self.positions.append(item)
    
    def insert(self, item, idx):
        self.positions.insert(idx, item)

    def visualize(self, xy=False):
        ''' Plots a 3D PositionList 
        arg:
            xy: bool - if True plot x vs y in 2D
        '''
        if xy is False:
            fig = plt.figure()
            plot = fig.add_subplot(111,projection='3d')

            xpos = [i.x for i in self.positions]
            ypos = [i.y for i in self.positions]
            zpos = [i.z for i in self.positions]

            plot.scatter(xpos,ypos,zpos)
            plot.set_xlabel('X')
            plot.set_ylabel('Y')
            plot.set_zlabel('Z')
        else:
            x = [p.x for p in self.positions]
            y = [p.y for p in self.positions]

            plt.scatter(x,y)
            plt.title('Position List')
            plt.xlabel('X')
            plt.ylabel('Y')
    
    def save(self, filename, path):
        ''' Save PositionList() as a json file
        '''
        # Convert to dict form 
        data = defaultdict(dict)
        for i, val in enumerate(self.positions):
            data[i]['x'] = val.x
            data[i]['y'] = val.y
            data[i]['z'] = val.z
            data[i]['theta'] = val.theta
            data[i]['numAxes'] = val.numAxes
            
        # Write to file
        with open(path + filename + '.json', 'w') as outfile:
            json.dump(data, outfile)
    
def load(filename, path):
    ''' Load PositionList() from json file 
    
    args:
        filename: string 
        path: directory to save file 
    returns:
        PositionList() 
    '''
    with open(path + filename + '.json') as f:
        data = json.load(f,object_pairs_hook=OrderedDict)
    sp = []
    for key, val in data.items():
        sp.append(StagePosition(x=val['x'], y=val['y'],
                                    z=val['z'], theta=val['theta']))
    return PositionList(positions=sp)

def current(mmc):
    ''' Gets the current stage position 
    
    arg:
        mmc: Micromanager instance
    returns:
        (x_pos, y_pos)
    '''
    return (mmc.getXPosition(), 
            mmc.getYPosition())

def set_pos(mmc, x=None, y=None, z=None):
    ''' Sets a microscope position
    args:
        - mmc instance
        - x (float)
        - y (float)
        - z (float) (default is None - keeps previous foucs)
    '''
    if z is not None:
        if x is None and y is None:
            mmc.setPosition(z)
            mmc.waitForSystem()
        else:
            mmc.setXYPosition(x,y)
            mmc.setPosition(z)
            mmc.waitForSystem()
    else:
        mmc.setXYPosition(x,y)
        mmc.waitForSystem()

class StagePosition:
    ''' Stores the data of one instantanious stage position 
    args:
        x: x position (optional)
        y: y position (optional)
        z: z position (optional)
        theta: theta position (optional)
    '''
    def __init__(self, x=None, y=None, z=None, theta=None):
        self.x = x
        self.y = y
        self.z = z
        self.theta = theta
        self.numAxes = 0
        for val in [x, y, z, theta]:
            if val is not None:
                self.numAxes = self.numAxes + 1
    
    def __eq__(self, other):
        ''' Allows use of == operator on two StagePositions
        '''
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z and
                self.theta == other.theta and
                self.numAxes == other.numAxes)
    
    def __str__(self):
        ''' Allows for print(StagePosition()) to see values
        '''
        if self.numAxes == 0:
            return 'No vals'
        if self.numAxes == 1:
            return "(" + str(self.x) + ")"
        elif self.numAxes == 2:
            return "(" + str(self.x) + "," + str(self.y) + ")"
        elif self.numAxes ==3:
            return ("(" + str(self.x) + "," + str(self.y) + 
                    "," + str(self.z) + ")")
        else:
            return ("(" + str(self.x) + "," + str(self.y) + 
                    "," + str(self.z) + "," + str(self.theta) + ")")
    
    def dist(self, other):
        ''' l2 distance between two stage postions. eg stage1.dist(stage2)
        args: 
            other: StagePosition()
        returns:
            distance between points 
        '''
        if self.numAxes == 0:
            raise ValueError('StagePosition does not have any values')
        if self.numAxes == 1:
            return np.sqrt(np.square(self.x - other.x))
        elif self.numAxes == 2:
            return np.sqrt(np.square(self.x - other.x) + 
                       np.square(self.y - other.y))
        elif self.numAxes ==3:
            return np.sqrt(np.square(self.x - other.x) + 
                       np.square(self.y - other.y) + 
                       np.square(self.z - other.z))
    
