def help_main(help_args):
    help_args = list(help_args)
    resp = ''
    if len(help_args) < 1: #No arg with help call
        resp = "Usage:\n**~help\n\
            [\n\
            bugfact\n\
            check\n\
            clear** *owner command* **\n\
            horny\n\
            joker\n\
            miner\n\
            monke\n\
            note\n\
            status\n\
            todo\n\
            ]**"
    else: #Help call containing arg
        call = help_args[0]
        
        if "bugfact" in call:
            resp = "This function sends a random bugfact, or a specific one if you know the number call\nUsage:\n\t**~bugfact [optional: bugfact_number]**"
        elif "check" in call:
            resp = "This function manually checks the status of the daily health screen and returns whether or not it has been completed successfully\nUsage:\n**~check**"
        elif "clear" in call:
            resp = "This function clears the indicated channel\nUsage:\n\t**~clear**"
        elif "horny" in call: #Open horny.txt
            with open('help/horny.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        elif "joker" in call: #Open joker.txt
            with open('help/joker.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        elif "miner" in call:
            with open('help/miner.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        elif "monke" in call: #Open monke.txt
            with open('help/monke.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        elif "status" in call:
            resp = "This function manually updates the status of the bot as configured in the main py file\nUsage:\n\t**~status**"
        elif "todo" in call: #Open todo.txt
            with open('help/todo.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        else:
            resp = "invalid call"
            
    return resp
