from pymongo import MongoClient
import pandas as pd
import json
import os

server = {"host" : "localhost",
          "port" : 27017,
          "database" : "",
          "collection" : ""}

logData = {
    "run_name": "",
    "inputs":{},
    "iter_data":[]
    }

def logInputs(inputs, names, run_name, log_destination):

    if log_destination == 'database':
        # specify host db details as necessary
        server["database"] = "pso_opf_inputs"
        server["collection"] = run_name

        client = MongoClient(host=server["host"], port=server["port"])
        log = client[server["database"]][server["collection"]]

        obj = {name:val for name,val in zip(names,inputs)}
        log.insert_one(obj)
        del(log)

    elif log_destination == 'file':
        logData['run_name'] = run_name
        logData['inputs'] = {name:val for name,val in zip(names,inputs)}
        target = os.path.join(os.getcwd(), 'run_data', run_name+'.json')
        logFile = open(target, 'w')
        json.dump(logData, logFile)

    else:
        print('Log error: log_destination must be either "file" or "database"')


def createIterLog(run_name, log_destination):
    '''
    obtain a pointer to the log for storing fitness and time data at each iteration
    '''

    if log_destination == 'database':
        # specify host db details as necessary
        server["database"] = "pso_opf_runs"
        server["collection"] = run_name

        client = MongoClient(host=server["host"], port=server["port"])
        log = client[server["database"]][server["collection"]]
        return log

    elif log_destination == 'file':
        target = os.path.join(os.getcwd(), 'run_data', run_name+'.json')
        log = json.load(open(target, 'r'))
        return log

    else:
        print('Log error: log_destination must be either "file" or "database"')

def createProfileLog(run_name, log_destination):
    '''
    obtain a pointer to the log for storing run profile data
    '''

    if log_destination == 'database':
        server["database"] = "pso_opf_run_profiles"
        server["collection"] = run_name

        client = MongoClient(host=server["host"], port=server["port"])
        ProfileLog = client[server["database"]][server["collection"]]
        return ProfileLog

    elif log_destination == 'file':
        target = os.path.join(os.getcwd(), 'run_profiles', run_name+'.json')
        ProfileLog = open(target, 'w')
        return ProfileLog
    else:
        print('Log error: log_destination must be either "file" or "database"')


def logIter(log, iter, bestFitness, timeElapsed, log_destination):
    obj = {
        'iteration':iter,
        'bestFitness':bestFitness,
        'timeElapsed':timeElapsed
    }

    if log_destination == 'database':
        log.insert_one(obj)

    elif log_destination == 'file':
        log['iter_data'].append(obj)

    else:
        print('Log error: log_destination must be either "file" or "database"')

def logProfile(profileLog, profileData, log_destination):
    if log_destination == 'database':
        log.insert_one(profileData)

    elif log_destination == 'file':
        json.dump(profileData, profileLog)
        profileLog.close()

    else:
        print('Log error: log_destination must be either "file" or "database"')

def endLog(log, run_name, log_destination):
    if log_destination == 'database':
        del(log)
    elif log_destination == 'file':
        target = os.path.join(os.getcwd(), 'run_data', run_name+'.json')
        logFile = open(target, 'w')
        json.dump(log, logFile)
        logFile.close()
    else:
        print('Log error: log_destination must be either "file" or "database"')


def getAvailableRuns(source):
    if source == 'database':
        # itdentify database
        server["database"] = "pso_opf_runs"
        client = MongoClient(host=server["host"], port=server["port"])
        db = client[server["database"]]
        runs = db.collection_names()
        del(db)

        return runs

    elif source == 'file':
        dir = os.path.join(os.getcwd(), 'run_data')
        files = os.listdir(dir)
        runs = [f.replace('.json','') for f in files]
        return runs

    else:
        print('Log error: source must be either "file" or "database"')

