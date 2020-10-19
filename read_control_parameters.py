import pandas as pd

#TBD - To delete
def addParamTypeCol(param_data, param_type):
    paramType = pd.Series([param_type for i in param_data.index],
                          index=param_data.index,
                          name='paramType')

    return param_data.join(paramType)

# TBD - To delete
def addParamNumTypeCol(param_data, num_type):
    numType = pd.Series([num_type for i in param_data.index],
                          index=param_data.index,
                          name='numType')

    return param_data.join(numType)

def appendColumn(df, name, value):
    # append a constant value column to a dataframe
    newCol = pd.Series([value for i in df.index],
                       index=df.index,
                       name=name)

    return df.join(newCol)

def getGenRealPower(net):
    # read generation data from network
    param_data = net.res_gen[['p_mw', 'min_p_mw', 'max_p_mw']]

    # change names to match other parameters
    param_data = param_data.rename(columns={
                                        'p_mw': 'params',
                                        'min_p_mw': 'minVal',
                                        'max_p_mw': 'maxVal'})

    # add parameter label colums
    param_data = appendColumn(df=param_data,
                              value='realPower',
                              name='paramType')

    # set continious/discrete flag column
    param_data = appendColumn(df=param_data,
                              value='continuous',
                              name='numType')
    return param_data

def getGenVsched(net):
    param_data=net.res_gen.vm_pu

    param_data = appendColumn(df=param_data,
                              value='vSched',
                              name='paramType')

    param_data = appendColumn(df=param_data,
                              value='continuous',
                              name='numType')
    return data

def getTrafoTapPosition(net):
    data = addParamTypeCol(param_data=net.trafo.tap_pos,
                           param_type='tx2winding')
    return data

def get3WTrafoTapPosition(net):
    data = addParamTypeCol(param_data=net.trafo3w.tap_pos,
                           param_type='tx3winding')
    return data

def getshunt(net):
    data = addParamTypeCol(param_data=net.shunt.step,
                           param_type='shunt')
    return data

def get1DparameterArray(net):

    params = {
        'realPower': getGenRealPower(net),
        'vSched': getGenVsched(net),
        'tx2winding': getTrafoTapPosition(net),
        'tx3winding': get3WTrafoTapPosition(net),
        'shunt': getshunt(net)
        }

    paramArray = pd.Series([], name='params')

    for parameter in params:
        paramArray = pd.concat([paramArray, params[parameter]])

    return paramArray.reset_index()[['index','paramType','params']]
