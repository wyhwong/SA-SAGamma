import numpy as np
import matplotlib.pyplot as plt


def get_base_plot_3D(nrows=1, ncols=1, height=7, width=7, title="", ylabel="", xlabel="", spatial=True, tpad=2.5, lpad=0.1, bpad=0.12, fontsize=12):
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height), subplot_kw={'projection': '3d'})
    fig.tight_layout(pad=tpad)
    fig.subplots_adjust(left=lpad, bottom=bpad)
    fig.suptitle(title, fontsize=fontsize)
    fig.text(x=0.04, y=0.5, s=ylabel, fontsize=fontsize, rotation="vertical", verticalalignment='center')
    fig.text(x=0.5, y=0.04, s=xlabel, fontsize=fontsize, horizontalalignment='center')
    if spatial:
        if ncols==1 and nrows==1:
            axes.set(xlabel='X', ylabel='Y', zlabel='Z')
        else:
            axes[0].set(xlabel='X', ylabel='Y', zlabel='Z')
    return fig, axes


def plot_rss_surface(ax, rss, set_lims=True):
    phi = np.linspace(0, 2*np.pi, 100)
    theta = np.linspace(0, np.pi, 100)
    sphere_x_rss = rss * np.outer(np.cos(phi), np.sin(theta))
    sphere_y_rss = rss * np.outer(np.sin(phi), np.sin(theta))
    sphere_z_rss = rss * np.outer(np.ones(np.size(phi)), np.cos(theta))
    sphere_x_1 = np.outer(np.cos(phi), np.sin(theta))
    sphere_y_1 = np.outer(np.sin(phi), np.sin(theta))
    sphere_z_1 = np.outer(np.ones(np.size(phi)), np.cos(theta))
    if set_lims:
        ax.set(xlim3d=[-rss, rss], ylim3d=[-rss, rss], zlim3d=[-rss, rss])
    ax.plot_surface(sphere_x_rss, sphere_y_rss, sphere_z_rss,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.1)
    ax.plot_surface(sphere_x_1, sphere_y_1, sphere_z_1,  rstride=4, cstride=4, color='b', linewidth=0, alpha=0.2)
