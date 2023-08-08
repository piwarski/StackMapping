import arcpy, sys, datetime, time, os

arcpy.env.overwriteOutput = True
#start_time = time.time()
#now = datetime.datetime.now()
#print('starting')

Polygons = arcpy.GetParameterAsText(0)
#Polygons = r'C:/Users/10214536/OneDrive - State of Ohio/Documents/StackMapping/StackMapping.gdb/SG_Polys_Results'
Lines_In = arcpy.GetParameterAsText(1)
#Lines_In = r'C:/Users/10214536/OneDrive - State of Ohio/Documents/StackMapping/StackMapping.gdb/SG_Lines_editing'
field ="LITH"
Output_GDB = arcpy.GetParameterAsText(2)
#Output_GDB = r'C:/Users/10214536/OneDrive - State of Ohio/Documents/StackMapping/Output.gdb'
date = str(datetime.date.today().strftime("_%Y_%m_%d"))

#Planarize Lines
arcpy.AddMessage("Planarizing Lines")
#print("Planarizing Lines")
Lines = arcpy.management.FeatureToLine(Lines_In, Output_GDB + os.sep + "PlanarizedLines_", "", "ATTRIBUTES")
arcpy.AddMessage("Planarizing Lines: Complete")
#print("Planarizing Lines: Complete")

#Create Uppermost Lith Label
SG_Poly_Samp = Polygons

# Local variables:
Unit1_Field_Added = SG_Poly_Samp
Slashes_Field_Added = SG_Poly_Samp
Unit2_Field_Added = Unit1_Field_Added
Unit3_Field_Added = Unit2_Field_Added
Unit4_Field_Added = Unit3_Field_Added
Unit5_Field_Added = Unit4_Field_Added
Slashes_Added = Slashes_Field_Added
Unit_1_Calc = Slashes_Added
Unit_2_Calc = Slashes_Added
Unit_3_Calc = Slashes_Added
DraftMapPolyJoined__3_ = Slashes_Added
DraftMapPolyJoined__6_ = Slashes_Added
DraftMapPolyJoined__4_ = Slashes_Added
Unit_4_Calc = Slashes_Added
DraftMapPolyJoined__2_ = Slashes_Added
Unit_4_Calc__2_ = Slashes_Added
DraftMapPolyJoined__7_ = Slashes_Added
DraftMapPolyJoined__8_ = DraftMapPolyJoined__2_
DraftMapPolyJoined__5_ = DraftMapPolyJoined__8_


#arcpy.AddMessage("Labeling")

