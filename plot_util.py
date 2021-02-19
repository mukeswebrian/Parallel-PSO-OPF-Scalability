'''
Author: Brian Mukeswe
Date: February 18, 2021
Email: b.mukeswe@sms.ed.ac.uk


Purpose: This script contains utility functions for plotting experimental
         data
'''

import log_util
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import math



plot_fmt = {
    'marker':'.',
}

ax_title_fmt = {
    'size':14
}

tick_fmt = {
    'size':'large'
}

legend_fmt = {
    'fontsize':14
}

title_fmt = {
    'size':16
}

text_fmt = {
    'fontsize':9,
}

def format_label(s):
    '''
    Function to format the legend label for a given run_name
    e.g
    s: parallel_particles60_processes12_run1
    return: 60-particles 12-processes
    '''
    tokens = s.split('_')
    nums = '0123456789'
    label = ''
    for token in tokens[1:3]:
        i = 0
        while (token[i] not in nums) and (i<len(token)):
            i += 1

        if token[i:]=='1':
            label += token[i:] + '-' + token[:i-2] + ' '
        else:
            label += token[i:] + '-' + token[:i] + ' '

    return label.strip()

def plotRunQuantities(run, x_dim, x_label, y_dim, y_label, title, ax, source):

    data = log_util.getRunData(run, source)
    label = format_label(run)
    data.rename(columns={y_dim: label}, inplace=True)
    data.plot(kind='line', x=x_dim, y=label, ax=ax, figsize=(10,8), **plot_fmt)

    plt.xlabel(x_label, fontdict=ax_title_fmt)
    plt.ylabel(y_label, fontdict=ax_title_fmt)
    plt.title(title, **title_fmt)
    plt.yticks(**tick_fmt)
    plt.xticks(**tick_fmt)
    plt.legend(**legend_fmt)
    plt.grid()

    return ax

def plotAverageData(nParticles, runType, x_dim, x_label, y_dim, y_label, title, ax, source, num_iter=25):

    data = log_util.getAverageData(nParticles, source, runType)
    data = data.query('iteration <= {}'.format(num_iter))
    if nParticles <=5:
        label = '{} particles - serial'.format(nParticles, runType)
    else:
        label = '{} particles'.format(nParticles, runType)

    data.rename(columns={y_dim: label}, inplace=True)
    data.plot(kind='line', x=x_dim, y=label, ax=ax, figsize=(10,8), **plot_fmt)

    plt.xlabel(x_label, fontdict=ax_title_fmt)
    plt.ylabel(y_label, fontdict=ax_title_fmt)
    plt.title(title, **title_fmt)
    plt.yticks(**tick_fmt)
    plt.xticks(**tick_fmt)
    plt.xlim(0, max(data[x_dim])+5)

    if nParticles == 144:
        plt.text(x=data[x_dim].iloc[-1], y=data[label].iloc[-1]+0.04, s=label,  **text_fmt)
    elif nParticles == 288:
        plt.text(x=data[x_dim].iloc[-1], y=data[label].iloc[-1]-0.04, s=label,  **text_fmt)
    else:
        plt.text(x=data[x_dim].iloc[-1], y=data[label].iloc[-1], s=label, **text_fmt)
    plt.legend(**legend_fmt) # plt.legend([], frameon=False)#
    plt.grid()

    return ax

def plotProfile(data, title):
    fig = go.Figure(data=[go.Pie(
            labels=list(data.keys()),#[i for i in data.index],
            values=list(data.values()),#[data.loc[i] for i in data.index],
            hole = .4,
          )])
    fig.update_layout(title_text=title)

    return fig

def plotLine(x, y, name, fig):
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=name))

    return fig

def plotBar(data):
    to_plot = list(data.columns)
    to_plot.remove('index')
    fig = px.bar(data, x='index', y=to_plot)
    return fig

def plotBar2(data):
    to_plot = list(data.columns)
    to_plot.remove('index')

    fig, ax = plt.subplots()
    data.to_excel('profile.xlsx')
    for part in data.index:
        data.plot(kind='barh', x='index', stacked=True, ax=ax)

    plt.legend(to_plot)
    label_fmt = lambda i: i[:-4].replace('particles', '') + ' particles'
    ax.set_yticklabels([label_fmt(i.get_text()) for i in ax.get_yticklabels()])
    plt.grid(axis='x')
    plt.title('Runtime Breakdown', **title_fmt)
    plt.ylabel('Duration (seconds)')
    plt.ylabel('Number of Particles')

    return fig
