import pandapower as pp
import pandapower.converter as pc
import os
import pandas as pd
import time
from progress.bar import Bar

#cases = [f for f in os.listdir('case_files')]
cases = [c.strip() for c in open('reduced_case_list.txt','r').readlines()]
results = []
bar = Bar('Solving cases', max=len(cases))

for case in cases:
    # load cases
    net = pc.from_mpc(os.path.join(os.getcwd(), 'case_files', case),
                      casename_mpc_file='ans')

    # run a timed OPF solution
    start = time.perf_counter()
    try:
        pp.runopp(net)
        converged = True
    except:
        converged = False
    stop = time.perf_counter()


    # store results
    results.append({
        'case': case,
        'bus_count': len(net['bus']),
        'runtime_seconds': stop-start,
        'converged': converged,
        'losses_mw': net.res_line.pl_mw.sum() + net.res_trafo.pl_mw.sum() + net.res_trafo3w.pl_mw.sum()
    })

    # update progress Bar
    bar.next()
bar.finish()

results = pd.DataFrame(results)
results.to_csv('opf_runtimes.csv')
