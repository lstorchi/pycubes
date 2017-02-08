import sys

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

print cube

print cube.integrate()
vals = cube.integrate("xy")
#for v in vals:
#    print v
