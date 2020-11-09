import streamlit as st
from pymongo import MongoClient
import log_util
import matplotlib.pyplot as plt
import plot_util

labels = {
            'iteration': 'Number of Iterations',
            'timeElapsed': 'Time Elapsed (seconds)',
            'bestFitness': 'Power Loss (MW)'}

hide_menu_style = """
        <style>
        html {background-color: #EDF1F9;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.title('Power Loss Minimization with PSO')
st.header('Run Viewer')

consolidate = st.sidebar.radio("Select one",
                        ['plot average data','plot individual runs'])

x_dim = st.sidebar.selectbox('X dimension', sorted(list(labels.keys())))
y_dim = st.sidebar.selectbox('Y dimension', sorted(list(labels.keys())))

x_label = labels[x_dim]
y_label = labels[y_dim]
title = '{} vs {}'.format(y_label, x_label)
fig, ax = plt.subplots(**{'facecolor': '#EDF1F9'})

if consolidate=='plot individual runs':

    serial_runs = st.sidebar.multiselect('Select Serial Runs to be plotted',
                                         sorted(log_util.getSerialRuns()))
    parallel_runs = st.sidebar.multiselect('Select Parallel Runs to be plotted',
                                           sorted(log_util.getParallelRuns()))

    to_plot = serial_runs + parallel_runs


    if len(to_plot)>0:
        for run in to_plot:
            ax = plot_util.plotRunQuantities(run, x_dim, x_label, y_dim, y_label, title, ax)

        st.pyplot(fig)

    else:
        st.markdown('Select some data to display here ...')

elif consolidate == 'plot average data':
    parallel_nParticles = st.sidebar.multiselect('select parallel plots to be included', log_util.getParallelGroups())
    serial_nParticles = st.sidebar.multiselect('select serial plots to be included', log_util.getSerialGroups())


    for n in parallel_nParticles:
        ax = plot_util.plotAverageData(n, 'parallel', x_dim, x_label, y_dim, y_label, title, ax)

    for n in serial_nParticles:
        ax = plot_util.plotAverageData(n, 'serial', x_dim, x_label, y_dim, y_label, title, ax)

    st.pyplot(fig)

else:
    st.markdown('Select some data to display here ...')
