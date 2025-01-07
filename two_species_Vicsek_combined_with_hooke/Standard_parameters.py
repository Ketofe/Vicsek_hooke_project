import numpy as np
import File_for_accesing_src
from Create_groups import *


#If not specified these will be used
L=31.6
rho=0.5
N=int(rho*L**2)
v_0=0.1
eta=0
r=5
l=2.5
s,k=Create_groups([ [ [1,v_0/10 ], [-1,v_0/10 ]  ],[[-1,v_0/10 ],[1,v_0/10 ]]   ],N)
iterations=1000