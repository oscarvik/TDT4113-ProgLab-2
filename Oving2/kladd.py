history=[1,0,1,2,2,1,0,1,2,1,0,1,0,1,0,1,0,1,0,1,0,2,1,0,1]
x=history[-3:]
print("husk: "+str(x))

def subfinder(history, husk):
    matches = []
    for i in range(len(history)-len(husk)):
        if history[i] == husk[0] and history[i:i+len(husk)] == husk:
            matches.append(history[i+len(husk)])
    expected = max(set(matches), key=matches.count)
    if expected == 0:
        return 1
    elif expected == 1:
        return 2
    else:
        return 0



print(subfinder(history,x))
