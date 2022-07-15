def gcd(number1, number2):
  if number1 == 0 or number2 == 0:
    return number1 + number2
  else:
    absNumber1 = abs(number1)
    absNumber2 = abs(number2)
    biggerValue = max(absNumber1, absNumber2)
    smallerValue = min(absNumber1, absNumber2)
    return gcd(biggerValue % smallerValue, smallerValue)