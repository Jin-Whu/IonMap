# IonMap
Draw Ion map from ionex file.

# Dependency
1. **Python2.7**, **numpy**, **matplotlib**, **basemap**  

Notice:  
1. You can installed [Anaconda](http://pan.baidu.com/s/1boLcw27)
2. basemap installed use command `conda install package-name`

# Usage
`python main.py input output --start[-s] --end[-e] --interval[-i] --bound[-b] --colorbar[-c] --ratio[-r]`

Args:
- input:IONEX path  
- output:output directory  
- start:start epoch-HH:MM, default:start epoch of IONEX  
- end:end epoch-HH:MM, default:last epoch of IONEX  
- interval:interval(seconds), default:3600  
- bound:[lonmin,lonmax,latmin,latmax],default:IONEX range  
- colorbar:max value for colorbar,default:100  
- ratio:figure ratio, default:1.25  

Examples:
1. python main.py CODG001.17I .
2. python main.py CODG001.17I . -i 3600
3. python main.py CODG001.17I . -s 00:00
5. python main.py CODG001.17I . -s 00:00 -e 19:00
5. python main.py CODG001.17I . -b -180,180,-80,80
6. python main.py CODG001.17I . -r 1.25
7. python main.py CODG001.17I . -c 100
