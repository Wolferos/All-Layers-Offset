#!/usr/bin/env python

###################################################
##### All Layers Offset - GIMP plugin
##### (c) Wolferos Productions 2017
##### Forked from Group Offset by Vesa Kivimäki (http://registry.gimp.org/node/26996)
##### Released under GNU General Public License v2
###################################################

from gimpfu import *
import gtk

def debugMessage(Message):
    dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, Message)
    dialog.run()
    dialog.hide()

def py_group_offset_all(img, tdraw, xoffset, yoffset, edge, half):

        def dogroup(group):
              ll = group.layers
              for l in ll:
                 
                 if (type(l) == gimp.GroupLayer):
                   dogroup(l)
                 else:
                   if (edge == "wrap"):
                     pdb.gimp_drawable_offset(l, True, 0, xoffset, yoffset)
                   if (edge == "bg"):
                     pdb.gimp_drawable_offset(l, False, 0, xoffset, yoffset)
                   if (edge == "trans"):
                     pdb.gimp_drawable_offset(l, False, 1, xoffset, yoffset)

        def doAction():
              ll = img.layers
              for l in ll:
                 if (type(l) == gimp.GroupLayer):
                   dogroup(l)
                 else:
                   if (edge == "wrap"):
                     pdb.gimp_drawable_offset(l, True, 0, xoffset, yoffset)
                   if (edge == "bg"):
                     pdb.gimp_drawable_offset(l, False, 0, xoffset, yoffset)
                   if (edge == "trans"):
                     pdb.gimp_drawable_offset(l, False, 1, xoffset, yoffset)

        ### if half is set, set offsets to 1/2 image size
        if half:
           xoffset = (img.width // 2)
           yoffset = (img.height // 2)

        pdb.gimp_image_undo_group_start(img)
        doAction()
        pdb.gimp_image_undo_group_end(img)
        debugMessage("Operation completed")

register(
        "py_group_offset_all",
        "All Layers Offset",
        "Apply Offset to all Layers",
        "(c) Wolferos Productions",
        "GNU General Public License v2",
        "2012-2017",
        "<Image>/Group/All Layers Offset...", 
        "RGB*, GRAY*",
        [
                (PF_SPINNER, "xoffset", "X Offset", 0, (-32768, 32767, 1)),
                (PF_SPINNER, "yoffset", "Y Offset", 0, (-32768, 32767, 1)),
                (PF_RADIO, "edge", "Edge behaviour", "wrap", (
                     ("Wrap around", "wrap"),
                     ("Fill with bg", "bg"),
                     ("Transparent", "trans"))),
                (PF_TOGGLE, "half", "Offset by 1/2 of image", False)
        ],
        [],
        py_group_offset_all)

main()