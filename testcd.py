import sys
import numpy

import matplotlib.pyplot as plt

sys.path.append("./modules")
import load_cube

filenamea = ""
filenameb = ""
filenameab = ""

if (len(sys.argv)) != 4:
    print "Usage: ", sys.argv[0], " fileAB.cube fileA.cube fileB.cube"
    exit(1)
else:
    filenameab = sys.argv[1]
    filenamea = sys.argv[2]
    filenameb = sys.argv[3]

cubeAB = load_cube.cube(filenameab)
cubeA = load_cube.cube(filenamea)
cubeB = load_cube.cube(filenameb)

cube1 = cubeAB - cubeA
cube = cube1 - cubeB

#print cube

ymin = cube.get_origin()[1]
dy = cube.get_dy()
vals = cube.integrate("xy")
i = 0
xv = []
cd = []
vl = []
for v in vals:
    xv.append(ymin+i*dy) 
    cd.append(numpy.sum( vals[:i] ) * dy)
    vl.append(v)
    i = i + 1

plt.clf()
plt.plot(xv, cd, 'red', linestyle='--', linewidth=2, label='CD')
plt.plot(xv, vl, 'blue', linestyle='--', linewidth=2, label='VALUES')
legend = plt.legend(loc='upper right', shadow=True, fontsize='small')

plt.xlabel('X')
plt.ylabel('Y')
plt.show()

