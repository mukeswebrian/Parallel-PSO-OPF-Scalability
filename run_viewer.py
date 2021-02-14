import streamlit as st
from pymongo import MongoClient
import log_util
import matplotlib.pyplot as plt
import plot_util
import pandas as pd
import math

labels = {
            'iteration': 'Number of Iterations',
            'timeElapsed': 'Time Elapsed (seconds)',
            'bestFitness': 'Power Loss (MW)'}

hide_menu_style = """
        <style>
        html {background-color: white;}
        </style>
        """
st.set_page_config(layout='wide')
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.title('Power Loss Minimization with PSO')
#st.header('Run Viewer')

source = st.sidebar.selectbox("Select data source", ['database', 'file'], 1)
consolidate = st.sidebar.radio("Select one",
                        ['plot average data','plot individual runs','tabulate', 'plot impact of particles'])


fig, ax = plt.subplots(**{'facecolor': 'white'})

if consolidate=='plot individual runs':

    x_dim = st.sidebar.selectbox('X dimension', sorted(list(labels.keys())))
    y_dim = st.sidebar.selectbox('Y dimension', sorted(list(labels.keys())))

    x_label = labels[x_dim]
    y_label = labels[y_dim]
    title = '{} vs {}'.format(y_label, x_label)

    serial_runs = st.multiselect('Select Serial Runs to be plotted',
                                         sorted(log_util.getSerialRuns(source)))
    parallel_runs = st.multiselect('Select Parallel Runs to be plotted',
                                           sorted(log_util.getParallelRuns(source)))

    to_plot = serial_runs + parallel_runs


    if len(to_plot)>0:
        for run in to_plot:
            ax = plot_util.plotRunQuantities(run, x_dim, x_label, y_dim, y_label, title, ax, source)

        st.pyplot(fig)

    else:
        st.markdown('Select some data to display here ...')

elif consolidate == 'plot average data':
    x_dim = st.sidebar.selectbox('X dimension', sorted(list(labels.keys())))
    y_dim = st.sidebar.selectbox('Y dimension', sorted(list(labels.keys())))

    st.sidebar.markdown('> Additional parameters')
    num_iter = st.sidebar.slider('Number of iterations',1,50,25,1)

    x_label = labels[x_dim]
    y_label = labels[y_dim]
    title = '{} vs {}'.format(y_label, x_label)

    parallel_nParticles = st.sidebar.multiselect('select number of particles',
                                                  sorted(log_util.getParallelGroups(source)))
    #serial_nParticles = st.sidebar.multiselect('select serial plots to be included', sorted(log_util.getSerialGroups(source)))

    data = pd.DataFrame()

    for n in parallel_nParticles:
        ax = plot_util.plotAverageData(n, 'parallel', x_dim, x_label, y_dim, y_label, title, ax, source, num_iter)

    #for n in serial_nParticles:
    #    ax = plot_util.plotAverageData(n, 'serial', x_dim, x_label, y_dim, y_label, title, ax, source)

    st.pyplot(fig)

elif consolidate == 'plot impact of particles':
    table = []

    num_procs = st.sidebar.selectbox('select number of processes', sorted(log_util.getProcessCounts(source)))

    for n in sorted(log_util.getParallelGroups(source)):

        data = log_util.getAverageData(n, source, 'parallel', num_procs)
        if len(data)>0:
            table.append({'nparticles': n, 'bestFitness':data.bestFitness.min(), 'runtime':data.timeElapsed.max()})

    table = pd.DataFrame(table)

    table = table.query('nparticles>1')

    st.sidebar.markdown('> ### Additional parameters')
    use_log = st.sidebar.radio('select scale for number of particles', ['logarithmic', 'linear'])

    y_dim = st.sidebar.selectbox('Y dimension', ['bestFitness (MW)','runtime (s)'])
    fig, ax = plt.subplots()

    if use_log == 'logarithmic':
        table.nparticles = table.nparticles.apply(math.log)
        #table.bestFitness = table.bestFitness.apply(math.log)
        table.rename(columns={'nparticles':'log nparticles',
                              'bestFitness':'bestFitness (MW)',
                              'runtime':'runtime (s)'}, inplace=True)
        table.plot.scatter(x='log nparticles', y=y_dim, ax=ax)

    elif use_log == 'linear':
        table.rename(columns={'nparticles':'nparticles',
                              'bestFitness':'bestFitness (MW)',
                              'runtime':'runtime (s)'}, inplace=True)
        table.plot.scatter(x='nparticles', y=y_dim, ax=ax)

    st.pyplot(fig)
    st.table(table)


elif consolidate == 'tabulate':
    parallel_nParticles = st.sidebar.selectbox('select number of particles',
                                                  sorted(log_util.getParallelGroups(source)))
    table = log_util.getDataTable(parallel_nParticles, source, runType='parallel')

    fitness_table = table.pivot_table(index='iteration', columns=['run'], values='bestFitness')
    runtime_table = table.pivot_table(index='iteration', columns=['run'], values='timeElapsed')

    for i in fitness_table.columns[0].split('_'):
        if any(map(lambda x: x in i, ['particles', 'processes'])):
            st.info(i)

    col1, col2 = st.beta_columns((1,1))

    col1.info('### Fitness')
    fitness_table.rename(columns={c:c[-4:] for c in fitness_table.columns}, inplace=True)
    col1.table(fitness_table)

    col2.info('### Runtime')
    runtime_table.rename(columns={c:c[-4:] for c in runtime_table.columns}, inplace=True)
    col2.table(runtime_table)

else:
    st.markdown('Select some data to display here ...')
