import matplotlib.pyplot as plt
from matplotlib.image import imread
import numpy as np

class analyze_file:

    def __init__(self,file_path):
        self.file_path  =   file_path
        self.data       =   imread(self.file_path)
        self.dimention  =   self.data.shape

        self.type_index =   self.file_path.rfind('.')
        if self.type_index > 1:
            self.file_type   =   self.file_path[self.type_index:]
            self.file_name   =   self.file_path[:self.type_index]
        else:
            self.file_type   =   None
            self.file_name   =   string

#===============================================================================
"Operations"
#-------------------------------------------------------------------------------

def crop(image_path,**kwargs):

    image   =   analyze_file(image_path)
    up      =   int( image.dimention[0]/4 )
    down    =   int( image.dimention[0]*(3/4) )
    left    =   int( image.dimention[1]/4 )
    right   =   int( image.dimention[1]*(3/4) )
    save    =   False
    preview =   False

    if 'up' in kwargs:      up = kwargs['up']
    if 'down' in kwargs:    down = kwargs['down']
    if 'left' in kwargs:    left = kwargs['left']
    if 'right' in kwargs:   right = kwargs['right']
    if 'save' in kwargs:    save = kwargs['save']
    if 'preview' in kwargs: preview = kwargs['preview']

    # import pdb
    # pdb.set_trace()

    dataT   =   image.data[up:down,left:right,:]

    if save:

        save_file   =   image.file_name + '_cropped'
        if image.file_type != None: save_file += image.file_type

        fig1    =   plt.figure()
        plt.imshow(dataT)
        fig1.savefig(save_file)
        plt.close()

    if preview:

        fig2,ax  =   plt.subplots(1,2,figsize=(20,15))

        ax[0].imshow(image.data)
        ax[0].set_title('un-cropped image')

        ax[1].imshow(dataT)
        ax[1].set_title('cropped image')

        plt.show()
