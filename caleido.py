#!/usr/bin/env python
# >>> image = gimp.image_list()[0]
# >>> layer = image.layers[0]
# >>> import sys
# >>> sys.path.append('/home/noctrum/noctrum_priv/GIMP_scripts')
# >>> import caleido
# >>> caleido.caleidoscope_this(image,layer)

from gimpfu import *
from gimpenums import ORIENTATION_HORIZONTAL,ORIENTATION_VERTICAL
from sys import exit
import math

# Dictionary with layer blend modes mapping
blend_modes = {
        "LAYER_MODE_NORMAL_LEGACY":0,
        "LAYER_MODE_DISSOLVE":1,
        "LAYER_MODE_BEHIND_LEGACY":2,
        "LAYER_MODE_MULTIPLY_LEGACY":3,
        "LAYER_MODE_SCREEN_LEGACY":4,
        "LAYER_MODE_OVERLAY_LEGACY":5,
        "LAYER_MODE_DIFFERENCE_LEGACY":6,
        "LAYER_MODE_ADDITION_LEGACY":7,
        "LAYER_MODE_SUBTRACT_LEGACY":8,
        "LAYER_MODE_DARKEN_ONLY_LEGACY":9,
        "LAYER_MODE_LIGHTEN_ONLY_LEGACY":10,
        "LAYER_MODE_HSV_HUE_LEGACY":11,
        "LAYER_MODE_HSV_SATURATION_LEGACY":12,
        "LAYER_MODE_HSL_COLOR_LEGACY":13,
        "LAYER_MODE_HSV_VALUE_LEGACY":14,
        "LAYER_MODE_DIVIDE_LEGACY":15,
        "LAYER_MODE_DODGE_LEGACY":16,
        "LAYER_MODE_BURN_LEGACY":17,
        "LAYER_MODE_HARDLIGHT_LEGACY":18,
        "LAYER_MODE_SOFTLIGHT_LEGACY":19,
        "LAYER_MODE_GRAIN_EXTRACT_LEGACY":20,
        "LAYER_MODE_GRAIN_MERGE_LEGACY":21,
        "LAYER_MODE_COLOR_ERASE_LEGACY":22,
        "LAYER_MODE_OVERLAY":23,
        "LAYER_MODE_LCH_HUE":24,
        "LAYER_MODE_LCH_CHROMA":25,
        "LAYER_MODE_LCH_COLOR":26,
        "LAYER_MODE_LCH_LIGHTNESS":27,
        "LAYER_MODE_NORMAL":28,
        "LAYER_MODE_BEHIND":29,
        "LAYER_MODE_MULTIPLY":30,
        "LAYER_MODE_SCREEN":31,
        "LAYER_MODE_DIFFERENCE":32,
        "LAYER_MODE_ADDITION":33,
        "LAYER_MODE_SUBTRACT":34,
        "LAYER_MODE_DARKEN_ONLY":35,
        "LAYER_MODE_LIGHTEN_ONLY":36,
        "LAYER_MODE_HSV_HUE":37,
        "LAYER_MODE_HSV_SATURATION":38,
        "LAYER_MODE_HSL_COLOR":39,
        "LAYER_MODE_HSV_VALUE":40,
        "LAYER_MODE_DIVIDE":41,
        "LAYER_MODE_DODGE":42,
        "LAYER_MODE_BURN":43,
        "LAYER_MODE_HARDLIGHT":44,
        "LAYER_MODE_SOFTLIGHT":45,
        "LAYER_MODE_GRAIN_EXTRACT":46,
        "LAYER_MODE_GRAIN_MERGE":47,
        "LAYER_MODE_VIVID_LIGHT":48,
        "LAYER_MODE_PIN_LIGHT":49,
        "LAYER_MODE_LINEAR_LIGHT":50,
        "LAYER_MODE_HARD_MIX":51,
        "LAYER_MODE_EXCLUSION":52,
        "LAYER_MODE_LINEAR_BURN":53,
        "LAYER_MODE_LUMA_DARKEN_ONLY":54,
        "LAYER_MODE_LUMA_LIGHTEN_ONLY":55,
        "LAYER_MODE_LUMINANCE":56,
        "LAYER_MODE_COLOR_ERASE":57,
        "LAYER_MODE_ERASE":58,
        "LAYER_MODE_MERGE":59,
        "LAYER_MODE_SPLIT":60,
        "LAYER_MODE_PASS_THROUGH":61,
        "LAYER_MODE_REPLACE":62,
        "LAYER_MODE_ANTI_ERASE":63
        }

