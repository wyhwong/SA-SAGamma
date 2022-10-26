import numpy as np

# Convert the vector in "strumfric" coordinates to Cartesian coordinates
# here a is the vector being converted, b is the "strumfric" coordinates
def strum2cart(a, b):
    c_x = (a[0]*np.sin(np.arccos(b[1]))*np.cos(b[2]) - a[1]*b[1]*np.cos(b[2])/np.sqrt(1-b[1]**2) - a[2]*np.sin(np.arccos(b[1]))*np.sin(b[2]))
    c_y = (a[0]*np.sin(np.arccos(b[1]))*np.sin(b[2]) - a[1]*b[1]*np.sin(b[2])/np.sqrt(1-b[1]**2) + a[2]*np.sin(np.arccos(b[1]))*np.cos(b[2]))
    c_z = (a[0]*b[1] + a[1])
    c = np.array([c_x, c_y, c_z])
    return c
