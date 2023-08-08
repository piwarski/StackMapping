# -*- coding: utf-8 -*-

import arcpy, datetime, time, re, os
from sys import argv

print('starting')
arcpy.AddMessage('starting')
start_time = time.time()
now = datetime.datetime.now()

##Choose_Surficial_Points_To_Use=r"C:\Users\10214536\OneDrive - State of Ohio\Documents\StackMapping\FlatFile\SurficialGeologyOhio(DDF-8).gdb\SG_Polys" #Douglas said this is normally polygons, but using this because it has the right field and doesn't have the rest of the columns
##Output=r"C:\Users\10214536\OneDrive - State of Ohio\Documents\StackMapping\FlatFile\Output.gdb\SG_Flat_File_new"
##Output_Points_With_Type_Pit_Or_Quarry=r"C:\Users\10214536\OneDrive - State of Ohio\Documents\StackMapping\FlatFile\Output.gdb\Temp_Flat_File_No_Pits_Or_Quarries_new"

Choose_Surficial_Points_To_Use = arcpy.GetParameterAsText(0)
Output = arcpy.GetParameterAsText(1)

path = os.path.dirname(os.path.realpath(Output))

Output_Points_With_Type_Pit_Or_Quarry = path + os.sep + 'tempFile_delete'    

# To allow overwriting outputs change overwriteOutput option to True.
arcpy.env.overwriteOutput = True

# Process: Select Only Points with Labels (Select) (analysis)
t = time.process_time()
arcpy.analysis.Select(in_features=Choose_Surficial_Points_To_Use, out_feature_class=Output, where_clause="NOT label='Pit' AND NOT label='Quarry'")
print('Select Only Points with Labels (Select):' + str(time.process_time() - t))
arcpy.AddMessage('Select Only Points with Labels')

