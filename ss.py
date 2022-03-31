data = dict()
data[Exception] = "Parsa"


try:
    raise TypeError
except (ValueError, TypeError) as err:
    print("err")
