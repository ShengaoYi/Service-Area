# -*- coding: utf-8 -*-
'''
@Time    : 2023/6/15 9:55
@Author  : Ericyi
@File    : ServiceArea.py

'''

import arcpy
arcpy.CheckOutExtension("network")

nds = r"\Road Network.gdb\Road\Beijing_road"
nd_layer_name = "RoadNetwork"
input_facilities = r"io.gdb\entrance"
output_polygons = r"io.gdb\ServiceAreaPolygons"

# Create a network dataset layer and get the desired travel mode for analysis
arcpy.nax.MakeNetworkDatasetLayer(nds, nd_layer_name)
nd_travel_modes = arcpy.nax.GetTravelModes(nd_layer_name)
travel_mode = nd_travel_modes["New Travel Mode"]

# Instantiate a ServiceArea solver object
service_area = arcpy.nax.ServiceArea(nd_layer_name)

# Set properties Based on distance
service_area.distanceUnits = arcpy.nax.DistanceUnits.Kilometers
# Set properties Based on time
# service_area.timeUnits = arcpy.nax.TimeUnits.Minutes

service_area.defaultImpedanceCutoffs = [5, 10, 15]
service_area.travelMode = travel_mode
service_area.outputType = arcpy.nax.ServiceAreaOutputType.Polygons
service_area.geometryAtOverlap = arcpy.nax.ServiceAreaOverlapGeometry.Split

# Load inputs
service_area.load(arcpy.nax.ServiceAreaInputDataType.Facilities, input_facilities)
# Solve the analysis
result = service_area.solve()

print(result)
# Export the results to a feature class
if result.solveSucceeded:
    result.export(arcpy.nax.ServiceAreaOutputDataType.Polygons, output_polygons)
else:
    print("Solve failed")
    print(result.solverMessages(arcpy.nax.MessageSeverity.All))