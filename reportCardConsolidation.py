import os
import sys

# Command to run the script: python C:\Users\avenkata2\PycharmProjects\LogToInfo\fileConversionIssues.py C:\Users\avenkata2\Downloads\unzipped-Oct25
# In the above command, we will have to put all the files from nexus location: 
# FOR %B IN (ind cor par sco exm bft fid est) DO start chrome http://apdpdnexus.corp.intuit.net/nexus/content/repositories/releases/com/intuit/taxplatform/content/%B/us/fuego-input-templates-ftf/
# python C:\Users\avenkata2\PycharmProjects\LogToInfo\fileConversionIssues.py C:\Users\avenkata2\Downloads\unzipped-Oct25

fileLocation = sys.argv[1]#r'C:\Users\avenkata2\Downloads\unzipped-Oct25'
otherConversionIssuesFile = r''

def issueCollector(fileLocation, otherConversionIssuesFile):
    otherConversionIssues = []

    pythonFilePath = fileLocation.replace('\\', '/')
    fileDir = ""
    for file in os.listdir(pythonFilePath):
        if file.endswith(".txt"):
            fileDir = str(os.path.join(pythonFilePath, file))
        else: continue

        with open(fileDir, 'r') as input_data:
            print fileDir+""
            for line in input_data:
                if line.strip() == '****************************************Report card***********************************************':
                    otherConversionIssues.append("******"+fileDir+"******")
                    for line in input_data:
                        otherConversionIssues.append(line.rstrip('\n'))

    with open(otherConversionIssuesFile, 'a') as writeFile:
        for item in otherConversionIssues:
            writeFile.write("%s\n" % item)
        otherConversionIssues = []
        writeFile.close()
    return True

fileLocation = fileLocation+""

otherConversionIssuesFile = fileLocation+"\\"+"consolidatedFile" +'.txt'
if not os.path.exists(fileLocation+"\\"):
    os.makedirs(fileLocation+"\\")

issueCollector(fileLocation, otherConversionIssuesFile)
