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
    endepoch = None

    def __init__(self):
        """Initialize."""
        self.LAT = list()
        self.LON = list()
        self.value = list()
        self.epoch = None


def roundb(num, base=10):
    return int(base * round(float(num) / base))


def process(targetpath, storepath, interval, start=None, end=None, bound=None, colorbar=100, ratio=10./8):
    """"process.

    Args:
        targetpath:target file path.
        storepath:store file path.
        interval:plot interval.
        bound:bound
        colorbar:colorbar range
        ratio:ratio
    """
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
        if not start:
            epoch = TecMap.startepoch
        else:
            hm = map(int, start.split(':'))
            epoch = TecMap.startepoch
            epoch = datetime.datetime(epoch.year, epoch.month, epoch.day, hm[0], hm[1], 0)
            TecMap.startepoch = epoch
        if end:
            hm = map(int, start.split(':'))
            endepoch = TecMap.startepoch
            endepoch = datetime.datetime(epoch.year, epoch.month, epoch.day, hm[0], hm[1], 0)
            TecMap.endepoch = endepoch
        for line in f:
            if 'START OF TEC MAP' in line:
                tecmap = TecMap()
                if not readtecmap(f, interval, tecmap):
                    continue
                plottecmap(tecmap, storepath, bound, colorbar, ratio)
                if TecMap.endepoch:
                    if epoch == TecMap.endepoch:
                        break
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


def readtecmap(f, interval, tecmap):
    """read tec map data.

    Arg:
        f:file handle.
        interval:interval.
        tecmap:Tec Map.
    """
    try:
        for line in f:
            if 'EPOCH OF CURRENT MAP' in line:
                datelst = map(int, line[:line.index('E')].split())
                cur_epoch = datetime.datetime(*datelst)
                seconds = int((cur_epoch - TecMap.startepoch).total_seconds())
                if seconds % interval != 0:
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


def plottecmap(tecmap, storepath, bound=None, colorbar=100, ratio=10./8):
    """Plot tecmap.

    Arg:
        tecmap:Tec Map.
        storepath:store file path.
        bound:bound
        ratio:axes ratio
    """
    try:
        plt.style.use('ggplot')
        if not bound:
            lonmin = TecMap.lonrange[0]
            lonmax = TecMap.lonrange[1]
            latmin = TecMap.latrange[1]
            latmax = TecMap.latrange[0]
        else:
            lonmin = bound[0]
            lonmax = bound[1]
            latmin = bound[2]
            latmax = bound[3]
        m = Basemap(
            projection='cyl',
            llcrnrlon=lonmin,
            urcrnrlon=lonmax,
            llcrnrlat=latmin,
            urcrnrlat=latmax,
            fix_aspect=False)
        m.aspect = ratio
        m.drawparallels(
            np.arange(roundb(latmin), latmax, 10),
            labels=[1, 0, 0, 0],
            linewidth=0,
            size=10,
            weight='bold')
        m.drawmeridians(
            np.arange(roundb(lonmin), lonmax, 10),
            labels=[0, 0, 0, 1],
            linewidth=0,
            size=10,
            weight='bold')
        m.drawcoastlines()
        m.drawcountries()

        m.pcolormesh(
            tecmap.LON,
            tecmap.LAT,
            tecmap.value,
            vmin=0,
            vmax=colorbar,
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
        raise
        return