# construct list of blending modes
blend_list = [blend_mode for blend_mode in blend_modes]


def get_layer_position(img, layer):
   """
   Given an image and a layer, returns the position in the layers stack of the layer.

   Parameters:
   img   : Image to work on
   layer : The layer in the image which position is requested

   Returns:
   int : position of the layer in the stack
   """
   pos = 0;
   for i in range(len(img.layers)):
       if(img.layers[i] == layer):
           pos = i
   return pos

def duplicate_layer(img,layer,name):
   """
   Gets a layer and duplicates it just over the source.
   Sets the name of the layer to the argument given.
   Returns the position of the created layer.

   Parameters:
   img   : image The current image.
   layer : layer to duplicate.
   name  : Name to use for the copy of the layer

   Returns:
   layer : The new layer
   """

   # Get the layer position.
   pos = get_layer_position(img,layer)
   newLayer = layer.copy()
   newLayer.name = name
   img.add_layer(newLayer, pos)
   return newLayer


def duplicate_and_rotate(img,layer,degrees,name,auto_center,center_x,center_y,mode):
    """
    Duplicates a given layer and returns it rotated degrees using center_x,center_y as pivot point

    Parameters:
    img         : The image containing the layer
    layer       : Layer to duplicate and rotate
    degrees     : AMount of degrees to rotate
    name        : Baame for the rotated layer
    auto_center : Rotate uses it (see rotate documentation)
    center_x    : X coordinate for the pivot point
    center_y    : Y coordinate for the pivot point

    Returns:
    layer : The resulting rotated layer
    """
    layer = duplicate_layer(img,layer, "{}_{}_ROTATED_0".format(name,degrees))
    layer.mode = mode
    pdb.gimp_item_transform_rotate(layer,math.radians(degrees),auto_center,center_x,center_y)
    pdb.gimp_image_raise_item_to_top(img,layer)
    return layer


def duplicate_and_flip(img,layer,type_of_flip,degrees,mode):
    """
    Duplicates a given layer and returns it flipped as indicated by type_of_flip

    Parameters:
    img          : The image containing the layer
    layer        : Layer to duplicate and rotate
    type_of_flip : Kind of flip, if it is vertical flip or horizontal flip
    degrees      : Number of degrees to use for the layer name

    Returns:
    layer : The resulting flipped layer
    """
    layer = duplicate_layer(img,layer,"{}_{}_{}_1".format(layer.name,degrees,type_of_flip))
    pdb.gimp_item_transform_flip_simple(layer,type_of_flip,TRUE,0)
    layer.mode = mode
    pdb.gimp_image_raise_item_to_top(img,layer)
    return layer


def fourFlip(img, layer, degrees,center_x, center_y,auto_center=TRUE,mode=36):
   """
   Takes an image, a layer and an amount of degrees and process the layer in the following way:
   - Duplicates the input layer, rotates it the given amount of degrees
   - Duplicates the previous layer and does a vertical flip over it
   - Duplicates previous layer and does an horizontal flip over it
   - Duplicates previous layer and does a vertical flip over it
   Returns a list with the layers in creation order

   Parameters:
   img         : The current image we want to work on
   layer       : The layer we want to use as a source for the transformations
   degrees     : The amount of degrees we want to rotate the layer
   center_x    : X coordinate of the pivot point
   center_y    : Y coordinate of the pivot point
   auto_center : if using auto pivot point (center of image) when rotating

   Returns:
   list<layer> : A list of layers in creation order
   """

   # Duplicate input layer, rotate it, apply Lighten only and raise it to the top
   # Do the same duplicating in cascade with flips instead of rotations: VERTICAL, HORIZONTAL, VERTICAL
   initial_layer = duplicate_and_rotate(img,layer,degrees,layer.name,auto_center,center_x,center_y,mode)
   vertical_flip_layer = duplicate_and_flip(img,initial_layer,ORIENTATION_VERTICAL,degrees,mode)
   horiz_flip_layer = duplicate_and_flip(img,vertical_flip_layer,ORIENTATION_HORIZONTAL,degrees,mode)
   vertical_flip_2_layer = duplicate_and_flip(img,horiz_flip_layer,ORIENTATION_VERTICAL,degrees,mode)

   # Return the four layers created in a list
   return [initial_layer,vertical_flip_layer,horiz_flip_layer,vertical_flip_2_layer]


