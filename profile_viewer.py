import streamlit as st
from pymongo import MongoClient
import log_util
import matplotlib.pyplot as plt
import plot_util
import pandas as pd
import plotly.graph_objects as go

labels = {
            'iteration': 'Number of Iterations',
            'timeElapsed': 'Time Elapsed (seconds)',
            'bestFitness': 'Power Loss (MW)'}

hide_menu_style = """
        <style>
        html {background-color: white;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.title('Power Loss Minimization with PSO - Code Profile')
st.header('Duration in seconds of different stages in the algorithm')

source = st.sidebar.selectbox("Select data source", ['database', 'file'], 1)

profiles = st.sidebar.multiselect("Select run profile", log_util.getAvailableProfiles(source))

table = pd.DataFrame()
for profile in profiles:
    data = log_util.getProfileData(profile, source)
    table = table.join(pd.DataFrame(data, index=[profile]).T, how='right')

st.table(table.T)

plot = st.sidebar.radio('Select one', ['pie', 'line','bar'])

if plot == 'pie':
    to_plot = st.sidebar.selectbox('Select profile to plot', profiles)
    plotData = {i:table[to_plot].loc[i] for i in table.index}
    fig = plot_util.plotProfile(plotData, title='Runtime Breakdown: '+to_plot)
    st.plotly_chart(fig)

elif plot =='line':
    defaults = ['Fitness Evaluation', 'PersonalBest Updates']
    to_plot = st.sidebar.multiselect('Select profile to plot', list(table.index),defaults)
    fig = go.Figure()

    for component in to_plot:
        x = [log_util.getNumParticles(p) for p in table.columns]
        y = list(table.loc[component])
        name = component
        fig = plot_util.plotLine(x, y, name, fig)

    fig.update_layout(title='Duration vs Number of Particles',
                      xaxis_title='Number of Particles',
                      yaxis_title='Duration (seconds)')
    st.plotly_chart(fig)

elif plot =='bar':
    data = table.T.reset_index()
    fig = plot_util.plotBar(data)
    fig.update_layout(title='Runtime Breakdown',
                      xaxis_title='Run',
                      yaxis_title='Duration (seconds)')
    st.plotly_chart(fig)
