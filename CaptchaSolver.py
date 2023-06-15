import os
from twocaptcha import TwoCaptcha
from timeit import default_timer as timer




def solve_it(Ss_name):
    dir = os.path.join(os.path.dirname(__file__), f'./Ss_captcha/{Ss_name}.png')
    
    api_key = os.getenv('2capthca api', 'cer')
    solver = TwoCaptcha(api_key)

    start = timer()
    try:
        result = solver.normal(dir)

    except Exception as e:
        print (e)

    else:
        code = result['code']
        print (f"captcha > {code}  T[{round(timer() - start, 3)}s]")


        # if not code.isnumeric():
        #     return -1

        return code

