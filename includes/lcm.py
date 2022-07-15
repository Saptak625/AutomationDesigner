from includes.gcd import gcd
def lcm(number1, number2):
  return (abs(number1 * number2) // gcd(number1, number2))