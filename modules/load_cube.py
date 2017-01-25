import numpy 
import math

class atom(object): 
  def __init__(self, zin, charge, x, y, z):
    self.__z = zin
    self.__coordinates = (x, y, z)
    self.__charge = charge
  
  def set_Z(self, zin): 
    self.__z = zin
  
  def get_Z(self):
    return self.__z

  def set_coordinates(self, x, y, z):
    self.__coordinates = (x, y, z)

  def get_x(self):
    return self.__coordinates[0]

  def get_y(self):
    return self.__coordinates[1]

  def get_z(self):
    return self.__coordinates[2]

  def get_coordinates(self):
    return self.__coordinatess

  def set_charge (self, charge):
    self.__charge = charge

  def get_charge (self):
    return self.__charge

  def get_str(self):
    return '%4d %10.6f %10.6f %10.6f %10.6f' % (self.__z, 
        self.__charge, self.__coordinates[0], self.__coordinates[1],
        self.__coordinates[2])

  def __repr__(self): # overloads printing
    return self.get_str()
 
class cube(object):

  def __init__(self, fname):

      self.__atoms = []
      self.__natoms = 0
      self.__nx = 0
      self.__ny = 0
      self.__nz = 0
      self.__data = numpy.zeros((1,1,1))
      self.__origin = numpy.zeros((1,1,1))
      self.__x = numpy.zeros((1,1,1))
      self.__y = numpy.zeros((1,1,1))
      self.__z = numpy.zeros((1,1,1))

      f = open(fname, 'r')
      
      for i in range(2): 
          f.readline() 
      
      line = f.readline().split() 
      self.__natoms = int(line[0])
      self.__origin = numpy.array([float(line[1]), \
          float(line[2]), \
          float(line[3])]) 
      
      line = f.readline().split() 
      self.__nx = int(line[0])
      self.__x = numpy.array([float(line[1]), \
              float(line[2]), \
              float(line[3])])
      
      line = f.readline().split() 
      self.__ny = int(line[0])
      self.__y = numpy.array([float(line[1]), \
              float(line[2]), \
              float(line[3])])
      
      line = f.readline().split() 
      self.__nz = int(line[0])
      self.__z = numpy.array([float(line[1]), \
              float(line[2]), \
              float(line[3])])
      
      for i in range(self.__natoms):
          line = f.readline().split()
          a = atom(int(line[0]), float(line[1]),  float(line[2]), \
                float(line[3]),  float(line[4]))
          self.__atoms.append(a)
        
      self.__data = numpy.zeros((self.__nx,self.__ny,self.__nz))
      i = 0
      for s in f:
          for v in s.split():
              self.__data[i/(self.__ny * self.__nz), \
                  (i/self.__nz)%self.__ny, \
                  i % self.__nz] = float(v)
              i += 1
      
      if i != self.__nx * self.__ny * self.__nz: 
          raise NameError, "Errore while reading cube file"


  def clear(self):
      self.__atoms = []
      self.__natoms = 0
      self.__nx = 0
      self.__ny = 0
      self.__nz = 0
      self.__data = numpy.zeros((1,1,1))
      self.__origin = numpy.zeros((1,1,1))
      self.__x = numpy.zeros((1,1,1))
      self.__y = numpy.zeros((1,1,1))
      self.__z = numpy.zeros((1,1,1))


  def get_natoms(self):
      return self.__natoms


  def get_atoms(self):
      return self.__atoms


  def get_data(self):
      return self.__data


  def set_data(self, newd):
      self.__data = newd


  def get_origin(self):
      return self.__origin


  def get_nx(self):
      return self.__nx


  def get_ny(self):
      return self.__ny


  def get_nz(self):
      return self.__nz

  def get_dx(self):
      return self.__x[0]


  def get_dy(self):
      return self.__y[1]


  def get_dz(self):
      return self.__z[2]


  def get_x(self):
      return self.__x


  def get_y(self):
      return self.__y


  def get_z(self):
      return self.__z

  def integrate (self, axis=""):

      if axis == "":
          itgr = numpy.sum(self.__data) * self.get_dx() * self.get_dy() * \
                  self.get_dz()
          return itgr
      elif axis == "xy":
          itgr = numpy.sum(self.__data, axis=(0,1)) * self.get_dx() * self.get_dy()
          return itgr
      elif axis == "yz":
          itgr = numpy.sum(self.__data, axis=(1,2)) * self.get_dy() * self.get_dz()
          return itgr
      elif axis == "xz":
          itgr = numpy.sum(self.__data, axis=(0,2)) * self.get_dx() * self.get_dy()
          return itgr

      return None

  def get_volume(self):

      vol = (self.__nx - 1) * self.get_x() * \
            (self.__ny - 1) * self.get_y() * \
            (self.__nz - 1) * self.get_z()

      return vol

  def get_str(self):

      str = "%4d %.6f %.6f %.6f\n" % \
              (self.__natoms, self.__origin[0], self.__origin[1], \
              self.__origin[2])
      str += "%4d %.6f %.6f %.6f\n"% \
              (self.__nx, self.__x[0], self.__x[1], self.__x[2])
      str += "%4d %.6f %.6f %.6f\n"% \
              (self.__ny, self.__y[0], self.__y[1], self.__y[2])
      str += "%4d %.6f %.6f %.6f\n"% \
              (self.__nz, self.__z[0], self.__z[1], self.__z[2])

      for a in self.__atoms:
          str += a.get_str() + "\n"
      
      for ix in xrange(self.__nx):
          for iy in xrange(self.__ny):
              for iz in xrange(self.__nz):
                   str += "%.5e "% self.__data[ix,iy,iz]
                   if (iz % 6 == 5): 
                       str += '\n'
      
      return str


  def __repr__ (self):

      str = "cube file\ngenerated\n"
      str += self.get_str()
      
      return str

  def dump(self, f):

      print >> f, "cube file\ngenerated"
      print >> f, self.get_str()

  def mask_sphere(self, r, cx, cy, cz):
      # cut a sphere with radius r and center in [cx,cy,cz]
      
      m = 0 * self.__data
      ixmin = int(math.ceil((cx-r)/self.__x[0]))
      ixmax = int(math.floor((cx+r)/self.__x[0]))
      for ix in xrange(ixmin, ixmax):
          ryz = math.sqrt(r**2-(ix*self.__x[0]-cx)**2)
          iymin = int(math.ceil((cy-ryz)/self.__y[1]))
          iymax = int(math.floor((cy+ryz)/self.__y[1]))
        
          for iy in xrange(iymin, iymax):
              rz = math.sqrt(ryz**2 - (iy*self.__y[1]-cy)**2)
              izmin = int(math.ceil((cz-rz)/self.__z[2]))
              izmax = int(math.floor((cz+rz)/self.__z[2])) 
        
              for iz in xrange (izmin, izmax):
                  m[ix,iy,iz] = 1
        
      return m
