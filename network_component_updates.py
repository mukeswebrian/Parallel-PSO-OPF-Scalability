import pandas as pd

# Generator outputs
def updateGenRealPower(net, bus, mwVal):
    # specifiy the gen bus number
    # specify the new MW output level
    genIndex = net.gen[net.gen.bus == bus].index[0] # get gen's index in  gen table
    data = pd.Series([mwVal], name='p_mw', index=[genIndex])
    net.gen.update(data)

# Terminal Voltages (shceduled Voltages)
def updateGenVsched(net, bus, puVal):
    # specifiy the gen bus number
    # specify the new Scheduled pu voltage level
    genIndex = net.gen[net.gen.bus == bus].index[0] # get gen's index in  gen table
    data = pd.Series([puVal], name='vm_pu', index=[genIndex])
    net.gen.update(data)

# Transformer Tap Adjustment
def updateTrafoTapPosition(net, lv_bus, hv_bus, tapPos):

    # filter the transformet table based on lv and hv buses
    txBusFilter = lambda bus, level: net.trafo[level]==bus
    combine = lambda l,h: l and h
    lv = txBusFilter(bus=lv_bus, level='lv_bus')
    hv = txBusFilter(bus=hv_bus, level='hv_bus')
    lv_hv = pd.Series(map(combine, lv, hv))

    # identify position of specified transformer in transforemer table
    txIndex = net.trafo[lv_hv].index[0]

    # apply ne tap position
    data = pd.Series([tapPos], name='tap_pos', index=[txIndex])
    net.trafo.update(data)

# Shunt Element Adjustment
def updateShunt(net, bus, mvarVal):
    shuntIndex = net.shunt[net.shunt.bus == bus].index[0]
    data = pd.Series([mvarVal], name='q_mvar', index=[shuntIndex])
    net.shunt.update(data)

# Setting & Enforcing voltage constraints - use cost function
# Setting & Enforcing Thermal constraints - use cost function

# Fitness Evaluation (Loss and cost calculation)
'''

(A * line loss + B * thermal violation + C * voltage violation)
'''
