import re

def logToInfo(logFile):
    """
    The function takes log file as input and outputs csv file containing the needed metrics like runtime per Iteration. 
    :param logFile: 
    :return csv: 
    """

    NumOfIterations = 0
    dataForIteration = []
    Iteration=[] #Done
    FileName=None #Done
    FileTimestamp=None #Done
    ClientName=None  #Done
    ClientIterations=[]       #Done
    RequestType=[]       #Done
    ProcessOutputReqTime = None     # column name is ProcessOutputRequest      # Done
    FEngine_CreateCalcOutput=[]   #Done
    FCalc_Calculate=[]            #Done
    EFRequest_ExecuteRequests=[] #Done
    EFReturn_ExecuteRequests=[]     #Inprogress
    ExtOnlyPrint_ExecuteRequests=None
    PartialPrint_ExecuteRequests=None
    StandardPrint_ExecuteRequests=None
    SubClientPackagePrint_ExecuteRequests=None
    TViewSyncRequestHandler_ProcessRequest=None
    COEViewSync_ReloadAfterCalc=None
    ClientNameAndTotalRunTime = []

    # ColumnName=FEngine.CreateCalcOutput;
    # ElapseTime(ms)=0;


    #matching lines based on words in the line.
    totalTimeVariables=['ColumnName=ClientIterations','Iteration','ElapseTime']
    ClientNameVariables=['ColumnName=Client', 'ClientName']
    ReqTypeAndPORVariables=['ColumnName=ProcessOutputRequest','ElapseTime(ms)=']
    CreateCalcOutputVariables=['ColumnName=FEngine.CreateCalcOutput', 'ElapseTime(ms)=']
    FCalc_CalculateVariables=['ColumnName=FCalc.Calculate', 'ElapseTime(ms)=']
    EFRequest_ERequestsVariables=['ColumnName=EFRequest.ExecuteRequests', 'ElapseTime(ms)=']
    EFReturn_ERequestsVariables=['ColumnName=EFReturn.ExecuteRequests', 'ElapseTime(ms)='] # NEED TO CHECK WITH EDDIE. INPROGRESS.


    with open(logFile,'r') as logReader:
        # Will have to change the following two variables if number of clients change.
        FileTimestamp = '-'.join(((logReader.readline()).split())[0:4])
        FileName = logReader.name

        for line in logReader:
            line = line.rstrip()
            if not line: continue


            # Gives out a list of run time per iteration. Also gives out total number of iterations and a list of Iteration#.
            # Output: int NumOfIterations, list ClientIterations[N], list Iteration[N]
            if all(word in line for word in totalTimeVariables):
                parts = line.split()
                Iteration.append(int(re.findall('\d+', parts[parts.__len__() - 2])[0]))
                ClientIterations.append(int(re.findall('\d+', parts[parts.__len__()-1] )[0]))
                NumOfIterations+=1
#        print(NumOfIterations,ClientIterations,Iteration)


            # Gives out a list of n sublists where each sublist contains the RequestType and its runtime. N is the number of iterations
            # Output: RequestType[[RequestType, ProcessOutputReqTime]...] . N sublists
            if all(word in line for word in ReqTypeAndPORVariables):
                parts = line.split()
                ProcessOutputReqTime = int(re.findall('\d+', parts[parts.__len__() - 1])[0])
                RequestType.append([''.join(re.findall('\=(.*?)\;', parts[parts.__len__() - 2])),ProcessOutputReqTime])
        # print(RequestType,ProcessOutputReqTime)


            # Gives out a list of FEngine_CreateCalcOutput value/runtime per iteration.
            # Output: FEngine_CreateCalcOutput[]. N values
            if all(word in line for word in CreateCalcOutputVariables):
                parts = line.split()
                FEngine_CreateCalcOutput.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
        # print(FEngine_CreateCalcOutput)


            # Gives out a list of FCalc_Calculate value/runtime per iteration.
            # Output: FCalc_Calculate[]. N values
            if all(word in line for word in FCalc_CalculateVariables):
                parts = line.split()
                FCalc_Calculate.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
        # print(FCalc_Calculate)


            # Gives out a list of EFRequest_ExecuteRequests value/runtime per iteration.
            # Output: EFRequest_ExecuteRequests
            if all(word in line for word in EFRequest_ERequestsVariables):
                parts = line.split()
                EFRequest_ExecuteRequests.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
        # print(EFRequest_ExecuteRequests)



#******************************************Not yet tested below section************************************************

            # Gives out a list of EFReturn_ExecuteRequests value/runtime per iteration.
            # Output: EFReturn_ExecuteRequests
            if all(word in line for word in EFReturn_ERequestsVariables):
                parts = line.split()
                EFReturn_ExecuteRequests.append(int(re.findall('\d+', parts[parts.__len__() - 1])[0]))
        # print(EFReturn_ExecuteRequests)

# ******************************************Not yet tested above section***********************************************

            # Gives out a list containing all client names along with total runtime.
            # Output: ClientNameAndTotalRunTime[2]. 1st value is ClientName, 2nd value is TotalClientRunTime
            if all(word in line for word in ClientNameVariables):
                parts = line.split()
                ClientNameAndTotalRunTime.append(re.findall('\=(.*?)\;', parts[parts.__len__() - 1]))

        ClientName = ''.join(ClientNameAndTotalRunTime[0])
        TotalClientRunTime = ''.join(ClientNameAndTotalRunTime[1])
        # print(ClientName, TotalClientRunTime)


logToInfo("logFileDoe.log")