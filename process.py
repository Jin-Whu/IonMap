#!/usr/bin/env python
# coding:utf-8
"""Read IONEX file and draw a ion map."""

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


class TecMap(object):
    """Tec Map."""

    latrange = None
    lonrange = None
    startepoch = None

    def __init__(self):
        """Initialize."""
        self.LAT = list()
        self.LON = list()
        self.value = list()
        self.epoch = None


def process(targetpath, storepath, interval):
    """"process.

    Args:
        targetpath:target file path.
        storepath:store file path.
        interval:plot interval.
    """
    try:
        interval = int(interval)
    except:
        print 'interval should be integer!'
        return

    if not os.path.exists(targetpath):
        print 'Nont find %s' % targetpath
        return

    if not os.path.exists(storepath):
        print 'Nont find %s' % storepath
        print 'Try to make it......'
        try:
            os.makedirs(storepath)
        except:
            print 'Make falied!'
            return

    with open(targetpath) as f:
        if not readheader(f):
            return
        epoch = TecMap.startepoch
        for line in f:
            if 'START OF TEC MAP' in line:
                tecmap = TecMap()
                if not readtecmap(f, epoch, tecmap):
                    continue
                plottecmap(tecmap, storepath)
                epoch += datetime.timedelta(seconds=interval)
            if 'START OF RMS MAP' in line:
                break


def readheader(f):
    """Read header.

    Arg:
        f:file handle.
    """
    try:
        for line in f:
            if 'EPOCH OF FIRST MAP' in line:
                datelst = map(int, line[:line.index('E')].split())
                startepoch = datetime.datetime(*datelst)
                TecMap.startepoch = startepoch
                continue
            if 'LAT1 / LAT2 / DLAT' in line:
                lats = map(float, line[:line.index('L')].split())
                TecMap.latrange = lats
                continue
            if 'LON1 / LON2 / DLON' in line:
                lons = map(float, line[:line.index('L')].split())
                TecMap.lonrange = lons
                continue
            if 'END OF HEADER' in line:
                return 1
    except:
        return 0


def readtecmap(f, epoch, tecmap):
    """read tec map data.

    Arg:
        f:file handle.
        epoch:epoch of tec map.
        tecmap:Tec Map.
    """
    try:
        for line in f:
            if 'EPOCH OF CURRENT MAP' in line:
                datelst = map(int, line[:line.index('E')].split())
                cur_epoch = datetime.datetime(*datelst)
                if cur_epoch != epoch:
                    return 0
                tecmap.epoch = cur_epoch
                continue
            if 'LAT/LON1/LON2/DLON/H' in line:
                LAT = float(line[1:8])
                LON1 = float(line[8:14])
                LON2 = float(line[14:20])
                DLON = float(line[20:26])
                LONS = np.arange(LON1, LON2 + DLON, DLON).tolist()
                tecmap.LAT.append([LAT] * len(LONS))
                tecmap.LON.append(LONS)
                values = list()
                for i in range(int(np.ceil(len(LONS) / 16.))):
                    temp = next(f)
                    for value in temp.split():
                        values.append(float(value) * 0.1)
                tecmap.value.append(values)
                continue
            if 'END OF TEC MAP' in line:
                return 1
    except:
        return 0


def plottecmap(tecmap, storepath):
    """Plot tecmap.

    Arg:
        tecmap:Tec Map.
        storepath:store file path.
    """
    try:
        plt.style.use('ggplot')
        m = Basemap(
            projection='cyl',
            llcrnrlon=TecMap.lonrange[0],
            urcrnrlon=TecMap.lonrange[1],
            llcrnrlat=TecMap.latrange[1],
            urcrnrlat=TecMap.latrange[0])
        m.drawparallels(
            np.linspace(-80, 80, 5),
            labels=[1, 0, 0, 0],
            linewidth=0,
            size=10,
            weight='bold')
        m.drawmeridians(
            np.linspace(-180, 180, 7),
            labels=[0, 0, 0, 1],
            linewidth=0,
            size=10,
            weight='bold')

        m.pcolormesh(
            tecmap.LON,
            tecmap.LAT,
            tecmap.value,
            vmin=0,
            vmax=100,
            shading='gouraud',
            latlon=True)
        cb = m.colorbar(location='right', size="5%", pad='2%')
        cb.ax.set_title('TECU', size=10, weight='bold')
        plt.setp(cb.ax.yaxis.get_ticklabels(), size=10, weight='bold')
        plt.title(str(tecmap.epoch), size=18, weight='bold')
        fig_name = '%s.png' % tecmap.epoch.strftime('%Y-%m-%d-%H-%M-%S')
        fig_path = os.path.join(storepath, fig_name)
        plt.savefig(fig_path, bbox_inches='tight')
        plt.clf()
        plt.close()
    except:
        return
