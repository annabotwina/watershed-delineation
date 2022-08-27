import arcpy
from arcpy import env
from arcpy.sa import *

## This tool calculates the drainage density for a specific basin shapefile.
## For this tool you will need a Digital Elevation Model(DEM), basin shapefile, and a projected coordinate system (unit: meters). 

basin = arcpy.GetParameterAsText(0)
dem = arcpy.GetParameterAsText(1)
coors = arcpy.GetParameterAsText(2)

## DEM to Stream Network Shapefile
fill = Fill(dem)
direction = FlowDirection(fill, "NORMAL")
accumulation = FlowAccumulation(direction)

## The con function is used to create an if/else statement on the input cells of a raster (flow accumulation).
## The Stream Network will be delineated. Cells which have more than 100 cells flowing into it, will be given a value of 1.

con = Con(accumulation, "1", "", "VALUE > 100")
stream_network = StreamToFeature(con, direction, "stream_network")
stream_clip = arcpy.analysis.Clip(stream_network, basin, "stream_clip")

## The stream_clip needs to be projected from a Geographic Projection System to a Projected Coordinate System
## This will convert the unit from degrees to meters in order to calculate the drainage density.

stream_project = arcpy.Project_management(stream_clip, "stream_project", coors)

## Before going further, check if the coordinate system used to project the shapefile is in meters, not feet or other.

desc = arcpy.Describe(stream_project)
sr = desc.spatialReference
unit = sr.linearUnitName

if unit == "Meter":
    arcpy.AddField_management(stream_project, "LENGTH_k", "DOUBLE")
else:
    arcpy.AddError("Coordinate System unit must be meter.")
    sys.exit(1)

## The Shape_Length is in meters. To convert the value to kilometers (preferred value) divide by 1000. Add to the new field.

with arcpy.da.UpdateCursor(stream_project, ["Shape_Length","LENGTH_k"]) as cursor:
    for row in cursor:
        row[1] = row[0] / 1000
        cursor.updateRow(row)

stream_lengths = []
with arcpy.da.SearchCursor(stream_project, ["LENGTH_k"]) as cursor:
    for row in cursor:
        stream_lengths.append(row)

## The values are in a tuple, in order to sum all the stream lengths, you must separate into a list.

stream_list = [x[0] for x in stream_lengths]
length_sum = sum(stream_list)

## Change Projection
basin_project = arcpy.Project_management(basin, "basin_project", coors)
arcpy.AddField_management(basin_project, "AREA_k", "DOUBLE")

## The Shape_Length is in square meters. To convert the value to square kilometers divide by 1000000. Add to the new field.

with arcpy.da.UpdateCursor(basin_project, ["Shape_Area","AREA_k"]) as cursor:
    for row in cursor:
        row[1] = row[0] / 1000000
        cursor.updateRow(row)

## Drainage Density Field and Calculations.
## Drainage Density = total length of all the streams and Rivers in a Drainage basin divided by the total area of the drainage basin.

arcpy.AddField_management(basin_project, "DD", "DOUBLE")
with arcpy.da.UpdateCursor(basin_project, ["AREA_k", "DD"]) as cursor:
    for row in cursor:
        row[1] = length_sum / row[0]
        if row[1] < 2:
            arcpy.AddMessage("Basin is very course.")
        elif row[1] > 2 and row[1] < 4:
            arcpy.AddMessage("Basin is course.")
        elif row[1] > 4 and row[1] < 6:
            arcpy.AddMessage("Basin is moderate.")
        elif row[1] > 6 and row[1] < 8:
            arcpy.AddMessage("Basin is fine.")    
        elif row[1] > 8:
            arcpy.AddMessage("Basin is very fine.")
        cursor.updateRow(row)
                                
