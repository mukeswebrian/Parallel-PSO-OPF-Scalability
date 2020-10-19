import pandas as pd
import pandapower as pp
import plotly.express as px
import pandapower.converter as pc
import os
import read_control_parameters as rd


case = 'pglib_opf_case57_ieee.mat'
net = pc.from_mpc(os.path.join(os.getcwd(), 'case_files', case),
                  casename_mpc_file='ans')

pp.runpp(net)

print(rd.get1DparameterArray(net))
