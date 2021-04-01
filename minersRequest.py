#Python3
#Author Aidan Mellin

import requests
import pprint
import math

def request(ID,call):
    """
    Generate request with given ID and run specific call

    Args:
        ID (str): ID Associated with eth.2miners
        call (str): which method to run
    """
    req = requests.get("https://eth.2miners.com/api/accounts/"+ID)

    if 'json' in req.headers.get('Content-Type'):
        rJson = req.json()
    else:
        print('Response content is not in JSON format.')
        rJson = 'spam'

    dec_bal = 9

    called = {
        'h': avg_hash(rJson['hashrate']), #Get hashrate
        'b': get_balance(rJson['stats'].get('balance'),dec_bal), #Get balance
        'w': get_workers(rJson["workers"]),
        'a': get_all(ID,rJson['hashrate'],rJson['stats'].get('balance'),dec_bal,rJson["workers"])    
    }
    
    return called[call]

    
def get_spaces(ID,tmp):
    """
    Returns the amount of spaces necessary to make the box look nice

    Args:
        tmp (str): the string to be used to calculate

    Returns:
        str : Amount of spaces necessary
    """
    return " " * (len(ID) - len(tmp))

def get_all(ID,hr, bal, dec, wkrs):  
    """
    Prints all data in a nice box

    Args:
        hr (int): [Average hashrate as returned by 2Miners]
        bal (int): [Current balance of ID used]
        dec (int): [The amount of decimal places 2Miners API returns with]
        wkrs (list[dict]): [List of workers containing some data in a dict]

    Returns:
        [str]: Pretty printed version
    """
    
    spacer = "`| "+ "-"*len(ID) +" |`\n" #Spacer in between lines (nice looking)
    ret_str = spacer #Init the string with a topper to the box as spacer
    
    calls = [ #The current calls that can be made to all (leaves open to more implementation)
        ID,
        "Current Balance: "+ str(get_balance(bal,dec)),
        "Avg Hash: "+str(avg_hash(hr)),
    ]
    workers = get_workers(wkrs) #Call to get list of workers with offline state
            
    ret_str += "".join(["`| "+i+get_spaces(ID,i)+" |`\n"+spacer for i in calls])
    ret_str += "`| Workers:" + get_spaces(ID,"Workers:")+" |`\n"+"".join(["`|      "+i+get_spaces(ID,"     "+i)+" |`\n"+spacer for i in workers])
    return ret_str

def req_overall(rJson):
    """Get all Request JSON keys

    Args:
        rJson (list[dict]): the returned keys of requests.json
    """
    print(rJson.keys())

def get_workers(workers):
    """
    List of workers associated with Hash ID

    Args:
        workers (list[dict]): list of workers 

    Returns:
        list: list of workers + offline state
    """
    ret = [i+": Offline = "+str(workers[i]['offline']) for i in workers.keys()]
    return ret

def avg_hash(hr):
    """
    Returns average hashrate associated with ID

    Args:
        hr (int): received hash (not expressed correctly)

    Returns:
        [float]: 
    """
    ret_hr = hr * (math.pow(10,-6))
    return ret_hr

def get_balance(bal,dec):
    """
    Gets balance associated with eth.2miners.com

    Args:
        bal (int): balance of acct
        dec (int): Number of decimals to round to

    Returns:
        float: The properly expressed balance
    """
    #Length of returned string can be any size. However, it only counts up to 9 decimal places. 
    return bal*math.pow(10,-dec )

def minerChart(rJson):
    """
    Prints list of miners associated with ID

    Args:
        rJson (requests.json): miners
    """
    minerCharts = rJson["minerCharts"]
    for i in minerChart:
        if not (i["workerOnline"] == 0):
            pprint.pprint(i)