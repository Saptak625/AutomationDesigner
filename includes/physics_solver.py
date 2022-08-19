from includes.physicssolver import PhysicsSolver
from includes.physicsequations import variables, equations

def physics_solver():
  p=PhysicsSolver("Physics Solver", variables(), equations())
  p.solve()