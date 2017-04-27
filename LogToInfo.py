import re
import sys
import os

# Information about iteration over files in a  given directory if directory is passed as argument to program. .
# for filename in os.listdir(sys.argv[1]):
#     if filename.endswith(".log"):
#         # print(os.path.join(directory, filename))
#         continue
#     else:
#         continue


def logToInfo(logFile):
    """
    The function takes log file as input and outputs csv file containing the needed metrics like runtime per Iteration. 
    :param logFile: 
    :return csv: 
    """

    NumOfIterations = 0
    ListOfIterations = []
    Iteration=[] #Done
    FileName=None #Done
    FileTimestamp=None #Done
    ClientName=None  #Done
    Client=None   #Total time that is sum of client iterations
    ClientIterations=[]       #Done
    RequestType=[]       #Done
    ProcessOutputReqTime = None   #Done  # column name is ProcessOutputRequest
    FEngine_CreateCalcOutput=[]   #Done
    FCalc_Calculate=[]            #Done
    EFRequest_ExecuteRequests=[] #Done
    StandardPrint_ExecuteRequests=[]        # Done
    EFReturn_ExecuteRequests=[]     #Done #NeedsTesting
    ExtOnlyPrint_ExecuteRequests=[]     #Done #NeedsTesting
    PartialPrint_ExecuteRequests=[]     #Done #NeedsTesting
    SubClientPackagePrint_ExecuteRequests=[]     #Done #NeedsTesting #just to commit
    TViewSyncRequestHandler_ProcessRequest=[]
    COEViewSync_ReloadAfterCalc=[]
    ClientNameAndTotalRunTime = []
    tempList = []
    firstAndLastLine=[]

    #matching lines based on patterns/substrings in the line.
    # totalTimeVariables=['ColumnName=ClientIterations','Iteration','ElapseTime']
    totalTimeVariables=['ColumnName=ClientIterations','Iteration=']
    count=0
    ClientNameVariables=['ColumnName=Client', 'ClientName']
    ReqTypeAndPORVariables=['ColumnName=ProcessOutputRequest','ElapseTime(ms)=']
    CreateCalcOutputVariables=['ColumnName=FEngine.CreateCalcOutput', 'ElapseTime(ms)=']
    FCalc_CalculateVariables=['ColumnName=FCalc.Calculate', 'ElapseTime(ms)=']
    EFRequest_ERequestsVariables=['ColumnName=EFRequest.ExecuteRequests', 'ElapseTime(ms)=']
    EFReturn_ERequestsVariables=['ColumnName=EFReturn.ExecuteRequests', 'ElapseTime(ms)='] # NEED TO CHECK WITH EDDIE. INPROGRESS.
    StandardPrint_ERequestsVariables=['ColumnName=StandardPrint.ExecuteRequests', 'ElapseTime(ms)=']
    COEViewSync_RACVariables=['ColumnName=COEViewSync.ReloadAfterCalc', 'ElapseTime(ms)=']
    TViewSyncRequestHandler_PRVariables = ['ColumnName=TViewSyncRequestHandler.ProcessRequest', 'ElapseTime(ms)=']
    ExtOnlyPrint_ERequestsVariables = ['ColumnName=ExtOnlyPrint.ExecuteRequests', 'ElapseTime(ms)=']
    PartialPrint_ERequestsVariables = ['ColumnName=PartialPrint.ExecuteRequests', 'ElapseTime(ms)=']
    SubClientPackagePrint_ERequestsVariables = ['ColumnName=SubClientPackagePrint.ExecuteRequests', 'ElapseTime(ms)=']
    StopIterationVariables=['Stop=', 'ColumnName=ClientIterations', 'Iteration=', 'ElapseTime(ms)=']


#   firstAndLastLine[] gives the first line and the last line of the file containing the file name and total iteration time.
#   ListOfIterations[] gives the set of lines from each iteration. Used for processing later.
    with open(logFile,'r') as logReader:
        # Will have to change the following two variables if number of clients change.
        FileTimestamp = '-'.join(((logReader.readline()).split())[0:4])
        FileName = logReader.name
        next(logReader)
        firstAndLastLine.append((logReader.readline()).rstrip())

        for line in logReader:
            line = line.rstrip()
            if not line: continue
            tempList.append(line)
            if all(word in line for word in StopIterationVariables):
                ListOfIterations.append(tempList)
                tempList=[]
                continue
        firstAndLastLine.append(tempList[0])
#        print(*ListOfIterations, sep='\n')
#        print(*firstAndLastLine, sep='\n')


#**************************** Need to process the two lists produced above for the following functions

