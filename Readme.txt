Name: StackMapping Toolbox
Author: Jason Piwarski
Creation Date: July 24, 2023

Change Log:
-7/24/23: Added derrivativeMapping, FlatFileModel, and LineTypeCheck tools to toolbox
-7/24/23: Updated FlatFile to use user input for 'no pits and quarries' when doing field mappings during append operation
-7/24/23: In FlatFile, checkString function was being called on L#Tx field, instead of L#T field. Corrected code
-7/25/23: In FlatFile, changed code to provide a layer thickness in the case of a dash.
-7/25/23: Fixed error in derrivativeMapping that didn't assign a value to L#noP field when parenthesis existed in L#S field
-7/25/23: In cases of layer being in parentheses, assign a value of 1 to L#T fields
-8/1/23: Renamed DERT2plus field to SGThickness and CarbDepth to CarbonateDepth. Set carbonate depth calculations to return a null value if the depth is equal to 10 or less