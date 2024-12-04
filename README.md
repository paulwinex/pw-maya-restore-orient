# Maya Orient Tool

![Dialog](images/img1.png)

Allows you to restore the orientation of an object based on selected reference elements.
This tool is useful when the original object has been transformed in the scene
and the transformations have been frozen. For example, all geometry in the scene has been merged into a single object.
After separating the large object into individual objects, the Orient Tool will help you restore the transformations
of the original objects and move them to the center of the world coordinates.

### Installation
Copy the pw_restore_object_orient folder to the Maya scripts directory. For example, `~/maya/scripts`.

To launch in Maya, add a button with the following code:

```python
import pw_restore_object_orient
pw_restore_object_orient.show()
```

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

When selecting, try to choose reference elements that are on the axis of symmetry
or are symmetrically positioned relative to the central axis. When selecting multiple components, it makes sense to choose coplanar components (lie in the same plane).

## Controls

`Set Object` - Select the object you will work with. This can only be a Transform node type. If a group is selected, all manipulations will affect all objects in the group.

`Align Selected` - Align the object using the current selection.

`Align Selected To Axis` - Align the object using the current selection, with the selected reference element oriented along a specific axis. 
Hold **Shift** to invert the direction of this axis.

`Rotate` - Group of buttons for quick rotation and alignment of orientation.

`X/Y/Z` - Orient the object along the selected axis relative to the selected element. The calculated vector will be exactly along the specified axis.

`xz/xy/yz/yx/zy/zx` - Rotate the axis of the selected element to the selected plane along the shortest path.
Before pressing, hold **Shift** to rotate around the first axis, and **Ctrl** to rotate around the second axis.
For example, if you select an edge and press the xz button, the object will rotate with the selected edge to the xz plane along the shortest path.
If you hold **Shift** before pressing, the rotation will occur along the x-axis, if you hold **Ctrl**, the rotation axis will be the global z axis.
This allows you to maintain the original orientation along the specified axis.

`+180/+90/-90/-180` - Rotate along the specified axis by the specified angle.

`Bottom` - Move the object to the center of the coordinates along X and Z and align the lowest point to 0 along the Y axis.

`Center` - Move the center of the object to the center of the world coordinates.

`Selected` - Find the center of the selected elements and move it to the center of the world coordinates.

`Freeze` - Invoke the `Modify/Freeze Transformations` command for the current object and all child objects.

`Reset` - Reset the changes to the current object.

`Restore Transform` - Restore the original transformations. This option is available as long as the current object selection is not reset.

### Calculation of the Source Vector

From any supported combinations of selected components, a source vector or basis for rotation is always calculated.
For example, if 1 polygon is selected, its source vector is the normal of that polygon. If multiple polygons are selected,
the source vector is the averaged normal of those polygons.
When selecting an edge, the source vector is directed along that edge.
When selecting two points, the vector will point from one point to the other.

This should be considered when choosing reference components.

### Difference Between Rotation Commands

The `X/Y/Z` buttons always orient the source vector along the specified axis. They should be used as the primary rotation.

The `xz/xy/yz/yx/zy/zx` buttons rotate the reference vector to the projection of the specified plane. It is better to use them for corrective rotation.
When using the **Shift** and **Ctrl** modifiers, you can maintain the orientation relative to the global axes when projecting components onto the plane.


### TODO

- The projection onto a plane is not yet designed to work with polygons.
- Interface for aligning multiple identical objects according to one rule