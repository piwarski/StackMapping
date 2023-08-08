import arcpy, sys, datetime, time, os

arcpy.env.overwriteOutput = True

start_time = time.time()
now = datetime.datetime.now()
#print('starting')

Polygons = arcpy.GetParameterAsText(0)
#Polygons = r'C:\Users\10214536\OneDrive - State of Ohio\Documents\StackMapping\DerrivativeMapping\SurficialGeologyOhio(DDF-8).gdb\SG_Polys'

#Definition Queries for L1TX (Layer one Texture) through L7TX. Field is set to C (coarse material) if they equal any of these values. 
#Add fields before we add "C" values
i = 1
while i <= 5:
    arcpy.management.AddField(Polygons, "L" + str(i) + "TX", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    i +=1
#print('L#TX fields created')
arcpy.AddMessage('L#TX fields created')

#Add "C" values to fields we just created that meet definition query criteria
i = 1
while i <= 5:
    codeblock = "def assignC(fieldName):\n    return {'S':'C','Si':'C','SG':'C','SGi':'C','IC':'C','ICi':'C','G':'C','Gi':'C'}.get(fieldName, None)"
    fieldName = 'L'+str(i)+'G'
    arcpy.CalculateField_management(Polygons,'L'+str(i)+'TX','assignC(!'+fieldName+'!)',"PYTHON",codeblock)
    i +=1
#print('"C" values added')
arcpy.AddMessage('"C" values added')

#Need to set L1TX to L5TX to () (parentheses) so that these () stack units are excluded from the queries below that determine if other units are buried.
i = 1
while i <= 5:
    codeblock = "def assignP(fieldName1,fieldName2):\n    if fieldName1 == '()':\n        return '()'\n    else:\n        return fieldName2"
    fieldName1 = 'L'+str(i)+'S'
    fieldName2 = "L"+str(i)+"TX"
    arcpy.CalculateField_management(Polygons,fieldName2,'assignP(!'+fieldName1+'!,!'+fieldName2+'!)',"PYTHON",codeblock)
    i+=1
#print('Parentheses added to L#TX fields')
arcpy.AddMessage('Parentheses added to L#TX fields')    

#Add layer thickness fields excluding units with parentheses including all textures (not just coarse)
i = 1
while i <= 5:
    if i == 1:
        arcpy.management.AddField(Polygons, "L" + str(i) + "TnoP", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    else:
        arcpy.management.AddField(Polygons, "L" + str(i) + "noP", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    i +=1
#print('L#noP fields created')
arcpy.AddMessage('L#noP fields created')

#Add L#TnoP values from L#t fields when L#S != parentheses
i = 1
while i <=5:
    codeblock = 'def assignT(fieldLT,fieldLS):\n    if fieldLS != "()":\n        return fieldLT\n    else:\n        return 0'
    fieldLT = 'L'+str(i)+'T'
    fieldLS = 'L'+str(i)+'S'
    if i == 1: #top layer had slightly differnt name
        arcpy.CalculateField_management(Polygons,'L'+str(i)+'TnoP','assignT(!'+fieldLT+'!,!'+fieldLS+'!)',"PYTHON",codeblock)
    else:
        arcpy.CalculateField_management(Polygons,'L'+str(i)+'noP','assignT(!'+fieldLT+'!,!'+fieldLS+'!)',"PYTHON",codeblock)
    i+=1
#print('Added L#noP values from L#t fields')
arcpy.AddMessage('Added L#noP values from L#t fields')

#Add noPT field
arcpy.management.AddField(Polygons, "noPT", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

#Calculate sum of nop fields for noPT field
codeblock = 'def sumV(L1TnoP,L2noP,L3noP,L4noP,L5noP):\n    a = (int(L1TnoP)+int(L2noP)+int(L3noP)+int(L4noP)+int(L5noP))-1\n    return a'
arcpy.CalculateField_management(Polygons,'noPT','sumV(!L1TnoP!,!L2noP!,!L3noP!,!L4noP!,!L5noP!)',"PYTHON",codeblock)
#print('Added noP')
arcpy.AddMessage('Added noP')

#Create L#FT fields
i = 1
while i <=5:
    arcpy.management.AddField(Polygons, "L" + str(i) + "FT", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    i+=1
#print('L#FT fields created')
arcpy.AddMessage('L#FT fields created')

#If L#TX is null, L#FT = L#TnoP or L#noP
i = 1
while i <=5:
    codeblock = 'def assignV(fieldTX,field_noP):\n    if fieldTX == None:\n        return field_noP\n    else:\n        return 0'
    fieldTX = 'L'+str(i)+'TX'    
    if i == 1: #top layer had slightly differnt name
        field_noP = 'L'+str(i)+'TnoP'
        arcpy.CalculateField_management(Polygons,'L'+str(i)+'FT','assignV(!'+fieldTX+'!,!'+field_noP+'!)',"PYTHON",codeblock)
    elif i > 1:
        field_noP = 'L'+str(i)+'noP'
        arcpy.CalculateField_management(Polygons,'L'+str(i)+'FT','assignV(!'+fieldTX+'!,!'+field_noP+'!)',"PYTHON",codeblock)
    i+=1
#print('Assigned L#FT values')
arcpy.AddMessage('Assigned L#FT values')

#Defines if a given layer is buried by fine grained material - if true: yes (it's buried). Used to populate L1B to L5B. If there are preexisting values, set fields all to <NULL> using None in field calculator first.
#Add new fields first
i = 1
while i <= 5:
    arcpy.management.AddField(Polygons, "L" + str(i) + "B", "Text", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    i +=1
#print('L#B fields created')
arcpy.AddMessage('L#B fields created')

#Assign yes values
i = 1
L_FTs_exp = []
while i <= 5:
    #Add new field name to list of fields that need to have their values summed
    L_FTs_exp.append('!L'+str(i)+'FT!')
    #Dyanmically generate CalculateField expression because number of parameters passed into codeblock function will change
    calcExpression = ','.join(L_FTs_exp)
    calcExpression = 'sumAndEval(' + calcExpression + ')'
    #Codeblock
    codeblock = "def sumAndEval(*args):\n    sum = 0\n    for num in args:\n        sum+= int(num)\n    if sum > 1:\n        return 'yes'"
    #Calculate Field
    arcpy.CalculateField_management(Polygons,'L'+str(i)+'B',calcExpression,"PYTHON",codeblock)
    i += 1
#print('Assigned yes values to L#B fields')    
arcpy.AddMessage('Assigned yes values to L#B fields')

#Defines Derivative material thickness for each layer. Used to populate L1DERT (layer one derivative thickness) to L5DERT. If there are preexisting values, set all fields to zero first.
#First, add L#DERT fields
i = 1
while i <= 5:
    arcpy.management.AddField(Polygons, "L" + str(i) + "DERT", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    i +=1
#print('L#DERT fields created')

#Then, perform calculations to populate L#DERT fields
#L1DERT: Definition query: L1B IS NULL And L1TX = 'C'     then field calculate: L1DERT = !L1TnoP!
codeblock = "def calcDERT1(field1,field2,assign1):\n    if field1 == None and field2 == 'C':\n        return assign1\n    else:\n        return 0"
arcpy.CalculateField_management(Polygons,"L1DERT",'calcDERT1(!L1B!,!L1TX!,!L1TnoP!)',"PYTHON",codeblock)
#print('L1DERT done')

#L2DERT: Definition query: L1B IS NULL And L2B IS NULL And L2TX = 'C'     Then field calculate: L2DERT = !L2noP!
codeblock = "def calcDERT2(field1,field2,field3,assign1):\n    if field1 == None and field2 == None and field3 == 'C':\n        return assign1\n    else:\n        return 0"
arcpy.CalculateField_management(Polygons,"L2DERT",'calcDERT2(!L1B!,!L2B!,!L2TX!,!L2noP!)',"PYTHON",codeblock)
#print('L2DERT done')

#L3DERT: Definition query: L1B IS NULL And L2B IS NULL And L3B IS NULL And L3TX = 'C'     Then field calculate: L3DERT = !L3noP!
codeblock = "def calcDERT3(field1,field2,field3,field4,assign1):\n    if field1 == None and field2 == None and field3 == None and field4 == 'C':\n        return assign1\n    else:\n        return 0"
arcpy.CalculateField_management(Polygons,"L3DERT",'calcDERT3(!L1B!,!L2B!,!L3B!,!L3TX!,!L3noP!)',"PYTHON",codeblock)
#print('L3DERT done')

#L4DERT: Definition query: L1B IS NULL And L2B IS NULL And L3B IS NULL AND L4B IS NULL And L4TX = 'C'     Then field calculate: L4DERT = L4noP
codeblock = "def calcDERT4(field1,field2,field3,field4,field5,assign1):\n    if field1 == None and field2 == None and field3 == None and field4 == None and field5 == 'C':\n        return assign1\n    else:\n        return 0"
arcpy.CalculateField_management(Polygons,"L4DERT",'calcDERT4(!L1B!,!L2B!,!L3B!,!L4B!,!L4TX!,!L4noP!)',"PYTHON",codeblock)
#print('L4DERT done')

#L5DERT: Definition query: L1B IS NULL And L2B IS NULL And L3B IS NULL AND L4B IS NULL AND L5B IS NULL And L5TX = 'C'     Then field calculate: L5DERT = L5noP
codeblock = "def calcDERT5(field1,field2,field3,field4,field5,field6,assign1):\n    if field1 == None and field2 == None and field3 == None and field5 == None and field6 == 'C':\n        return assign1\n    else:\n        return 0"
arcpy.CalculateField_management(Polygons,"L5DERT",'calcDERT5(!L1B!,!L2B!,!L3B!,!L4B!,!L5B!,!L5TX!,!L5noP!)',"PYTHON",codeblock)
#print('L5DERT done')

arcpy.AddMessage('L#DERTs done')

#Create DERT field
arcpy.management.AddField(Polygons, "DERT", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

#Calculate values for DERT field
codeblock = 'def sumDERT_Fields(L1,L2,L3,L4,L5):\n    a = L1 + L2 + L3 + L4 + L5\n    return a'
arcpy.CalculateField_management(Polygons,"DERT",'sumDERT_Fields(!L1DERT!,!L2DERT!,!L3DERT!,!L4DERT!,!L5DERT!)',"PYTHON",codeblock)
#print('L#DERT calculations completed')
arcpy.AddMessage('L#DERT calculations completed')

#Create DERT2plus field
arcpy.management.AddField(Polygons, "SGThickness", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

#Calculate values for DERT2plus field
#codeblock = 'def calcDERT2plus(DERT):\n    return int(DERT)*10'
codeblock = 'def calcDERT2plus(DERT):\n    if int(DERT)*10 <= 10:\n        return None\n    else:\n        return int(DERT)*10'
arcpy.CalculateField_management(Polygons,"SGThickness","calcDERT2plus(!DERT!)","PYTHON",codeblock)

#Create carbonate bedrock field
arcpy.management.AddField(Polygons, "CarbonateDepth", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#print('Created carbonate bedrock field')
arcpy.AddMessage('Created carbonate bedrock field')

#Calculate values for carbonate bedrock field
codeblock = "def carbBedCalc(L1G,L2G,L3G,L4G,L5G,noPT,L1TnoP,L2noP,L3noP,L4noP,L5noP):\n    if (L1G == 'DLs' or L2G == 'DLs' or L3G == 'DLs' or L4G == 'DLs' or L5G == 'DLs' or L1G == 'LsSh' or L2G == 'LsSh' or L3G == 'LsSh' or L4G == 'LsSh' or L5G == 'LsSh') and noPT <= 4:\n        return 10*(sum(filter(None,[L1TnoP,L2noP,L3noP,L4noP,L5noP]))-1)\n    else:\n        return None"
#codeblock = "def carbBedCalc(L1G,L2G,L3G,L4G,L5G,noPT,L1TnoP,L2noP,L3noP,L4noP,L5noP):\n    if (L1G == 'DLs' or L2G == 'DLs' or L3G == 'DLs' or L4G == 'DLs' or L5G == 'DLs' or L1G == 'LsSh' or L2G == 'LsSh' or L3G == 'LsSh' or L4G == 'LsSh' or L5G == 'LsSh') and noPT <= 4:\n        carbDepth = 10*(sum(filter(None,[L1TnoP,L2noP,L3noP,L4noP,L5noP]))-1)\n        if carbDepth < 20:\n            return None\n        else:\n            return carbDepth\n    else:\n        return None"
arcpy.CalculateField_management(Polygons,"CarbonateDepth",'carbBedCalc(!L1G!,!L2G!,!L3G!,!L4G!,!L5G!,!noPT!,!L1TnoP!,!L2noP!,!L3noP!,!L4noP!,!L5noP!)',"PYTHON",codeblock)
#print('Carbonate bedrock calculations done')
arcpy.AddMessage('Carbonate bedrock calculations done')

#print("Done. Total completion time: %s seconds" % round(time.time() - start_time))