arcpy.AddMessage("Labeling: adding unit fields")
#print("Labeling: adding unit fields")
# Process: Add Unit1 Field
arcpy.management.AddField(SG_Poly_Samp, "UNIT1", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Unit2 Field
arcpy.management.AddField(Unit1_Field_Added, "UNIT2", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Unit3 Field
arcpy.management.AddField(Unit2_Field_Added, "UNIT3", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Unit4 Field
arcpy.management.AddField(Unit3_Field_Added, "UNIT4", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Unit5 Field
arcpy.management.AddField(Unit4_Field_Added, "UNIT5", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddMessage("Labeling: adding unit fields Complete")
#print("Labeling: adding unit fields Complete")

# Process: Add Slashes Field
arcpy.AddMessage("Labeling: adding slash field")
#print("Labeling: adding slash field")
arcpy.management.AddField(SG_Poly_Samp, "LABELSLASHES", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddMessage("Labeling: adding slash field Complete")
#print("Labeling: adding slash field Complete")

# Process: Add Slashes
arcpy.AddMessage("Labeling: adding slashes")
#print("Labeling: adding slashes")
arcpy.management.CalculateField(Slashes_Field_Added, "LABELSLASHES", "!LABEL!+\"/\"+\"/\"+\"/\"+\"/\"+\"/\"+\"/\"+\"/\"+\"/\"+\"/\"", "PYTHON", "")
arcpy.AddMessage("Labeling: adding slashes Complete")
#print("Labeling: adding slashes Complete")

arcpy.AddMessage("Labeling: Calculating unit fields")
#print("Labeling: Calculating unit fields")
# Process: Calculate Field
arcpy.management.CalculateField(Slashes_Added, "UNIT1", "!LABELSLASHES!.strip().split(\"/\")[0]", "PYTHON", "\n\n") #removed "\\n\\n"

# Process: Calculate Field (2)
arcpy.management.CalculateField(Slashes_Added, "UNIT2", "!LABELSLASHES!.strip().split(\"/\")[1]", "PYTHON", "")

# Process: Calculate Field (3)
arcpy.management.CalculateField(Slashes_Added, "UNIT3", "!LABELSLASHES!.strip().split(\"/\")[2]", "PYTHON", "")

# Process: Calculate Field (4)
arcpy.management.CalculateField(Slashes_Added, "UNIT4", "!LABELSLASHES!.strip().split(\"/\")[3]", "PYTHON", "")

# Process: Calculate Field (5)
arcpy.management.CalculateField(Slashes_Added, "UNIT5", "!LABELSLASHES!.strip().split(\"/\")[4]", "PYTHON", "")

# Process: Unit1 Replace
arcpy.management.CalculateField(Slashes_Added, "UNIT1", "!UNIT1!.replace(\"-\",\"\").replace(\"0\",\"\").replace(\"1\",\"\").replace(\"2\",\"\").replace(\"3\",\"\").replace(\"4\",\"\").replace(\"5\",\"\").replace(\"6\",\"\").replace(\"7\",\"\").replace(\"8\",\"\").replace(\"9\",\"\")", "PYTHON", "")

# Process: Unit2 Replace
arcpy.management.CalculateField(Slashes_Added, "UNIT2", "!UNIT2!.replace(\"-\",\"\").replace(\"0\",\"\").replace(\"1\",\"\").replace(\"2\",\"\").replace(\"3\",\"\").replace(\"4\",\"\").replace(\"5\",\"\").replace(\"6\",\"\").replace(\"7\",\"\").replace(\"8\",\"\").replace(\"9\",\"\")", "PYTHON", "")

# Process: Unit3 Replace
arcpy.management.CalculateField(Slashes_Added, "UNIT3", "!UNIT3!.replace(\"-\",\"\").replace(\"0\",\"\").replace(\"1\",\"\").replace(\"2\",\"\").replace(\"3\",\"\").replace(\"4\",\"\").replace(\"5\",\"\").replace(\"6\",\"\").replace(\"7\",\"\").replace(\"8\",\"\").replace(\"9\",\"\")", "PYTHON", "")

# Process: Unit4 Replace
arcpy.management.CalculateField(Slashes_Added, "UNIT4", "!UNIT4!.replace(\"-\",\"\").replace(\"0\",\"\").replace(\"1\",\"\").replace(\"2\",\"\").replace(\"3\",\"\").replace(\"4\",\"\").replace(\"5\",\"\").replace(\"6\",\"\").replace(\"7\",\"\").replace(\"8\",\"\").replace(\"9\",\"\")", "PYTHON", "")

# Process: Unit5 Replace
arcpy.management.CalculateField(Slashes_Added, "UNIT5", "!UNIT5!.replace(\"-\",\"\").replace(\"0\",\"\").replace(\"1\",\"\").replace(\"2\",\"\").replace(\"3\",\"\").replace(\"4\",\"\").replace(\"5\",\"\").replace(\"6\",\"\").replace(\"7\",\"\").replace(\"8\",\"\").replace(\"9\",\"\")", "PYTHON", "")
arcpy.AddMessage("Labeling: Calculating unit fields Complete")
#print("Labeling: Calculating unit fields Complete")

# Process: Add Lith Field
arcpy.AddMessage("Labeling: adding lith field")
#print("Labeling: adding lith field")
arcpy.management.AddField(DraftMapPolyJoined__2_, "LITH", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddMessage("Labeling: adding lith filed complete")
#print("Labeling: adding lith filed complete")

# Process: Calc Lith Field
arcpy.AddMessage("Labeling: calculating lith field")
#print("Labeling: calculating lith field")
arcpy.CalculateField_management(DraftMapPolyJoined__8_, "LITH", "Findlith(!UNIT1!,!UNIT2!,!UNIT3!,!UNIT4!,!UNIT5!)", "PYTHON", "def Findlith(Unit1,Unit2,Unit3,Unit4,Unit5):\n    if \"(\" in Unit1.lower():\n        if \"(\" in Unit2.lower():\n            if \"(\" in Unit3.lower():\n                if \"(\" in Unit4.lower():\n                    return Unit5\n                else:\n                    return Unit4\n            else:\n                return Unit3\n        else:\n            return Unit2\n    else:\n        return Unit1\n            ")
arcpy.AddMessage("Labeling: calculating lith field compelete")
#print("Labeling: calculating lith field compelete")

#Test if LITH Field Contains NULL

arcpy.AddMessage("Labeling: Test if LITH field contains NULL")
#print("Labeling: Test if LITH field contains NULL")

LithField = "LITH"
cursor = arcpy.SearchCursor(Polygons)
NULL_List = []
for r in cursor:
    if r.getValue(LithField) is None or len(r.getValue(LithField)) == 0 :
        NULL_List.append(r.getValue(LithField))
    else:
        continue
NullCount = len(NULL_List)
arcpy.AddMessage(NullCount)
#print(NullCount)
if NullCount > 0:
    arcpy.AddError("Polygons 'LITH' Field contians NULL Values")
    #print("Polygons 'LITH' Field contians NULL Values")
    sys.exit("Polygons 'LITH' Field contians NULL Values")
else:
    arcpy.AddMessage("Polygons 'LITH' Field contians NO NULL Values: Continue")
    #print("Polygons 'LITH' Field contians NO NULL Values: Continue")
    
arcpy.AddMessage("Labeling: Test if LITH field contains NULL COMPLETE")
#print("Labeling: Test if LITH field contains NULL COMPLETE")

arcpy.AddMessage( "Labeling: Complete")
#print( "Labeling: Complete")

#Line Test
SpatialJoin = Output_GDB + "\SpatialJoin"
ID = "SpatialJoin_TARGET_FID"
LITH = "SpatialJoin_LITH"
SpatialJoin = Output_GDB + "\LineCheckOutput_" + date
SpatialJoin_lyr = "SpatialJoin_lyr"
Frequency = Output_GDB + "\Frequency"
FrequencyInitial = Output_GDB + "\FrequencyInitial"

#FieldMapping
fm = arcpy.FieldMap()
fm2 = arcpy.FieldMap()
fieldmappings = arcpy.FieldMappings()

fm.addInputField(Lines, "Linetype")

lt = fm.outputField
lt.name = "Linetype"
lt.aliasName = "Linetype"
fm.outputField = lt

fm2.addInputField(Polygons, "LITH")
fm2.mergeRule = "Join"
fm2.joinDelimiter = ","
l = fm2.outputField
l.name = "LITH"
l.aliasName = "LITH"
fm2.outputField = l

fieldmappings.addFieldMap(fm)
fieldmappings.addFieldMap(fm2)
#Spatial Join
arcpy.AddMessage("SpatialJoin")
#print("SpatialJoin")
SpatialJoin = arcpy.analysis.SpatialJoin(Lines, Polygons, SpatialJoin, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings, "SHARE_A_LINE_SEGMENT_WITH", "", "")
arcpy.AddMessage("SpatialJoin Complete")
#print("SpatialJoin Complete")

#LineCheck fn
#def fn (LineCheck):
#	lst = LineCheck.split(",")
#	if lst[1:] == lst[:-1]:
#		return "Dashed"
#	else:
#		return "Solid"

arcpy.AddMessage("AddField Line_Edge")
#print("AddField Line_Edge")
arcpy.management.AddField(SpatialJoin, "Line_Edge", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddMessage("AddField Line_Edge Complete")
#print("AddField Line_Edge Complete")

arcpy.AddMessage("AddField Line_Check")
#print("AddField Line_Check")
arcpy.management.AddField(SpatialJoin, "Line_Check", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddMessage("AddField Line_Check Complete")
#print("AddField Line_Check Complete")

arcpy.AddMessage("AddField Line_OK")
#print("AddField Line_OK")
arcpy.management.AddField(SpatialJoin, "Line_OK", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddMessage("AddField Line_OK Complete")
#print("AddField Line_OK Complete")

arcpy.AddMessage("Line Edge Check")
#print("Line Edge Check")
arcpy.management.CalculateField(SpatialJoin,"Line_Edge", "Check(!LITH!)", "PYTHON_9.3", "def Check(LITH):\n    lst = LITH.split(',')\n    if len(lst) == 1:\n        return 'Edge'\n    else:\n        return 'Not_Edge'" )
arcpy.AddMessage("Line Edge Check Complete")
#print("Line Edge Check Complete")

arcpy.AddMessage("Line Check")
#print("Line Check")
arcpy.management.CalculateField(SpatialJoin,"Line_Check", "Check(!LITH!)", "PYTHON_9.3", "def Check(LITH):\n    lst = LITH.split(',')\n    if lst[1:] == lst[:-1]:\n        return 'Dashed'\n    else:\n        return 'Solid'" )
arcpy.AddMessage("Line Check Complete")
#print("Line Check Complete")

arcpy.AddMessage("Compare old line type to new line type")
#print("Compare old line type to new line type")
arcpy.management.CalculateField(SpatialJoin, "Line_OK", "Check(!Line_Check!,!Linetype!) ", "PYTHON_9.3", "def Check( Line_Check , Linetype ):\n    if Line_Check != Linetype:\n        return 'False'\n    else:\n        return 'True'")
arcpy.AddMessage("Compare old line type to new line type Complete")
#print("Compare old line type to new line type Complete")

arcpy.management.Delete(Lines)
#print("--- %s seconds ---" % (time.time() - start_time))
#print('done')
