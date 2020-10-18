import pandapower as pp
import pandapower.converter as pc
import time
import os

case = 'pglib_opf_case6468_rte.mat'
print('solving case: ', case)

solution = 'opf'
net = pc.from_mpc(os.path.join(os.getcwd(), 'case_files', case),
                  casename_mpc_file='ans')


if solution == 'opf':
    # run a timed OPF solution
    start = time.perf_counter()
    try:
        pp.runopp(net)
        converged = True
    except:
        converged = False
    stop = time.perf_counter()

# store result
result = {
    'case': case,
    'bus_count': len(net['bus']),
    'runtime_seconds': stop-start,
    'converged': converged,
    'solution': solution
}

print(result)
