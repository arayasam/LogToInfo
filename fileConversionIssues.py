import os
import sys

# Command to run the script: python C:\Users\avenkata2\PycharmProjects\LogToInfo\fileConversionIssues.py C:\Users\avenkata2\Downloads\unzipped-Oct25
# In the above command, we will have to put all the files from nexus location: 
# python C:\Users\avenkata2\PycharmProjects\LogToInfo\fileConversionIssues.py C:\Users\avenkata2\Downloads\11-30\unzipped
# FOR %A IN (ind cor par exm sco fid est bft) DO FOR %B in (13 14 15 16 17) DO start chrome http://apdpdnexus.corp.intuit.net/nexus/content/repositories/releases/com/intuit/taxplatform/content/20%B/%A/us/fuego-input-templates-ftf/

fileLocation = sys.argv[1]#r'C:\Users\avenkata2\Downloads\unzipped-Oct25'
fileConversionIssuesFile = r'C:\Users\avenkata2\Downloads\unzipped-Oct25\fileCI.txt'
controlConversionIssuesFile = r'C:\Users\avenkata2\Downloads\unzipped-Oct25\controlCI.txt'
otherConversionIssuesFile = r'C:\Users\avenkata2\Downloads\unzipped-Oct25\otherCI.txt'

if not os.path.exists(fileLocation+"\\output"):
    # print "Output location: "fileLocation+"\\output"
    os.makedirs(fileLocation+"\\output")



def issueCollector(fileLocation, fileConversionIssuesFile, controlConversionIssuesFile, otherConversionIssuesFile):
    fileConversionIssues = []
    controlConversionIssues = []
    otherConversionIssues = []
    if not os.path.exists(fileLocation+"\output"):
        # print fileLocation+"\\output"
        os.makedirs(fileLocation+"\output")

    pythonFilePath = fileLocation.replace('\\', '/')
    pythonFilePath += r'/Fuego_templates/fuego_output_inputscreens/'
    fileDir = ""
    for file in os.listdir(pythonFilePath):
        if file.endswith(".txt"):
            fileDir = str(os.path.join(pythonFilePath, file))

    with open(fileDir, 'r') as input_data:
        for line in input_data:
            if line.strip() == '--------File Conversion Errors :':
                break
        for line in input_data:
            if line.strip() == '--------Control Conversion Errors :':
                break
            fileConversionIssues.append(line.rstrip('\n'))
        input_data.close()

    with open(fileDir, 'r') as input_data:
        for line in input_data:
            if line.strip() == '--------Control Conversion Errors :':
                break
        for line in input_data:
            if line.strip() == '--------Conversion Warnings :':
                break
            controlConversionIssues.append(line.rstrip('\n'))
        input_data.close()

    with open(fileDir, 'r') as input_data:
        for line in input_data:
            if line.strip() == '--------Conversion Warnings :':
                for line in input_data:
                    otherConversionIssues.append(line.rstrip('\n'))
        input_data.close()

    # print len(fileConversionIssues)
    # print "-----------------------------------"
    # print len(controlConversionIssues)
    # print "-----------------------------------"
    # print len(otherConversionIssues)

    with open(fileConversionIssuesFile, 'a') as writeFile:
        for item in fileConversionIssues:
            writeFile.write("%s\n" % item)

    with open(controlConversionIssuesFile, 'a') as writeFile:
        for item in controlConversionIssues:
            writeFile.write("%s\n" % item)

    with open(otherConversionIssuesFile, 'a') as writeFile:
        for item in otherConversionIssues:
            writeFile.write("%s\n" % item)
    return True


for fileDir in os.listdir(fileLocation):
    allYears = ['2017', '2016', '2015', '2014', '2013']
    try:
        for YYYY in allYears:
            if fileDir.find(YYYY) != -1:
                fileConversionIssuesFile = fileLocation + \
                    '\\output\\fileConversionIssues' + YYYY + '.txt'
                controlConversionIssuesFile = fileLocation + \
                    '\\output\\controlConversionIssues' + YYYY + '.txt'
                otherConversionIssuesFile = fileLocation + \
                    '\\output\\otherConversionIssues' + YYYY + '.txt'

                fileLocation2 = fileLocation + '\\' + fileDir
                issueCollector(fileLocation2, fileConversionIssuesFile, controlConversionIssuesFile, otherConversionIssuesFile)
    except WindowsError:
        print "Error because of zip files in the same location. Not an issue."
        # You may need to check if the multiple except work as expected or not.
    except:
        print "Error"

#            issueCollector(fileLocation + '\\' + fileDir, fileConversionIssuesFile,
#                           controlConversionIssuesFile, otherConversionIssuesFile)
