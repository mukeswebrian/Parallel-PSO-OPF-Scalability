import pandas as pd

# Generator outputs
def updateGenRealPower(net, mwVal, bus=None, genIndex=None):
    # specifiy the either the bus number or the index
    # specify the new MW output level
    if genIndex is None:
        genIndex = net.gen[net.gen.bus == bus].index[0] # get gen's index in  gen table

    data = pd.Series([mwVal], name='p_mw', index=[genIndex])
    net.gen.update(data)

# Terminal Voltages (shceduled Voltages)
def updateGenVsched(net, puVal, bus=None, genIndex=None):
    # specifiy the either the bus number or the index
    # specify the new Scheduled pu voltage level
    if genIndex is None:
        genIndex = net.gen[net.gen.bus == bus].index[0] # get gen's index in  gen table

    data = pd.Series([puVal], name='vm_pu', index=[genIndex])
    net.gen.update(data)

# Transformer Tap Adjustment
def updateTrafoTapPosition(net, tapPos, lv_bus=None, hv_bus=None, txIndex=None):
    # specifiy the either the bus numbers or the index

    if txIndex is None:
        # filter the transformet table based on lv and hv buses
        txBusFilter = lambda bus, level: net.trafo[level]==bus
        combine = lambda l,h: l and h
        lv = txBusFilter(bus=lv_bus, level='lv_bus')
        hv = txBusFilter(bus=hv_bus, level='hv_bus')
        buses = pd.Series(map(combine, lv, hv))

        # identify position of specified transformer in transforemer table
        txIndex = net.trafo[buses].index[0]

    # apply ne tap position
    data = pd.Series([tapPos], name='tap_pos', index=[txIndex])
    net.trafo.update(data)

def update3WTrafoTapPosition(net, tapPos, lv_bus=None, mv_bus=None, hv_bus=None, txIndex=None):
    # specifiy the either the bus numbers or the index

    if txIndex is None:
    # filter the transformet table based on lv and hv buses
        txBusFilter = lambda bus, level: net.trafo3w[level]==bus
        combine = lambda l,m,h: all((l,m,h))
        lv = txBusFilter(bus=lv_bus, level='lv_bus')
        mv = txBusFilter(bus=mv_bus, level='mv_bus')
        hv = txBusFilter(bus=hv_bus, level='hv_bus')
        buses = pd.Series(map(combine, lv, mv, hv))

        # identify position of specified transformer in transforemer table
        txIndex = net.trafo[buses].index[0]

    # apply ne tap position
    data = pd.Series([tapPos], name='tap_pos', index=[txIndex])
    net.trafo.update(data)

# Shunt Element Adjustment
def updateShunt(net, mvarVal, bus=None, shuntIndex=None):
    # specifiy the either the bus numbers or the index

    if shuntIndex is None:
        shuntIndex = net.shunt[net.shunt.bus == bus].index[0]

    data = pd.Series([mvarVal], name='q_mvar', index=[shuntIndex])
    net.shunt.update(data)

def updateControlParams(net, param_data):

    def updateParam(i):
        param_type = param_data.loc[i].paramType

        if param_type == 'realPower':
            updateGenRealPower(net,
                               mwVal=param_data.loc[i].params,
                               genIndex=param_data.loc[i]['index'])
            return True

        elif param_type == 'vSched':
            updateGenVsched(net,
                            puVal=param_data.loc[i].params,
                            genIndex=param_data.loc[i]['index'])
            return True

        elif param_type == 'tx2winding':
            updateTrafoTapPosition(net,
                                   tapPos=param_data.loc[i].params,
                                   txIndex=param_data.loc[i]['index'])
            return True

        elif param_type == 'tx3winding':
            update3WTrafoTapPosition(net,
                                     tapPos=param_data.loc[i].params,
                                     txIndex=param_data.loc[i]['index'])
            return True

        elif param_type == 'shunt':
            updateShunt(net,
                        mvarVal=param_data.loc[i].params,
                        shuntIndex=param_data.loc[i]['index'])
            return True

        else:
            return False

    return all(map(updateParam, param_data.index))











# Setting & Enforcing voltage constraints - use cost function
# Setting & Enforcing Thermal constraints - use cost function
