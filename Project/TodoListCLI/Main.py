from Task import Task
#TodoList main
#We will use a loop on the file 
print('What file would you like to open ? ( A new file will be create if the file didnt exist yet) : ')
filename = input()

def load_task(file) : # this method help us get task that already in file
    taskList = []
    with open(file, 'a') as create :
        pass

    with open (file, 'r') as f :
        for line in f :
            line = line.strip() # this will remove any \n ( truthy string )
            if not line : # check if there is a blank line in the file
                continue
            name, id, day, month, done = line.split(';')
            t = Task(name, int(id), day, month)
            if done == 'V' :
                t.Done()
            taskList.append(t)
    
    return taskList

def save_tasks(file, taskList) : # this method help us save
    with open( file, 'w') as f :
        for x in taskList :
            f.write(str(x).rstrip('\n') + '\n')
            
            
force_quit = 0
taskList = load_task(filename)
print('The todolist will be represent with format : name,id,day,month,status')

while force_quit != 5 :
    print('-----What do you want to do ?-----')
    print('Choose between these actions : 1.Add a task  2.Show all task  3.Delete a task  4.Note a task as done  5.Finsish TodoList' )
    mode = input()

    idTask = 1 if not taskList else max(int(t.getID()) for t in taskList) + 1

    if mode == '1' :
        print('Please enter the task name :')
        taskName = input()
        print('Please enter the due date :')
        dueDate = input()
        while int(dueDate) > 31 or int(dueDate) < 1 or not dueDate.isdigit()  :
            print('The date must be lower than 31 and greater than 0 and must be a number')
            dueDate = input()
        print('And the due month :')
        dueMonth = input()
            
        task = Task ( taskName, idTask, dueDate, dueMonth )
        taskList.append(task)
        print('Task added') 
        save_tasks(filename, taskList)
                        
            
    elif mode ==  '2':
        print('Here is your to do list :')
        if taskList == [] :
            print('Dust...yeah there is nothing but DUST!!!')
        for x in taskList :
            print(str(x))

    elif mode == '3' :
        print('What task would you like to delete ? Please enter the ID of the task : ')
        deleteTaskID = input()
        taskList = [x for x in taskList if x.getID() != int(deleteTaskID)]
        save_tasks(filename, taskList)
            
    elif mode == '4':
        print('What task do you want to note as done ? Please enter the ID of the task : ')
        doneTaskID = input()
        for x in taskList : 
            if x.getID() == int(doneTaskID) :
                x.Done()
        save_tasks(filename, taskList)

    elif mode == '5':
        print('Thank you for using Tungs super awesome TODOList !!!')
        force_quit = 5
    else :
        print('Invalid mode choice!! Please dont do that')

save_tasks(filename, taskList)