# Process: Add Field (Add Field) (management)
t = time.process_time()
Test_SG_Labels_Selects = arcpy.management.AddField(in_table=Output, field_name="LABELSLASHES", field_type="TEXT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
print('Add Field (Add Field) (management):' + str(time.process_time() - t))
arcpy.AddMessage('Add LABELSLASHES Field')

# Process: Add Slashes (Calculate Field) (management)
t = time.process_time()
Slashes_Added = arcpy.management.CalculateField(in_table=Test_SG_Labels_Selects, field="LABELSLASHES", expression="!LABEL!+\"/\"+\"/\"+\"/\"+\"/\"+\"/\"+\"/\"+\"/\"", expression_type="PYTHON", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]
print('Add Slashes (Calculate Field):' + str(time.process_time() - t))
arcpy.AddMessage('Add Slashes')

#Create L1-L7 fields
t = time.process_time()
arcpy.management.AddFields(
    Slashes_Added, 
    [['L1', 'TEXT'], 
     ['L2', 'TEXT'],
     ['L3', 'TEXT'],
     ['L4', 'TEXT'],
     ['L5', 'TEXT'],
     ['L6', 'TEXT'],
     ['L7', 'TEXT']])
print('Added Fields L1-L7:' + str(time.process_time() - t))
arcpy.AddMessage('Added Fields L1-L7')

#Calculate data for L1-L7 fields
t = time.process_time()
arcpy.management.CalculateFields(Slashes_Added,"PYTHON3",[
                                 ['L1','!LABELSLASHES!.strip().split(\"/\")[0]'],
                                 ['L2','!LABELSLASHES!.strip().split(\"/\")[1]'],
                                 ['L3','!LABELSLASHES!.strip().split(\"/\")[2]'],
                                 ['L4','!LABELSLASHES!.strip().split(\"/\")[3]'],
                                 ['L5','!LABELSLASHES!.strip().split(\"/\")[4]'],
                                 ['L6','!LABELSLASHES!.strip().split(\"/\")[5]'],
                                 ['L7','!LABELSLASHES!.strip().split(\"/\")[6]']])
print('Calculate L1-L7:' + str(time.process_time() - t))
arcpy.AddMessage('Calculate L1-L7')

#Create L1G-L7G fields
t = time.process_time()
arcpy.management.AddFields(
    Slashes_Added, 
    [['L1G', 'TEXT'], 
     ['L2G', 'TEXT'],
     ['L3G', 'TEXT'],
     ['L4G', 'TEXT'],
     ['L5G', 'TEXT'],
     ['L6G', 'TEXT'],
     ['L7G', 'TEXT']])
print('Addded Fields L1G-L7G:' + str(time.process_time() - t))
arcpy.AddMessage('Addded Fields L1G-L7G')

#Calculate data for L1-L7 fields
t = time.process_time()
expression = '.replace(\"-\",\"\").replace(\"(\",\"\").replace(\")\",\"\").replace(\"0\",\"\").replace(\"1\",\"\").replace(\"2\",\"\").replace(\"3\",\"\").replace(\"4\",\"\").replace(\"5\",\"\").replace(\"6\",\"\").replace(\"7\",\"\").replace(\"8\",\"\").replace(\"9\",\"\")'
arcpy.management.CalculateFields(Slashes_Added,"PYTHON3",[
                                 ['L1G',"!L1!"+expression],
                                 ['L2G',"!L2!"+expression],
                                 ['L3G',"!L3!"+expression],
                                 ['L4G',"!L4!"+expression],
                                 ['L5G',"!L5!"+expression],
                                 ['L6G',"!L6!"+expression],
                                 ['L7G',"!L7!"+expression]])
print('Calculate L1G-L7G:' + str(time.process_time() - t))
arcpy.AddMessage('Calculate L1G-L7G')

#Create L1Tx-L7Tx fields
t = time.process_time()
arcpy.management.AddFields(
    Slashes_Added, 
    [['L1Tx', 'TEXT'], 
     ['L2Tx', 'TEXT'],
     ['L3Tx', 'TEXT'],
     ['L4Tx', 'TEXT'],
     ['L5Tx', 'TEXT'],
     ['L6Tx', 'TEXT'],
     ['L7Tx', 'TEXT']])
print('Addded Fields L1Tx-L7Tx:' + str(time.process_time() - t))
arcpy.AddMessage('Addded Fields L1Tx-L7Tx')

#Combine two codeblocks below into one
t = time.process_time()
codeblock = """import re
def calc(Lnumber):
    contains_alpha = Lnumber.isalpha()
    contains_dash = False
    contains_parentheses = False
    if '-' in Lnumber:
        contains_dash = True
    if '(' in Lnumber:
        contains_parentheses = True
    Ldigits = re.sub('\\D', '', Lnumber)
    if len(Ldigits) == 0 and contains_alpha:
        return '1'
    elif len(Ldigits) == 0 and contains_dash:
        return '1'
    elif len(Ldigits) == 0 and contains_parentheses:
        return '1'
    return Ldigits"""
labelSelects = arcpy.management.CalculateFields(Slashes_Added,"PYTHON3",[
                                 ['L1Tx',"calc(!L1!)"],
                                 ['L2Tx',"calc(!L2!)"],
                                 ['L3Tx',"calc(!L3!)"],
                                 ['L4Tx',"calc(!L4!)"],
                                 ['L5Tx',"calc(!L5!)"],
                                 ['L6Tx',"calc(!L6!)"],
                                 ['L7Tx',"calc(!L7!)"]],codeblock)
print('Calculate L1Tx1-L7Tx:' + str(time.process_time() - t))
arcpy.AddMessage('Calculate L1Tx1-L7Tx')

#Create fields for L1t-L7T
t = time.process_time()
arcpy.management.AddFields(
    Slashes_Added, 
    [['L1T', 'SHORT'], 
     ['L2T', 'SHORT'],
     ['L3T', 'SHORT'],
     ['L4T', 'SHORT'],
     ['L5T', 'SHORT'],
     ['L6T', 'SHORT'],
     ['L7T', 'SHORT']])
print('Addded Fields L1T-L7T:' + str(time.process_time() - t))
arcpy.AddMessage('Addded Fields L1T-L7T')

#Calculate data for L1T-L7T fields
t = time.process_time()
codeblock = """def checkString(L_Tx):
                    if L_Tx.isnumeric():
                        return float(L_Tx)
                    else:
                        return 0"""

arcpy.management.CalculateFields(Slashes_Added,"PYTHON3",[
                                 ['L1T','checkString(!L1Tx!)'],
                                 ['L2T','checkString(!L2Tx!)'],
                                 ['L3T','checkString(!L3Tx!)'],
                                 ['L4T','checkString(!L4Tx!)'],
                                 ['L5T','checkString(!L5Tx!)'],
                                 ['L6T','checkString(!L6Tx!)'],
                                 ['L7T','checkString(!L7Tx!)']],codeblock)
print('Convert L1T-L7T:' + str(time.process_time() - t))
arcpy.AddMessage('Convert L1T-L7T')

#Create fields for L1S-L7S fields
t = time.process_time()
arcpy.management.AddFields(
    Slashes_Added, 
    [['L1S', 'TEXT'], 
     ['L2S', 'TEXT'],
     ['L3S', 'TEXT'],
     ['L4S', 'TEXT'],
     ['L5S', 'TEXT'],
     ['L6S', 'TEXT'],
     ['L7S', 'TEXT']])
print('Addded Fields L1S-L7S:' + str(time.process_time() - t))
arcpy.AddMessage('Addded Fields L1S-L7S')

#Calculate data for L1S-L7S fields
expression='.replace(\"a\",\"\").replace(\"b\",\"\").replace(\"c\",\"\").replace(\"d\",\"\").replace(\"e\",\"\").replace(\"f\",\"\").replace(\"g\",\"\").replace(\"h\",\"\").replace(\"i\",\"\").replace(\"j\",\"\").replace(\"k\",\"\").replace(\"l\",\"\").replace(\"m\",\"\").replace(\"n\",\"\").replace(\"o\",\"\").replace(\"p\",\"\").replace(\"q\",\"\").replace(\"r\",\"\").replace(\"s\",\"\").replace(\"t\",\"\").replace(\"u\",\"\").replace(\"v\",\"\").replace(\"w\",\"\").replace(\"x\",\"\").replace(\"y\",\"\").replace(\"z\",\"\").replace(\"A\",\"\").replace(\"B\",\"\").replace(\"C\",\"\").replace(\"D\",\"\").replace(\"E\",\"\").replace(\"F\",\"\").replace(\"G\",\"\").replace(\"H\",\"\").replace(\"I\",\"\").replace(\"J\",\"\").replace(\"K\",\"\").replace(\"L\",\"\").replace(\"M\",\"\").replace(\"N\",\"\").replace(\"O\",\"\").replace(\"P\",\"\").replace(\"Q\",\"\").replace(\"R\",\"\").replace(\"S\",\"\").replace(\"T\",\"\").replace(\"U\",\"\").replace(\"V\",\"\").replace(\"W\",\"\").replace(\"X\",\"\").replace(\"Y\",\"\").replace(\"Z\",\"\").replace(\"0\",\"\").replace(\"1\",\"\").replace(\"2\",\"\").replace(\"3\",\"\").replace(\"4\",\"\").replace(\"5\",\"\").replace(\"6\",\"\").replace(\"7\",\"\").replace(\"8\",\"\").replace(\"9\",\"\")'    
lastCalc = arcpy.management.CalculateFields(Slashes_Added,"PYTHON3",[
                                 ['L1S','!L1!'+expression],
                                 ['L2S','!L2!'+expression],
                                 ['L3S','!L3!'+expression],
                                 ['L4S','!L4!'+expression],
                                 ['L5S','!L5!'+expression],
                                 ['L6S','!L6!'+expression],
                                 ['L7S','!L7!'+expression]])
print('Convert for L1S-L7S:' + str(time.process_time() - t))
arcpy.AddMessage('Convert for L1S-L7S')

# Process: Select Only Points with Labels (2) (Select) (analysis)
t = time.process_time()
if lastCalc and labelSelects:
    arcpy.analysis.Select(in_features=Choose_Surficial_Points_To_Use, out_feature_class=Output_Points_With_Type_Pit_Or_Quarry, where_clause="label='Pit' OR label='Quarry'")
print('Select Only Points with Labels (2):' + str(time.process_time() - t))
arcpy.AddMessage('Select Only Points with Labels')

# Process: Append (Append) (management)
t = time.process_time()
if lastCalc and labelSelects:
    SG_Flat_File_10_ = arcpy.management.Append(inputs=[Output_Points_With_Type_Pit_Or_Quarry], target=Output, schema_type="NO_TEST", field_mapping="OGS_CODE \"OGS_CODE\" true true false 4 Text 0 0,First,#,"+Output+",OGS_CODE,0,4;GEO_ID \"GEO_ID\" true true false 8 Text 0 0,First,#,"+Output+",GEO_ID,0,8;quad100K \"quad100K\" true true false 35 Text 0 0,First,#,"+Output+",quad100K,0,35;EditorName \"EditorName\" true true false 50 Text 0 0,First,#,"+Output+",EditorName,0,50;LastUpdate \"LastUpdate\" true true false 8 Date 0 0,First,#,"+Output+",LastUpdate,-1,-1;quad24k \"quad24k\" true true false 50 Text 0 0,First,#,"+Output+",quad24k,0,50;label \"label\" true true false 254 Text 0 0,First,#,"+Output+",label,0,254;UNIT1 \"UNIT1\" true true false 255 Text 0 0,First,#,"+Output+",UNIT1,0,255;UNIT2 \"UNIT2\" true true false 255 Text 0 0,First,#,"+Output+",UNIT2,0,255;UNIT3 \"UNIT3\" true true false 255 Text 0 0,First,#,"+Output+",UNIT3,0,255;UNIT4 \"UNIT4\" true true false 255 Text 0 0,First,"+Output+",UNIT4,0,255;UNIT5 \"UNIT5\" true true false 255 Text 0 0,First,#,"+Output+",UNIT5,0,255;LABELSLASHES \"LABELSLASHES\" true true false 255 Text 0 0,First,#,"+Output+",LABELSLASHES,0,255;LITH \"LITH\" true true false 255 Text 0 0,First,#,"+Output+",LITH,0,255", subtype="", expression="")[0]    
print('Append (Append):' + str(time.process_time() - t))
arcpy.AddMessage('Append')

# Process: Add Field (16) (Add Field) (management)
t = time.process_time()
if lastCalc and labelSelects:
    SG_Flat_File_37_ = arcpy.management.AddField(in_table=SG_Flat_File_10_, field_name="TotalThickness", field_type="SHORT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
print('Add Field (16):' + str(time.process_time() - t))
arcpy.AddMessage('Add Field')

# Process: Calculate Field (29) (Calculate Field) (management)
t = time.process_time()
if lastCalc and labelSelects:
    SG_Flat_File_36_ = arcpy.management.CalculateField(in_table=SG_Flat_File_37_, field="TotalThickness", expression="((!L1T!+ !L2T!+ !L3T!+ !L4T!+ !L5T!+ !L6T!+ !L7T!)* 10) - 10", expression_type="Python", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]
print('Calculate Field (29):' + str(time.process_time() - t))
arcpy.AddMessage('Calculate Field')

#Add Bedrock Lithology
arcpy.management.AddField(in_table=SG_Flat_File_36_, field_name="BedrockLith", field_type="TEXT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]
codeblock = """def getBedLith(label):
    lastLabel = label.split("/")[-1]
    if lastLabel in ['w','m','Pit','Quarry']:
        return None
    else:
        return lastLabel
        
"""
arcpy.management.CalculateField(in_table=SG_Flat_File_36_, field="BedrockLith", expression="getBedLith(!label!)", expression_type="Python", code_block=codeblock, field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

# Process: Delete Field (Delete Field) (management)
t = time.process_time()
if lastCalc and labelSelects:
    SG_Flat_File_45_ = arcpy.management.DeleteField(in_table=SG_Flat_File_36_, drop_field=["LITHOLOGY", "MAP_LITH", "maplith100", "code", "UNIT1", "UNIT2", "UNIT3", "UNIT4", "UNIT5", "LABELSLASHES","L1Tx", "L2Tx", "L3Tx", "L4Tx", "L5Tx", "L6Tx", "L7Tx", "Digit", "Alpha"], method="DELETE_FIELDS")[0]
print('Delete Fields:' + str(time.process_time() - t))
arcpy.AddMessage('Delete Fields')

arcpy.management.Delete(Output_Points_With_Type_Pit_Or_Quarry)

print("Done. Total completion time: %s seconds" % round(time.time() - start_time))

