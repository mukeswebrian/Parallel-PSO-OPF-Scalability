import pandapower as pp
import pandapower.converter as pc
import os
import pandas as pd
import time
from progress.bar import Bar

cases = [f for f in os.listdir('case_files')]
results = []
bar = Bar('Solving cases', max=len(cases))
bar.next()

for case in cases:
    # load cases
    net = pc.from_mpc(os.path.join(os.getcwd(), 'case_files', case),
                      casename_mpc_file='ans')

    # run a timed PF solution
    start = time.perf_counter()
    try:
        pp.runpp(net)
        converged = True
    except:
        converged = False
    stop = time.perf_counter()


    # store results
    results.append({
        'case': case,
        'bus_count': len(net['bus']),
        'runtime_seconds': stop-start,
        'converged': converged
    })

    # update progress Bar
    bar.next()
bar.finish()

results = pd.DataFrame(results)
results.to_excel('pf_runtimes.xlsx')
