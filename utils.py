SMALL_FLOAT = 0.005

def eq_z(num:float) -> bool:
    return (-SMALL_FLOAT < num and num < SMALL_FLOAT)

def sign_of(num:float) -> float:
    if (eq_z(num)):
        return 0
    if (num < 0.0):
        return -1.0
    return 1.0
