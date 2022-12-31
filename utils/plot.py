#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt


def get_base_plot_3D(nrows=1, ncols=1, height=7, width=7, title="", ylabel="", xlabel="", spacial=True, tpad=2.5, lpad=0.1, bpad=0.12, fontsize=12):
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height), subplot_kw={'projection': '3d'})
    fig.tight_layout(pad=tpad)
    fig.subplots_adjust(left=lpad, bottom=bpad)
    fig.suptitle(title, fontsize=fontsize)
    fig.text(x=0.04, y=0.5, s=ylabel, fontsize=fontsize, rotation="vertical", verticalalignment='center')
    fig.text(x=0.5, y=0.04, s=xlabel, fontsize=fontsize, horizontalalignment='center')
    if spacial:
        if ncols==1 and nrows==1:
            axes.set(xlabel='X', ylabel='Y', zlabel='Z')
        else:
            axes[0].set(xlabel='X', ylabel='Y', zlabel='Z')
    return fig, axes


def get_sphere_surface(ax, rss):
    u = np.linspace(0, 2*np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    sphere_x_rss = rss * np.outer(np.cos(u), np.sin(v))
    sphere_y_rss = rss * np.outer(np.sin(u), np.sin(v))
    sphere_z_rss = rss * np.outer(np.ones(np.size(u)), np.cos(v))
    sphere_x_1 = np.outer(np.cos(u), np.sin(v))
    sphere_y_1 = np.outer(np.sin(u), np.sin(v))
    sphere_z_1 = np.outer(np.ones(np.size(u)), np.cos(v))
    elev = 10.0
    rot = 80.0 / 180 * np.pi
    ax.set(xlim3d=[-rss, rss], ylim3d=[-rss, rss], zlim3d=[-rss, rss])
    ax.plot_surface(sphere_x_rss, sphere_y_rss, sphere_z_rss,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.1)
    ax.plot_surface(sphere_x_1, sphere_y_1, sphere_z_1,  rstride=4, cstride=4, color='b', linewidth=0, alpha=0.2)
    #calculate vectors for "vertical" circle
    a = np.array([-np.sin(elev / 180 * np.pi), 0, np.cos(elev / 180 * np.pi)])
    b = np.array([0, 1, 0])
    b = b * np.cos(rot) + np.cross(a, b) * np.sin(rot) + a * np.dot(a, b) * (1 - np.cos(rot))
