import log_util
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px



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

def plotRunQuantities(run, x_dim, x_label, y_dim, y_label, title, ax, source):

    data = log_util.getRunData(run, source)
    label = run
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

def plotAverageData(nParticles, runType, x_dim, x_label, y_dim, y_label, title, ax, source):

    data = log_util.getAverageData(nParticles, source, runType)
    label = '{} particles - {}'.format(nParticles, runType)
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
