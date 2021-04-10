'''
Author: Brian Mukeswe
Date: Novemebr 9, 2020
Email: b.mukeswe@sms.ed.ac.uk
Purpose: This code includes custom utility functions for reading the control parameters
         of a power system network model. These functions are used as part of the 
         Particle Swarm Optimization algorithm implemetation.
'''
import pandas as pd

def appendColumn(df, name, value):
    # append a constant value column to a dataframe
    newCol = pd.Series([value for i in df.index],
                       index=df.index,
                       name=name)

    return pd.DataFrame(df).join(newCol)

def getGenRealPower(net):
    # read generation data from network
    param_data = net.gen[['p_mw', 'min_p_mw', 'max_p_mw']]

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
    param_data = net.gen.vm_pu
    param_data.name = 'params'

    param_data = appendColumn(df=param_data,
                              value='vSched',
                              name='paramType')

    param_data = appendColumn(df=param_data,
                              value=0.95,
                              name='minVal')
    param_data = appendColumn(df=param_data,
                              value=1.05,
                              name='maxVal')

    param_data = appendColumn(df=param_data,
                              value='continuous',
                              name='numType')
    return param_data

def getTrafoTapPosition(net):
    param_data = net.trafo.tap_pos
    param_data.name = 'params'
    param_data = appendColumn(df=param_data,
                              value='tx2winding',
                              name='paramType')

    param_data = appendColumn(df=param_data,
                              value=-3,
                              name='minVal')
    param_data = appendColumn(df=param_data,
                              value=3,
                              name='maxVal')

    param_data = appendColumn(df=param_data,
                              value='discrete',
                              name='numType')
    return param_data

def get3WTrafoTapPosition(net):
    param_data=net.trafo3w.tap_pos
    param_data.name = 'params'
    param_data = appendColumn(df=param_data,
                              value='tx3winding',
                              name='paramType')

    param_data = appendColumn(df=param_data,
                              value=-3,
                              name='minVal')
    param_data = appendColumn(df=param_data,
                              value=3,
                              name='maxVal')

    param_data = appendColumn(df=param_data,
                              value='discrete',
                              name='numType')
    return param_data

def getshunt(net):

    param_data = param_data=net.shunt.step
    param_data.name = 'params'
    param_data = appendColumn(df=param_data,
                              value='shunt',
                              name='paramType')

    param_data = appendColumn(df=param_data,
                              value=1,
                              name='minVal')
    param_data = appendColumn(df=param_data,
                              value=3,
                              name='maxVal')

    param_data = appendColumn(df=param_data,
                              value='discrete',
                              name='numType')
    return param_data

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

    cols = ['index','paramType','numType','params','maxVal','minVal']

    return paramArray.reset_index()[cols]
