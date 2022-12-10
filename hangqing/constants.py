import os, math

# Cosntants used for API functionalities, do not change

API_TOKEN = "e2faec93d69c35b1a9d348ca46fcf38726370474"

#CML格式代码
def breaker():
    """自动格式代码，适应CML宽度
    """
    term_size = os.get_terminal_size().columns
    half = math.floor((term_size-12)/2)
    print("\n" + '─' * half + " PKU TRADER " + '─' * half + "\n")
