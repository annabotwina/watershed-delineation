# watershed-delineation
Watershed delineation Script Tool
Drainage Density Documentation:
This tool calculates the drainage density for a specific basin shapefile.
For this tool you will need a Digital Elevation Model (DEM), basin shapefile, and a projected coordinate system.
Convert the DEM to a Projected Stream Network Shapefile, the clip the basin shapefile. 
Flow accumulation raster is used in the Con() function. The parameter “VALUE  > 100” sets an if/else statement that if a cell has more than 100 cells flowing into it,
the value of 1 is given. Else, the cell is given a value of NoData. This is a simple way to make the stream network more visible by eliminating small values. 
The stream_clip needs to be projected from a Geographic Projection System to a Projected Coordinate System. 
If the DEM and basin shapefile are already in a projected coordinate system, for tool parameters choose the current coordinate system. 
Else, this will convert the unit from degrees to meters in order to calculate the drainage density. 
The correct units for the density are kilometers / square kilometers. 
Before going further, the tool will  check if the coordinate system used to project the shapefile is in meters, not feet or other. 
Thus, any coordinate system used before or after the projection will be tested for the correct units. 
The projected stream clip has the field “Shape_Length”, which is in meters. 
A user can not edit this field, thus the user creates a new field “LENGTH_k”. 
Using the update cursor, the values of “Shape_Length” are divided by 1000 to update the new field. 
Using a search cursor, values are appended to a list. However, the values are within a tuple. 
Using a for condition, the user extracts the values from inside the tuple into a regular list. The values are then summed. 
“AREA_k” is a new field added to the projected basin shapefile. There is another field called “Shape_Area” in square meters, which cannot be edited. 
The user creates the new field and uses a update cursor to divide the “Shape_Area” value by 1000000 to convert to square kilometers. 
The last step is to add a Drainage Density (DD) field to the projected basin. 
With a update cursor, the sum of the stream lengths and “AREA_k” are divided and entered into the “DD” field. 
Using an if/elif conditional, a message is written after the tool is processed to tell the user the characteristic of the drainage density value. 
![image](https://user-images.githubusercontent.com/112206662/187042776-675a0c34-c994-4439-a233-aa78d90c11a7.png)
