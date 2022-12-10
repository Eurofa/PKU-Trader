import os, math, time

# Cosntants used for API functionalities, do not change

API_TOKEN = "e2faec93d69c35b1a9d348ca46fcf38726370474"

#CML格式代码
def breaker(content=" PKU TRADER "):
    """自动格式代码，适应CML宽度
    """
    term_size = os.get_terminal_size().columns
    
    if content == " PKU TRADER ":
        half = math.floor((term_size-12)/2)
        print("\n" + '─' * half + content + '─' * half + "\n")
    else:
        half = math.floor((term_size-len(content))/2)
        print("\n" + '─' * half + content + '─' * half + "\n")

def wait_t(n=0.5):
    time.sleep(n)
    
def qing():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
 
    else:
        _ = os.system('clear')