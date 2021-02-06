def help_main(help_args):
    help_args = list(help_args)
    resp = ''
    if len(help_args) < 1: #No arg with help call
        resp = "Usage:\n**~help [monke/joker/horny/todo]**"
    else: #Help call containing arg
        call = help_args[0]
        if "monke" in call: #Open monke.txt
            with open('help/monke.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        elif "joker" in call: #Open joker.txt
            with open('help/joker.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        elif "horny" in call: #Open horny.txt
            with open('help/horny.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        elif "todo" in call: #Open todo.txt
            with open('help/todo.md','r') as fp:
                resp = f"{fp.read()}".format(**locals())
        else:
            resp = "invalid call"
    return resp
