import pandapower as pp
import pandapower.converter as pc
import pandapower.networks as pn

'''
# create network
net = pn.case14()
pp.runpp(net)

#convert to matpower Format
pc.to_mpc(net, "case14.mat")
'''

# load MATPOWER network and calculate opf
net = pc.from_mpc('case_files\pglib_opf_case14_ieee.mat', casename_mpc_file='ans')
pp.runopp(net)
print(net)