def copy_visible_and_paste(img,result_layer):
    """
    Copy all visible layers from projection point and paste it in the given layer

    Parameters:
    img          : Image containing the layer
    result_layer : The layer to paste to

    Returns:
    Bool : True if copy was good, False otherwise
    """
    if pdb.gimp_edit_copy_visible(img):
        paste_me_layer = pdb.gimp_edit_paste(result_layer, TRUE)
        pdb.gimp_floating_sel_attach(paste_me_layer,result_layer)
        pdb.gimp_floating_sel_anchor(paste_me_layer)
    else:
        return False
    return True


def initialise_coords(img,coordinate):
    """
    Receives the value for a coordinate and returns the proper one.

    Parameters:
    img        : Image
    coordinate : coordinate to process

    Returns:
    int : The new value for the coordinate
    """
    if coordinate == -1:
        return img.width / 2
    return coordinate

def get_blend_int(n_mode):
    return blend_modes[blend_list[n_mode]]


def caleidoscope_this(img, layer, initial_rotation=0, iterations=90, interval=12, blend_mode=36, center_x=-1, center_y=-1):
   """ 
   This takes the top layer and duplicates it interations times and rotate it and flips (3 times per image)
   the idea is to create a caleidoscopic image out of the first layer.
   
   Parameters:
   img              : The current image.
   layer            : The layer of the image that is selected and source of the flips.
   initial_rotation : Start point for the rotation, default 0
   iterations       : End point of the rotation, default 90 (in degrees)
   interval         : Size of the steps in degrees, default 12
   """

   # Initialising
   auto_center = TRUE
   if (center_x != -1 or center_y != -1):
       auto_center = FALSE
   center_x = initialise_coords(img,center_x)
   center_y = initialise_coords(img,center_y)


   ####################
   # We create a layer from the original layer to store the result 
   layer_global_result = duplicate_layer(img,layer, "{}_RESULT".format(layer.name))
   layer_global_result.mode = 28

   # We duplicate the original layer as the source for the rotations
   layer_primera = duplicate_layer(img,layer, "{}_{}_primera".format(layer.name,0))
   layer_primera.mode = get_blend_int(blend_mode)
   
   # Moving result to the top so it remains in the proper position
   pdb.gimp_image_raise_item_to_top(img,layer_global_result)

   # Calculating the steps to do per rotation
   for currentDegrees in range(int(initial_rotation), int(iterations), interval):
       # To preserve the effect, we do the rotations and flips in different layers
       # And then copy all visible layers and paste it in the result layer.
       # The layers created in this loop are deleted at the end so the result layer
       # remains on top. This way, the next iteration will have the result layer
       # as bottom layer for the Lighten Only effect and changes are propagated
       # through iterations without piling up layers.
       layer_iter = fourFlip(img, layer_primera, currentDegrees, center_x, center_y,auto_center=auto_center,mode=get_blend_int(blend_mode))

       # Copy and paste from visible
       if not copy_visible_and_paste(img,layer_global_result):
           gimp.message("ERROR: Problems pasting visible layer")
           exit(1)

       # Layers cleanup
       for l in layer_iter:
           img.remove_layer(l)
       pdb.gimp_progress_update(float(currentDegrees * 100) / float(iterations - initial_rotation))
   img.remove_layer(layer_primera)

   # End progress.
   pdb.gimp_progress_end()

register(
   "python_fu_test_caleido",
   "Kaleidoscope effect",
   "Takes an image and replciates and flips creating a kaleiodscope effect. For the center coordinates, use -1 to auto calculate the center of the image",
   "Alex Sola",
   "Open source (Creative Commons)",
   "2021",
   "<Image>/Filters/Custom/caleidoscope",
   "*",
   [
       (PF_SLIDER, "initial_rotation", "Start angle for rotation (degrees)", 0, (0,360,1)),
       (PF_SLIDER, "iterations", "Max angle to rotate (degrees)", 90, (0,360,1)),
       (PF_INT, "interval", "Angle per rotation (degrees)", 12),
       (PF_OPTION, "blend_mode", "Blend mode for the layers",50, (blend_list)),
       (PF_INT, "center_x", "X coordinate for the pivot point", -1),
       (PF_INT, "center_x", "Y coordinate for the pivot point", -1)
   ],
   [],
   caleidoscope_this)

main()
