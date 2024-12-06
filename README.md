# Maya Restore Orient Tool

Allows you to restore the orientation of an object based on selected reference elements.
This tool is useful when the original object has been transformed in the scene
and the transformations have been frozen. For example, all geometry in the scene has been merged into a single object.
After separating the large object into individual objects, the Orient Tool will help you restore the transformations
of the original objects and move them to the center of the world coordinates.
You can also return the restored object to its original location in the scene, but with the correct transformations.

### Installation

Copy the `pw_restore_object_orient` folder to the Maya scripts directory, for example `~/maya/scripts`

To launch in Maya, add a button with this code

```python
import pw_maya_restore_orient
pw_maya_restore_orient.show()
```

### Usage

1. First, select an object in the scene. This should be a `Transform` node. It doesn't matter if it's a single object or a group. Click the `Set Object` button.
2. Switch to component selection mode and select reference elements.
   When selecting, try to choose elements that are on the axis of symmetry or are symmetrically positioned relative to the central axis.
   When selecting multiple components, it makes sense to choose coplanar components (lie in the same plane).
   A reference vector is created from the selected components, which is then used for alignment and rotation manipulations.
3. Select an operation and click the corresponding button in the dialog.

> The results of alignment operations will differ when the `Shift` and `Ctrl` modifiers are held.

### Reference Element Options

- 1 point
- 2 points
- 3 points
- 1 edge
- 2 edges
- multiple edges (more than 2)
- 1 face
- 1 point + 1 edge
- 1 point + 2 edges
- 2 faces
- multiple faces (more than 2)

#### Calculation of the Initial Vector

From any supported combination of selected components, an initial vector or basis for rotation is always calculated.
For example, if 1 polygon is selected, its initial vector is the **normal of that polygon**. If multiple polygons are selected,
the initial vector is the **average normal** of those polygons.
When an edge is selected, the initial vector is directed **along that edge**.
When two points are selected, the vector will be directed **from one point to the other**.

This should be considered when choosing reference components.

### Dialog Controls

![Dialog](images/img1.png)

#### Current Object

`Set Object` - Select the object you will work with. This can only be a `Transform` node.
If a group is selected, all manipulations will affect all objects in the group.
With the `Shift` key held, the current object will be reset.

#### Align Selected

`Quick Align` - Quickly align the object using the current selection. With the `Shift` key held, the reference vector is inverted.
Quick alignment selects the nearest world axis to the reference vector. Hold **Shift** to invert the alignment direction.

`X/Y/Z` - Align the object using the current selection, with the selected reference element oriented along the chosen axis.
Hold **Shift** to invert the direction of this axis.

#### Rotate Selected To

Group of buttons for quick rotation and orientation alignment.

`X/Y/Z` - Orient the object along the selected axis relative to the chosen element.
The calculated vector will be directed exactly along the specified axis.

`XZ/XY/YZ/YX/ZY/ZX` - Rotate the axis of the selected element to the chosen plane. Useful for correcting the orientation of the object
after primary alignment.

By default, the shortest path is chosen. The rotation axis will be perpendicular to the reference vector lying on the specified plane.
The `Shift` and `Ctrl` keys change the rotation axis. The chosen axis remains written on the button in uppercase.

For example, if you select an edge and press the `XZ` button, the object will rotate with the selected edge to the `xz` plane along the shortest path.
If you hold `Shift`, the text on the button will change to `Xz`, meaning the rotation will occur along the `X` axis.
If you hold `Ctrl`, the text will change to `xZ`, and the rotation axis will be the `Z` axis.

This allows you to maintain the original orientation along the specified axis.

`+90 / -90` - Rotate along the specified axis by the specified angle.
Pressing `Shift` changes the angle to 180, and pressing `Ctrl` also changes the angle to 180.

#### Set Origin To

`Base` - Move the object to the center of coordinates along `X` and `Z` and align the lowest point to 0 along the `Y` axis.

`Center` - Move the center of the object to the center of world coordinates.

`Selected` - Find the center of the selected elements and move it to the center of world coordinates.

#### Finalize

`Freeze` - Call the `Modify/Freeze Transformations` command for the current object and all child objects.

`Reset` - Reset the changes to the current object.

`Restore Transform` - Restore the original position of the object in the scene after restoring transformations.
This option is available after the `Freeze` command and before the current object selection is reset.
The object will be moved to its original position but with the correct transformations relative to the new orientation and position.

### API

> todo

### TODO

- Projection to the plane is not yet calculated for polygons
- Interface for aligning multiple identical objects according to one rule