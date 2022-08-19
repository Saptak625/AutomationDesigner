def variables():
  return ['s', 'u', 'v', 'a', 't', 'F', 'm', 'p', 'deltav', 'J', 'W', 'K', 'U', 'g', 'h']

def equations():
  return [#Kinematics
          ('s', 'u*t+(a*t**2)/2'), 
          ('v', 'u+a*t'), 
          ('v**2', 'u**2+2*a*s'), 
          ('s', 't*(u+v)/2'), 
          ('s', 'v*t-(a*t**2)/2'),
          #Newton Second Law
          ('F', 'm*a'),
          #Momentum
          ('p', 'm*v'),
          #Impulse
          ('J', 'F*t'),
          ('F*t', 'm*deltav'),
          #Work
          ('W', 'F*s'),
          #Energy
          ('K', '(m*v**2)/2'),
          ('U', 'm*g*h')
          ]