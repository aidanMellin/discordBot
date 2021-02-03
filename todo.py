def todo_main(todo_arg, p_arg):
	resp = ''
	if todo_arg[0] == 'add': #Adding things to todo list
		todo_add("todo_persist/"+str(ctx.message.author.id),todo_arg)
		resp = "TODO added"
	
	elif 'remove' in todo_arg[0] or "rm" in todo_arg[0]: #Remove a (batch) of todo(s)
		todo_rm("todo_persist/"+str(ctx.message.author.id), todo_arg)
		resp = "TODO deleted"

	elif todo_arg[0] == "view": #Print a formatted version of the user-specific todo list
		resp = todo_view("todo_persist/"+str(ctx.message.author.id))
        
	elif "p" in todo_arg[0][0]: #A prioritize method: Bolds the multiple? calls
		todo_p("todo_persist/"+str(ctx.message.author.id),todo_arg)
		resp = "TODO Prioritized"

	elif todo_arg[0] == "clear":
		open("todo_persist/"+str(ctx.message.author.id)+".txt", 'w').close()
		resp = "TODO Cleared"
	return resp

def todo_add(author, todo_arg):
    """
    TODO Add Function utility. Adds user indicated todo's to stored text files under todo_persist/
    """
    with open(author+".txt", 'a+') as fp: #Open as a+ so it appends to the bottom of the file (or crea
        fp.seek(0) #Redundancy
        todo_add = " ".join(todo_arg[1:]) #Each call will have one todo to add, so combine the split a
        fp.write(todo_add)
        fp.write("\n")

def todo_rm(author, todo_arg):
    """
    Removes already present todo's.
    """
    with open(author+".txt", 'r') as fp: #Read the lines and store to a list for easier manipulation
        lines = fp.readlines()
        if len(todo_arg) > 2: #Multiple rm calls
            rm_obj = todo_arg[1:]
            rm_obj = [int(i) for i in rm_obj] #Int all of the numbers in the list
            rm_obj.sort(reverse=True) #Sort in descending order to account for list deletion when remo
            for i in range(len(rm_obj)):
                del lines[int(rm_obj[i])-1]
        else: #Only one remove call
            del lines[int(todo_arg[1])-1]
        with open(author+".txt", 'w+') as fp:
            for line in lines:
              fp.write(line) #Rewrite the remaining lines from the lines list

def todo_view(author):
    """
    Prettyprint format of the TODO list
    """
    with open(author+".txt", 'r+') as fp:
        fp.seek(0) #Redundancy
        resp = ""
        line = fp.readline()
        if(line == ""): #Empty todo list
            resp = "Nothing currently in TODO List"
        count = 1
        while line: #Put the entire todo list in one formatted string so that there is no lag when sen
            resp += "".join(str(count)+". "+line)
            line = fp.readline()
            count += 1
    return resp

def todo_p(author, todo_arg):
    """
    Prioritizes user-indicated todo as known by the number on the list
    """
    with open(author+".txt", 'r+') as fp:
        pos = fp.tell()
        line = fp.readlines()
        line_manip = line[int(todo_arg[1])-1]
        print(line_manip)
        if not "*" in line_manip:
            line_manip = "**"+line[int(todo_arg[1])-1].strip("\n")+"**\n"
        else:
            time.sleep(2)
            print("removing **")
            line_manip = line_manip.replace("*","")
            print("New Line manip = "+line_manip)
        line[int(todo_arg[1])-1] = line_manip
    with open(author+".txt","w") as fp:
        for i in range(len(line_manip)):
            fp.write(line[i])
