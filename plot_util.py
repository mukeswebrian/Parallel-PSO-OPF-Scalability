import log_util
import matplotlib.pyplot as plt

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

def plotRunQuantities(run, x_dim, x_label, y_dim, y_label, title, ax):

    data = log_util.getRunData(run)
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

def plotAverageData(nParticles, runType, x_dim, x_label, y_dim, y_label, title, ax):

    data = log_util.getAverageData(nParticles, runType)
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
