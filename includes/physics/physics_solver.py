from includes.physics.physicssolver import PhysicsSolver
from includes.physics.physicsequations import variables, equations

def physics_solver():
  p=PhysicsSolver("Physics Solver", variables(), equations())
  p.solve()