def getAvailableProfiles(source):
    if source == 'database':
        # itdentify database
        server["database"] = "pso_opf_profiles"
        client = MongoClient(host=server["host"], port=server["port"])
        db = client[server["database"]]
        profiles = db.collection_names()
        del(db)

        return profiles

    elif source == 'file':
        dir = os.path.join(os.getcwd(), 'run_profiles')
        files = os.listdir(dir)
        profiles = [f.replace('.json','') for f in files]
        return profiles

    else:
        print('Log error: source must be either "file" or "database"')

def getParallelRuns(source):
    return [r for r in getAvailableRuns(source) if 'parallel' in r]

def getSerialRuns(source):
    return [r for r in getAvailableRuns(source) if 'parallel' not in r]

def runExists(run_name, source):
    # check if performance data corresponding to a specified run exists
    if run_name in getAvailableRuns(source):
        return True
    else:
        return False

def profileExists(run_name, source):
    # check if profile data corresponding to a specified run exists
    if run_name in getAvailableProfiles(source):
        return True
    else:
        return False

def getRunData(run_name, source):

    if not runExists(run_name, source):
        print('No data for run {} in {}'.format(run_name, source))
        return None

    if source == 'database':
        # specify host db details as necessary
        server["database"] = "pso_opf_runs"
        server["collection"] = run_name

        client = MongoClient(host=server["host"], port=server["port"])
        log = client[server["database"]][server["collection"]]

        # fetch all the results for the specified run
        entries = []
        for entry in log.find({}):
            entries.append(entry)

        if len(entries)==0: # no hits for the query
            print("No hits for the specified query")
            data = None
        else: # create a DataFrame containing the results of the run
            data = pd.DataFrame(entries).drop(columns=["_id"])

        del(log)
        return data

    elif source == 'file':
        target = os.path.join(os.getcwd(), 'run_data', run_name+'.json')
        run_info = json.load(open(target, 'r'))
        data = pd.DataFrame(run_info['iter_data']) # convert to DataFrame
        return data

    else:
        print('Log error: source must be either "file" or "database"')

def getProfileData(run_name, source):

    if not profileExists(run_name, source):
        print('No data for run {} in {}'.format(run_name, source))
        return None

    if source == 'database':
        return None

    elif source == 'file':
        target = os.path.join(os.getcwd(), 'run_profiles', run_name+'.json')
        run_info = json.load(open(target, 'r'))
        #data = pd.DataFrame(run_info, index=[run_name]).T # convert to DataFrame
        return run_info

    else:
        print('Log error: source must be either "file" or "database"')


def getNumParticles(run_name):
    '''Determines the number of particles corresponding to a given run_name'''
    numbers = '0123456789'
    nums = []
    flg = 0
    i,j,k = 0,0,0

    while i < len(run_name):

        if run_name[i] in numbers and flg==0:
            j = i
            k = i
            flg = 1

        elif run_name[i] in numbers and flg==1:
            k += 1
        elif run_name[i] not in numbers and flg==1:
            k += 1
            flg = 0
            nums.append(int(run_name[j:k]))
        else:
            pass

        i += 1

    return nums[0]


def getAverageData(nParticles, source, runType='serial'):

    # filter runs
    if runType == 'serial':
        runs = [ c for c in getSerialRuns(source) if getNumParticles(c)==nParticles ]
    elif runType == 'parallel':
        runs = [ c for c in getParallelRuns(source) if getNumParticles(c)==nParticles ]
    else:
        print('Type must be either "parallel" or "serial"')

    # laod datasets
    data = [getRunData(run_name, source) for run_name in runs]

    # calculate average
    total = 0
    for df in data:
        total = total + df

    average = total/len(data)

    return average

def getParallelGroups(source):
    groups = set()
    for run in getParallelRuns(source):
        n = getNumParticles(run)
        if n not in groups:
            groups.add(n)

    return list(groups)

def getSerialGroups(source):
    groups = set()
    for run in getSerialRuns(source):
        n = getNumParticles(run)
        if n not in groups:
            groups.add(n)

    return list(groups)