#
#
#             # Gives out a list containing all client names along with total runtime.
#             # Output: ClientNameAndTotalRunTime[2]. 1st value is ClientName, 2nd value is TotalClientRunTime
#         #     if all(word in line for word in ClientNameVariables):
#         #         parts = line.split()
#         #         ClientNameAndTotalRunTime.append(re.findall('\=(.*?)\;', parts[parts.__len__() - 1]))
#         #
#         # ClientName = ''.join(ClientNameAndTotalRunTime[0])
#         # TotalClientRunTime = ''.join(ClientNameAndTotalRunTime[1])
#         # # print(ClientName, TotalClientRunTime)
#
#
#             # Gives out a list of run time per iteration. Also gives out total number of iterations and a list of Iteration#.
#             # Output: int NumOfIterations, list ClientIterations[N], list Iteration[N]
#             if all(word in line for word in totalTimeVariables):
#                 parts = line.split()
#                 Iteration.append(int(re.findall('\d+', parts[parts.__len__() - 2])[0]))
#                 ClientIterations.append(int(re.findall('\d+', parts[parts.__len__()-1] )[0]))
#                 NumOfIterations+=1
#         # print(NumOfIterations,ClientIterations,Iteration)
#
#
#             # Gives out a list of n sublists where each sublist contains the RequestType and its runtime. N is the number of iterations
#             # Output: RequestType[[RequestType, ProcessOutputReqTime]...] . N sublists
#             if all(word in line for word in ReqTypeAndPORVariables):
#                 parts = line.split()
#                 ProcessOutputReqTime = int(re.findall('\d+', parts[parts.__len__() - 1])[0])
#                 RequestType.append([''.join(re.findall('\=(.*?)\;', parts[parts.__len__() - 2])),ProcessOutputReqTime])
#         # print(RequestType,ProcessOutputReqTime)
#
#
#             # Gives out a list of FEngine_CreateCalcOutput value/runtime per iteration.
#             # Output: FEngine_CreateCalcOutput[]. N values
#             if all(word in line for word in CreateCalcOutputVariables):
#                 parts = line.split()
#                 FEngine_CreateCalcOutput.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
#         # print(FEngine_CreateCalcOutput)
#
#
#             # Gives out a list of FCalc_Calculate value/runtime per iteration.
#             # Output: FCalc_Calculate[]. N values
#             if all(word in line for word in FCalc_CalculateVariables):
#                 parts = line.split()
#                 FCalc_Calculate.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
#         # print(FCalc_Calculate)
#
#
#             # Gives out a list of EFRequest_ExecuteRequests value/runtime per iteration.
#             # Output: EFRequest_ExecuteRequests. N Values
#             if all(word in line for word in EFRequest_ERequestsVariables):
#                 parts = line.split()
#                 EFRequest_ExecuteRequests.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
#         # print(EFRequest_ExecuteRequests)
#
#
#             # Gives out a list of StandardPrint_ExecuteRequests value/runtime per iteration.
#             # Output: StandardPrint_ExecuteRequests[]. N values
#             if all(word in line for word in StandardPrint_ERequestsVariables):
#                 parts = line.split()
#                 StandardPrint_ExecuteRequests.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
#         # print(StandardPrint_ExecuteRequests)
#
# #*************************Not yet tested above section************************************************************
#
#             # Gives out a list of ExtOnlyPrint_ExecuteRequests value/runtime per iteration.
#             # Output: ExtOnlyPrint_ExecuteRequests[]. N values
#             if all(word in line for word in ExtOnlyPrint_ERequestsVariables):
#                 parts = line.split()
#                 ExtOnlyPrint_ExecuteRequests.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
#         # print(ExtOnlyPrint_ExecuteRequests)
#
#             # Gives out a list of PartialPrint_ExecuteRequests value/runtime per iteration.
#             # Output: PartialPrint_ExecuteRequests[]. N values
#             if all(word in line for word in PartialPrint_ERequestsVariables):
#                 parts = line.split()
#                 PartialPrint_ExecuteRequests.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
#         # print(PartialPrint_ExecuteRequests)
#
#             # Gives out a list of SubClientPackagePrint_ExecuteRequests value/runtime per iteration.
#             # Output: SubClientPackagePrint_ExecuteRequests[]. N values
#             if all(word in line for word in SubClientPackagePrint_ERequestsVariables):
#                 parts = line.split()
#                 SubClientPackagePrint_ExecuteRequests.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
#         # print(SubClientPackagePrint_ExecuteRequests)
#
#
#             # Gives out a list of EFReturn_ExecuteRequests value/runtime per iteration.
#             # Output: EFReturn_ExecuteRequests[]. N values
#             if all(word in line for word in EFReturn_ERequestsVariables):
#                 parts = line.split()
#                 EFReturn_ExecuteRequests.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
#         # print(EFReturn_ExecuteRequests)
#
# #*********************************Not yet tested above section********************************************************
#
#             # Gives out a list of COEViewSync_ReloadAfterCalc value/runtime per iteration.
#             # Output: COEViewSync_ReloadAfterCalc[]. N values
#             if all(word in line for word in COEViewSync_RACVariables):
#                 parts = line.split()
#                 COEViewSync_ReloadAfterCalc.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
#         # print(COEViewSync_ReloadAfterCalc)
#
#
#             # Gives out a list of TViewSyncRequestHandler_ProcessRequest value/runtime per iteration.
#             # Output: TViewSyncRequestHandler_ProcessRequest[]. N values
#             if all(word in line for word in TViewSyncRequestHandler_PRVariables):
#                 parts = line.split()
#                 TViewSyncRequestHandler_ProcessRequest.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
#         # print(TViewSyncRequestHandler_ProcessRequest)
#

logToInfo("LacerteMockAppPerfData-ViewSync-DOE-042617122534.log")
