import matplotlib.pyplot as plt
from matplotlib.image import imread
import matplotlib.cm as cm
import numpy as np
from scipy import ndimage

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

def if_save(image,dataT,append_save):
    """
    this function is called inside the image operation functions and will save
    the transformed image

    position arguments
    ------------------
    image:          analyze_file class object
    dataT:          np.array, transformed image
    append_save:    string, is attached at the end of the file name of the
                    saved image

    output
    ------
    None
    """

    save_file   =   image.file_name + '_' + append_save
    if image.file_type != None: save_file += image.file_type

    fig =   plt.figure()
    plt.imshow(dataT)
    plt.axis('off')
    fig.savefig(save_file)
    plt.close()

def if_preview(image,dataT,append_preview,**kwargs):
    """
    this function is called inside the image operation functions and will
    preview the original image and the transformed image side by side.

    position arguments
    ------------------
    image:  analyze_file class object
    dataT:  np.array, transformed image

    output
    ------
    None
    """
    fig,ax  =   plt.subplots(1,2,figsize=(20,15))

    ax[0].imshow(image.data)
    ax[0].set_title('original image')

    ax[1].imshow(dataT)
    ax[1].set_title(append_preview + ' image')
    ax[1].axis('off')

    plt.tight_layout()
    plt.show()

#===============================================================================
"Operations"
#-------------------------------------------------------------------------------

def crop(image_path,**kwargs):
    """
    takes the pathway to an image, loads the image, and crops the image.

    position argument
    -----------------
    image_path: string, path/to/file.file_type

    keyword arguments
    -----------------
    up:         integer, desired starting index for axis = 0    [size * 1/4]
    down:       integer, desired ending index for axis = 0      [size * 3/4]
    left:       integer, desired starting index for axis = 1    [size * 1/4]
    right:      integer, desired starting index for axis = 1    [size * 3/4]
    save:       boolean, option to save the file with "_cropped" attached to
                original file designation [False]
    preview:    boolean, option to show the original and cropped image side by
                side [False]

    output
    ------
    None
    """

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

    dataT   =   image.data[up:down,left:right,:]

    if save:    if_save(image,dataT,'cropped')
    if preview: if_preview(image,dataT,'cropped')

def mirror(image_path,**kwargs):
    """
    takes the pathway to an image, loads the image, and mirrors the image along
    a desired axis.

    position argument
    -----------------
    image_path: string, path/to/file.file_type

    keyword arguments
    -----------------
    axis:       string, "horizontal" or "vertical" [horizontal]
    save:       boolean, option to save the file with "_cropped" attached to
                original file designation [False]
    preview:    boolean, option to show the original and cropped image side by
                side [False]

    output
    ------
    None
    """

    image   =   analyze_file(image_path)
    axis    =   "horizontal"
    save    =   False
    preview =   False

    if 'axis' in kwargs:    axis = kwargs['axis']
    if 'save' in kwargs:    save = kwargs['save']
    if 'preview' in kwargs: preview = kwargs['preview']

    if axis == 'horizontal':
        dataT           =   image.data[:,::-1,:]
        append_save     =   'mirror_h'
        append_preview  =   'horizontally mirrored'
    else:
        dataT           =   image.data[::-1,:,:]
        append_save     =   'mirror_v'
        append_preview  =   'vertically mirrored'

    if save:    if_save(image,dataT,append_save)
    if preview: if_preview(image,dataT,append_preview)

def rotate(image_path,**kwargs):
    """
    takes the pathway to an image, loads the image, and rotates the image by
    a certain angle.

    position argument
    -----------------
    image_path: string, path/to/file.file_type

    keyword arguments
    -----------------
    angle:      float or integer, angle of rotation (degrees) [90]
    save:       boolean, option to save the file with "_cropped" attached to
                original file designation [False]
    preview:    boolean, option to show the original and cropped image side by
                side [False]

    output
    ------
    None
    """

    image   =   analyze_file(image_path)
    angle   =   -90
    save    =   False
    preview =   False

    if 'angle' in kwargs:   angle = kwargs['angle']
    if 'save' in kwargs:    save = kwargs['save']
    if 'preview' in kwargs: preview = kwargs['preview']

    dataT   =   ndimage.interpolation.rotate(image.data,angle)

    if save:    if_save(image,dataT,'rotated')
    if preview: if_preview(image,dataT,'rotated')

def preview_color_breakdown(image_path,**kwargs):
    """
    takes the pathway to an image, loads the image, and breaks up the RGB
    components of the image.

    position argument
    -----------------
    image_path: string, path/to/file.file_type

    keyword arguments
    -----------------
    cmap:       string, matplotlib.cm color scheme ['binary']
    save:       boolean, option to save the file with "_cropped" attached to
                original file designation [False]
    preview:    boolean, option to show the original and cropped image side by
                side [True]

    output
    ------
    None
    """

    cmap    =   'binary'
    save    =   False
    preview =   True

    if 'cmap' in kwargs:    cmap = kwargs['cmap']
    if 'save' in kwargs:    save = kwargs['save']
    if 'preview' in kwargs: preview = kwargs['preview']

    image   =   analyze_file(image_path)
    red     =   image.data[:,:,0]
    green   =   image.data[:,:,1]
    blue    =   image.data[:,:,2]

    fig,ax  =   plt.subplots(2,2,figsize=(20,12))

    ax[0,0].imshow(image.data)
    ax[0,0].set_title('original image')

    ax[0,1].imshow(red, cmap=cmap)
    ax[0,1].set_title('red')

    ax[1,0].imshow(green, cmap=cmap)
    ax[1,0].set_title('green')

    ax[1,1].imshow(blue, cmap=cmap)
    ax[1,1].set_title('blue')

    for i in range(2):
        for j in range(2):
            ax[i,j].axis('off')

    plt.tight_layout()

    if save:
        save_file   =   image.file_name + '_colors'
        if image.file_type != None: save_file += image.file_type
        fig.savefig(save_file)

    if preview:
        plt.show()
    else:
        plt.close()
