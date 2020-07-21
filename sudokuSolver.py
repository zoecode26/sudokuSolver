from tkinter import *
from collections import Counter

root = Tk()
root.title("Sudoku Solver")
root.geometry("485x485")
root.resizable(0,0)

##root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file = 'C:/Users/zoeth/Documents/Coding/PythonProjects/Sudoku Solver/logo.png'))

changes = []
third = False

def collectData():
    alpha = False
    correctRange = True
    blanks = 0
    inputData = [ [ 0 for i in range(9) ] for j in range(9) ]
    for i in range(9):
        for j in range(9):
            currentPos = "square"+str(i)+str(j)
            valueToAdd = globals()[currentPos].get()
            inputData[i][j] = valueToAdd
            if valueToAdd == '':
                blanks+=1
            if valueToAdd.isalpha():
                alpha = True
            if alpha == False and valueToAdd!='':
                try:
                    if (int(valueToAdd)<0 or int(valueToAdd)>10):
                            correctRange = False
                except:
                    correctRange = False
    if alpha == False and correctRange == True and blanks != 0 and blanks != 81:
        firstAlgorithm(inputData, changes)

def findCombinations(inputData, changes):
    rows = []
    possnumbers = ['1','2','3','4','5','6','7','8','9']
    for i in range (9):
        row = []
        for j in range(9):
            if inputData[i][j]!= '':
                row.append(inputData[i][j])
        rows.append(row)
        

    columns = []
    for j in range (9):
        column = []
        for i in range(9):
            if inputData[i][j]!= '':
                column.append(inputData[i][j])
        columns.append(column)


    possoutcomesrows = []
    for i in range(9):
        tempList2 = []
        for j in range(9):
            res = [t for t in possnumbers if t not in rows[i]]
            if inputData[i][j]!='':
                tempList = [inputData[i][j]+"*"]
                tempList2.append(tempList)
            else:
                tempList2.append(res)
        possoutcomesrows.append(tempList2)


    columnsTemp = []
    for j in range(9):
        tempList2=[]
        for i in range(9):
            res = [t for t in possnumbers if t not in columns[j]]
            if inputData[i][j]!='':
                tempList = [inputData[i][j]+"*"]
                tempList2.append(tempList)
            else:
                tempList2.append(res)
        columnsTemp.append(tempList2)


    newList = []
    for j in range(9):
        for i in range(9):
            newList.append(columnsTemp[i][j])


    possoutcomescolumns = []
    for i in range (0, 80, 9):
        possoutcomescolumns.append(newList[i:i+9])


    possoutcomesfinal = []
    for i in range(len(possoutcomescolumns)):
        tempList = []
        for j in range(len(possoutcomescolumns[i])):
            list1 = (possoutcomesrows[i][j])
            list2 = (possoutcomescolumns[i][j])
            intersection = list(set(list1).intersection(list2))
            intersection.sort()
            tempList.append(intersection)
        possoutcomesfinal.append(tempList)


    boxList = []
    coordinates = [[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]
    for k in coordinates:
        tempList = []
        x = int(k[0])
        y = int(k[1])
        for i in range (x,x+3,1):
            for j in range (y,y+3,1):
                if possoutcomesfinal[i][j]!='':
                    tempList.append(possoutcomesfinal[i][j])

        boxList.append(tempList)

    
    boxes=[]
    for i in boxList:
        tempList = []
        for j in i:
            if len(j) == 1:
                for k in j:
                    if len(k) != 1:
                        tempList.append(j[0])
        boxes.append(tempList)

    for i in range(len(boxes)):
        for j in range(len(boxes[i])):
            value = boxes[i][j]
            value = value[0]
            for k in range(len(boxList[i])):
                if value in boxList[i][k]:
                    if len (boxList[i][k]) !=1:
                        boxList[i][k].remove(value)

    for i in range(len(boxList)):
        for j in range(len(boxList[i])):
            if (len(boxList[i][j]))==1:
                for k in range(len(boxList[i][j])):
                    valueToChange = boxList[i][j][k]
                    boxList[i][j][k] = valueToChange[0]

    firstArray = []                
    coordinates = [[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]
    for k in coordinates:
        x = int(k[0])
        y = int(k[1])
        for i in range (x,x+3,1):
            for j in range (y,y+3,1):
                firstArray.append(boxList[i][j])

    finalArray =[]
    for i in range(0, len(firstArray),9):
        finalArray.append(firstArray[i:i+9])

    return {"finalArray":finalArray,"boxList":boxList}

def firstAlgorithm(inputData, changes):
    blanks = 0
    for i in inputData:
        for j in i:
            if j == '':
                blanks+=1
    if blanks == 1 and len(changes)>0:
        checkSolution(inputData)
    else:

        result = findCombinations(inputData, changes)
        recursiveArray = result["finalArray"]
        boxList = result["boxList"]
        
        for i in range(len(recursiveArray)):
            for j in range(len(recursiveArray[i])):
                if (len(recursiveArray[i][j]))!= 1:
                    recursiveArray[i][j]=''
                else:
                    recursiveArray[i][j] = recursiveArray[i][j][0]

        solved = True
        for i in recursiveArray:
            for j in i:
                if j == '':
                    solved = False

        if solved == False:
            if inputData != recursiveArray:
                firstAlgorithm(recursiveArray, changes)
            else:
                secondAlgorithm(boxList, inputData, result["finalArray"], changes)
        else:
            arrayToDisplay = recursiveArray
            displaySolution(recursiveArray)


def secondAlgorithm(boxList, inputData, finalArray, changes):
    combinedLists = []
    for i in boxList:
        tempList = []
        for j in i:
            for k in j:
                tempList.append(k)
        combinedLists.append(tempList)


    combinedSets = []
    for i in combinedLists:
        tempList = []
        a_dict = Counter(i)
        for key in a_dict:
            if a_dict[key] == 1:
                tempList.append(key)
        combinedSets.append(tempList)


    boxes=[]
    for i in boxList:
        tempList = []
        for j in i:
            if len(j) == 1:
                tempList.append(j[0])
        boxes.append(tempList)


    remainingNumbers = []
    for i in range(len(boxes)):
        res = [t for t in combinedSets[i] if t not in boxes[i]]
        remainingNumbers.append(res)


    for i in range(len(boxList)):
        for j in range(len(boxList[i])):
            for k in range(len(remainingNumbers[i])):
                if remainingNumbers[i][k] in boxList[i][j]:
                    boxList[i][j] = [remainingNumbers[i][k]]

    firstArray = []                
    coordinates = [[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]
    for k in coordinates:
        x = int(k[0])
        y = int(k[1])
        for i in range (x,x+3,1):
            for j in range (y,y+3,1):
                firstArray.append(boxList[i][j])

    secondAlArray =[]
    for i in range(0, len(firstArray),9):
        secondAlArray.append(firstArray[i:i+9])

    thirdArray = secondAlArray

    for i in range(len(secondAlArray)):
        for j in range(len(secondAlArray[i])):
            if (len(secondAlArray[i][j]))!= 1:
                secondAlArray[i][j]=''
            else:
                secondAlArray[i][j] = secondAlArray[i][j][0]
                    
    solved = True
    for i in secondAlArray:
        for j in i:
            if j == '':
                solved = False

    if solved == False:
        if inputData != secondAlArray:
            firstAlgorithm(secondAlArray, changes)
        else:
            thirdAlgorithm(inputData, finalArray, changes)
    else:
        arrayToDisplay = secondAlArray
        displaySolution(secondAlArray, changes)

def thirdAlgorithm(inputData, finalArray, changes):
    third = True
    result = findCombinations(finalArray, changes)
    thirdAlArray = result["finalArray"]

    lengthArray = []
    lengthArrayTemp = []
    for i in thirdAlArray:
        for j in i:
            lengthArray.append(len(j))
            lengthArrayTemp.append(len(j))
    
    lengthArrayTemp = list(dict.fromkeys(lengthArrayTemp))
    if 1 in lengthArrayTemp:
        lengthArrayTemp.remove(1)
    lengthArrayTemp.sort()
    lengthValue = lengthArrayTemp[0]


    for i in range(len(lengthArray)):
        if lengthValue == lengthArray[i]:
            fillPosition = i
            break

    simpleArray = []
    counter = 0
    for i in thirdAlArray:
        for j in i:
            simpleArray.append(j)

    possibleNumbers = simpleArray[fillPosition]

    if len(possibleNumbers)>1:
        simpleArray[fillPosition] = [simpleArray[fillPosition][0]]
        possibleNumbers.remove(simpleArray[fillPosition][0])
        changes.append([fillPosition, possibleNumbers])


    for i in range(len(simpleArray)):
         if len(simpleArray[i]) != 1:
             simpleArray[i]= ['']

    updatedArray =[]

    for i in simpleArray:
        for j in i:
            updatedArray.append(j)
    
    finalArray = []
    
    for i in range(0, len(updatedArray),9):
        finalArray.append(updatedArray[i:i+9])

    firstAlgorithm(finalArray, changes)
    
def checkSolution(inputData):
    simpleArray = []
    for i in inputData:
        for j in i:
            for k in j:
                simpleArray.append(k)

    counts = []
    counts.append(simpleArray.count("1"))
    counts.append(simpleArray.count("2"))
    counts.append(simpleArray.count("3"))
    counts.append(simpleArray.count("4"))
    counts.append(simpleArray.count("5"))
    counts.append(simpleArray.count("6"))
    counts.append(simpleArray.count("7"))
    counts.append(simpleArray.count("8"))
    counts.append(simpleArray.count("9"))

    solved = True
    for i in counts:
        if i != '9':
            solved  = False

    inputData = [ [ 0 for i in range(9) ] for j in range(9) ]
    for i in range(9):
        for j in range(9):
            currentPos = "square"+str(i)+str(j)
            valueToAdd = globals()[currentPos].get()
            inputData[i][j] = valueToAdd

    tempArray = []
    for i in inputData:
        for j in i:
            tempArray.append(j)

    lastChange=(changes[len(changes)-1])
    lastChangePos = lastChange[0]
    lastChangeNextOption = lastChange[len(lastChange)-1]

    tempArray[lastChangePos] = lastChangeNextOption[0]

    if (len(lastChangeNextOption)) == 1:
        changes.remove(changes[len(changes)-1])
    else:
        changeList = lastChange[1]
        changeList.pop(0)

    finalArray = []
    
    for i in range(0, len(tempArray),9):
        finalArray.append(tempArray[i:i+9])

    if len(changes)>1:
        firstAlgorithm(finalArray, changes)
    else:
        displaySolution(inputData)
    

def displaySolution(arrayToDisplay):
    for rowValue in range(9):
        for columnValue in range(9):
            currentSquare = "square"+str(rowValue)+str(columnValue)
            currentValue = (globals()[currentSquare]).get()
            if len(currentValue) == 0:
                (globals()[currentSquare]).config(foreground = "#8A2BE2")
            (globals()[currentSquare]).delete(0, END)
            (globals()[currentSquare]).insert(0, arrayToDisplay[rowValue][columnValue])
            

            
def createSquaresList():
    value = 0
    squares = []
    for i in range(81):
        squares.append("square"+str(value))
        value = value+1


def addComponents():
    for rowValue in range(9):
        for columnValue in range(9):
            currentSquare = "square"+str(rowValue)+str(columnValue)
            if (rowValue < 3 and columnValue < 3) or (rowValue < 3 and columnValue > 5) or (rowValue > 2 and rowValue < 6 and columnValue > 2 and columnValue < 6) or (rowValue > 5 and columnValue < 3) or (rowValue > 5 and columnValue > 5):
                globals()[currentSquare] = Entry(root,width = 2, justify='center', background="#ebe5f5")
            else:
                globals()[currentSquare] = Entry(root,width = 2, justify='center')
            globals()[currentSquare].grid(row = rowValue, column = columnValue, ipady = 5, ipadx = 5)
            globals()[currentSquare].config(font=("Courier", 25))

    solve=Button(root,text="SOLVE",command=collectData, font=("Courier", 16))
    solve.grid(row=9, column=0, columnspan = 9)
    

createSquaresList()
addComponents()
root.mainloop()

