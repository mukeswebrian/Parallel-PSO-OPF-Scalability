from pymongo import MongoClient
import pandas as pd

server = {"host" : "localhost",
          "port" : 27017,
          "database" : "",
          "collection" : ""}


def logInputs(inputs, names, run_name):

    # specify host db details as necessary
    server["database"] = "pso_opf_inputs"
    server["collection"] = run_name

    client = MongoClient(host=server["host"], port=server["port"])
    log = client[server["database"]][server["collection"]]

    obj = {name:val for name,val in zip(names,inputs)}
    log.insert_one(obj)
    del(log)


def createIterLog(run_name):

    # specify host db details as necessary
    server["database"] = "pso_opf_runs"
    server["collection"] = run_name

    client = MongoClient(host=server["host"], port=server["port"])
    log = client[server["database"]][server["collection"]]

    return log


def logIter(log, iter, bestFitness, timeElapsed):
    obj = {
        'iteration':iter,
        'bestFitness':bestFitness,
        'timeElapsed':timeElapsed
    }

    log.insert_one(obj)

def getAvailableRuns():
    # itdentify database
    server["database"] = "pso_opf_runs"
    client = MongoClient(host=server["host"], port=server["port"])
    db = client[server["database"]]
    runs = db.collection_names()
    del(db)

    return runs

def getParallelRuns():
    return [r for r in getAvailableRuns() if 'parallel' in r]

def getSerialRuns():
    return [r for r in getAvailableRuns() if 'parallel' not in r]

def getRunData(run_name):

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

def getNumParticles(run_name):
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


def getAverageData(nParticles, runType='serial'):

    # filter runs
    if runType == 'serial':
        runs = [ c for c in getSerialRuns() if getNumParticles(c)==nParticles ]
    elif runType == 'parallel':
        runs = [ c for c in getParallelRuns() if getNumParticles(c)==nParticles ]
    else:
        print('Type must be either "parallel" or "serial"')

    # laod datasets
    data = [getRunData(run_name) for run_name in runs]

    # calculate average
    total = 0
    for df in data:
        total = total + df

    average = total/len(data)

    return average

def getParallelGroups():
    groups = set()
    for run in getParallelRuns():
        n = getNumParticles(run)
        if n not in groups:
            groups.add(n)

    return list(groups)

def getSerialGroups():
    groups = set()
    for run in getSerialRuns():
        n = getNumParticles(run)
        if n not in groups:
            groups.add(n)

    return list(groups)
