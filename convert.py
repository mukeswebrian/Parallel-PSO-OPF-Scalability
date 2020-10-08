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

# load network
net = pc.from_mpc('case30.mat', casename_mpc_file='ans')
pp.runpp(net)
print(net)
