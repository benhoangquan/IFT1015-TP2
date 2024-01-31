import math
import random
#Variable globale 
MAX_ROW = 0
MAX_COL = 0
nbTotalCase = MAX_ROW * MAX_COL
bombRatio = 0.15
bombLeft = 0

firstClickPos = 0
firstClick = True
finish = False
caseList = []


#_____________Utility function____________
def case(index):
    #return HTML element of a case with id index
    return document.querySelector('#case' + str(index))

def element(id):
    return document.querySelector("#" + id)

def getImg(imgName): 
    #return string contains link to assets image
    webDirectory = "http://codeboot.org/images/minesweeper/"
    nameSuffix = ".png"
    return '<img src="' + webDirectory + imgName + nameSuffix + '">' 

def createHTMLBracket(name, content, attribut = ""): 
    #Exemple of return: <td onclick="something">This is a text<td>
    if len(attribut) > 0: 
        return '<'+ name + " " + attribut + '>'+ content + '</' + name + '>'
    else: 
        return '<' + name + '>' + content + '</' + name + '>'

def getAdjacentCase(caseId): 
    #return list of index of all adjacent cases
    global MAX_COL, MAX_ROW

    #Two utility function to convert between index coordinate and column row coordinate
    def rowCol2Id(row, col): return MAX_COL * row + col
    def id2RowCol(id): return id // MAX_COL, id % MAX_COL

    currentRow, currentCol = id2RowCol(caseId)
    adjList = []
    
    #loop for all adjacent cases
    for rowDelta in [-1, 0, +1]: 
        for colDelta in [-1, 0, +1]: 
            row = currentRow + rowDelta
            col = currentCol + colDelta

            # verify if adjacent cases valid and in the table
            if row in range (0, MAX_ROW)\
                and col in range (0, MAX_COL)\
                and (row != currentRow or col != currentCol) : 
                #^avoid the case itself^
                adjCaseId = rowCol2Id(row, col)
                adjList.append(adjCaseId)

    return adjList 

def testGetAdjacentCaseAndTestPropagate(): 
    global MAX_COL, MAX_ROW
    MAX_ROW = 4
    MAX_COL = 4
    inputArr = [1,1,1,0,\
         2,"B",2,0,\
         2,"B",2,0,\
         1,1,1,0]
    
    assert (getAdjacentCase(5)) == [0, 1, 2, 4, 6, 8, 9, 10]
    assert (getAdjacentCase(0)) == [1, 4, 5]
    assert (getAdjacentCase(1)) == [0, 2, 4, 5, 6]

    def propagate(gameArr, clicPos):
        #Simplify version of propagate algorithm in clic()
        listOfIndex = []
        listOfIndex.append(clicPos)    
        for elem in listOfIndex: 
            if gameArr[elem] == 0: 
                for case in getAdjacentCase(elem):
                    if case not in listOfIndex:
                        listOfIndex.append(case)
            else:
                pass
        return listOfIndex
    
    assert propagate(inputArr, 3) == [3, 2, 6, 7, 10, 11, 14, 15]
    assert propagate(inputArr, 7) == [7, 2, 3, 6, 10, 11, 14, 15]
    assert propagate(inputArr, 0) == [0]    

#_____________Init-related function____________   

def initHTMLCases(): 
    #create
    global nbTotalCase

    def createHTML4Case(caseId): 
        contenu = getImg("blank")
        attribut = 'id="case_" onclick="click(_, event)"'
        attribut = attribut.replace("_", str(caseId))
        return createHTMLBracket("td", contenu, attribut)

    def trJoin(lst): 
        return createHTMLBracket("tr", ''.join(lst))
    def tableJoin(lst): 
        return createHTMLBracket("table", ''.join(lst))
    def grouper(lst, taille):  
        groupes = []
        accum = []
        for elem in lst:
            accum.append(elem)
            if len(accum) == taille:
                groupes.append(accum)
                accum = []
        if len(accum) > 0:
            groupes.append(accum)
        return groupes
    def listeToTable(lst, taille):
        return tableJoin(list(map(trJoin, grouper(lst, taille))))
    lstTuile = list(map(createHTML4Case, list(range(nbTotalCase))))

    return listeToTable(lstTuile, MAX_COL)

def testInitHTMLCase():
    global nbTotalCase, MAX_COL, MAX_ROW
    nbTotalCase = 4; MAX_ROW = 2; MAX_COL = 2
    
    testAns = """
    <table><tr><td id="case0" onclick="click(0, event)"><img src="http://codeboot.org/images/minesweeper/blank.png"></td><td id="case1" onclick="click(1, event)"><img src="http://codeboot.org/images/minesweeper/blank.png"></td></tr><tr><td id="case2" onclick="click(2, event)"><img src="http://codeboot.org/images/minesweeper/blank.png"></td><td id="case3" onclick="click(3, event)"><img src="http://codeboot.org/images/minesweeper/blank.png"></td></tr></table
    """
    assert (initHTMLCases()) == testAns
    
def initCaseList(): 
    global nbTotalCase, caseList
    caseList = []
    for i in range(nbTotalCase): 
        caseList.append(struct(isBomb = False, bombSurround = 0,\
                               isFlagged = False, isUnveiled = False))

def testInitCaseList(): 
    global nbTotalCase, caseList   
    nbTotalCase = 10
    initCaseList()
    assert(len(caseList) == nbTotalCase)
    
    for i in range(nbTotalCase): 
        assert caseList[i] == struct(isBomb = False, bombSurround = 0,\
                                    isFlagged = False, isUnveiled = False)
        
def initBomb(): 
    global nbTotalCase, firstClickPos, bombRatio, caseList

    def fisherYateShuffle(lst):
        n = len(lst)
        for i in range(0, n - 2):
            j = int(random.random()*100 % (n-i) + i)
            temp = lst[i]; lst[i] = lst[j]; lst[j] = temp
        return lst

    def getBombSurround(caseId):
        adjCaseIdList = getAdjacentCase(caseId)
        bombCounter = 0 
        for elm in adjCaseIdList: 
            if caseList[elm].isBomb: 
                bombCounter += 1
        return bombCounter      
    
    #swap user-clicked case with an empty case if the former is a bomb
    def swapFirstClick():
        if caseList[firstClickPos].isBomb: 
            emptyCase = struct(isBomb=False, bombSurround=0, \
                               isFlagged=False, isUnveiled=False)
            emptyCaseId = caseList.index(emptyCase)
            
            temp = caseList[firstClickPos]
            caseList[firstClickPos] = caseList[emptyCaseId]
            caseList[emptyCaseId] = temp
    
    nbBomb = math.floor(nbTotalCase * bombRatio)
    for i in range(nbBomb): 
        caseList[i].isBomb = True
    caseList = fisherYateShuffle(caseList)
    swapFirstClick()
    
    #update caseList with bombSurround each case for 
    for i in range(nbTotalCase): 
        caseList[i].bombSurround = getBombSurround(i)

def testInitBomb(): 
    global nbTotalCase, firstClickPos, bombRatio, caseList
    nbTotalCase = 100
    bombRatio = 0.5
    
    initCaseList()
    initBomb()
    randomId = int(random.random()*100)
    caseList[randomId].isFlagged = True
    caseList[randomId].isUnveiled = True
    
    bombCounter = 0
    flagCounter = 0 
    unveilCounter = 0
    listSize = len(caseList) - 1
    while listSize >= 0 : 
        if caseList[listSize].isBomb: 
            bombCounter += 1
        elif caseList[listSize].isFlagged: 
            flagCounter += 1
        elif caseList[listSize].isUnveiled: 
            unveilCounter += 1
        listSize -= 1
        
            
    assert bombCounter == 50
    assert flagCounter == 1
    assert unveilCounter == 1
        
def init(largeur, hauteur):
    global nbTotalCase, MAX_COL, MAX_ROW, finish, firstClick, firstClickPos, bombLeft
    MAX_ROW = hauteur; MAX_COL = largeur; nbTotalCase = largeur * hauteur
    finish = False; firstClick = True; firstClickPos = 0
    
    main = document.querySelector('#main')
    main.innerHTML = """
      <style>
      #main table {
        border: 1px solid black;
        margin: 10px;
      }
      #main table td {
        width: 30px;
        height: 30px;
        border: none;
      }
      .msgBomb {
        display: inline-block; 
      }
      
      </style>
      <link rel="preload" href="http://codeboot.org/images/minesweeper/0.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/1.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/2.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/3.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/4.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/5.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/6.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/7.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/8.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/blank.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/flag.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/mine.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/mine-red.png">
      <link rel="preload" href="http://codeboot.org/images/minesweeper/mine-red-x.png">
      

     """
    bombLeft = math.floor(nbTotalCase * bombRatio)
    msgBomb = createHTMLBracket("h3", "Bomb left:", 'id="text" class="msgBomb"')\
    + createHTMLBracket("h3", str(bombLeft), 'id="bombLeft" class="msgBomb"')
    main.innerHTML+= msgBomb
    main.innerHTML+= createHTMLBracket("button", "restart", 'class="msgBomb" onclick="init(' + str(MAX_COL) + "," + str(MAX_ROW) + ')"')
    main.innerHTML+= initHTMLCases()
    initCaseList()

#_______________Clic-related function_____________
def click(id, event): 
    global caseList, nbTotalCase, firstClick, firstClickPos, finish, bombLeft
    
    def plantOrUnplantFlag(caseId):
        #Plant or unplant flag and update counter
        global bombLeft
        if not caseList[caseId].isUnveiled: 
            isCurrentlyFlagged = caseList[caseId].isFlagged
            if not isCurrentlyFlagged:
                caseList[caseId].isFlagged = True 
                case(caseId).innerHTML = getImg("flag")
                bombLeft -= 1 if bombLeft > 0 else 0
            else: 
                caseList[caseId].isFlagged = False
                case(caseId).innerHTML = getImg("blank")
                bombLeft += 1
                
        element("bombLeft").innerHTML = str(bombLeft)
                
    def unveiledChangeImg(caseId):
        #unveiled the image (front-end) using the data from caseList
        thisCase = caseList[caseId]
        strImg = ""
        if thisCase.isBomb:
            if thisCase.isFlagged:
                strImg = "flag"
            else:
                if thisCase.isUnveiled: 
                    strImg = "mine-red"
                else: 
                    strImg = "mine"
        else:
            if thisCase.isFlagged:
                strImg = "mine-red-x"
            else:
                strImg = str(thisCase.bombSurround)
        case(caseId).innerHTML = getImg(strImg)

    def unveiled(caseId):
        #unveiled change the state isUnveiled in caseList (back-end)
        #and change the image (front-end)
        if not caseList[caseId].isUnveiled and not caseList[caseId].isFlagged:
            caseList[caseId].isUnveiled = True
            unveiledChangeImg(caseId)
    
    def unveiledBombs(): 
        #unveil all bombs at the end
        for i in range(len(caseList)):
            case = caseList[i]
            if case.isBomb or case.isFlagged: 
                unveiledChangeImg(i)
                #unveiled was not used bcz it would changed case.isUnveiled; 
                #it would cause a false negative for checkFinish function
    
    def propagate(caseId):
        #breadth-first search algorithm
        #return list of case to be unveiled when user click on a cases with 0 bomb surrounds
        listOfIndex = []
        #check if the initial case has 0 bomb surround
        if caseList[caseId].bombSurround == 0 and caseList[caseId].isBomb == False: 
            listOfIndex.append(caseId)
        
        for elem in listOfIndex: 
            #if the case has 0 bomb surround, update list with all adjacent cases,
            #until all cases with 0 bomb surround checked
            #elif the case has n bomb, do nothing
            if caseList[elem].bombSurround == 0 and caseList[caseId].isBomb == False: 
                for case in getAdjacentCase(elem):
                    if case not in listOfIndex:
                        listOfIndex.append(case)
            else:
                pass

        return listOfIndex
    
    def checkFinish(caseId): 
        #return the ending and the verdict of the game
        winVerdict = False; finish = False
        thisCase = caseList[caseId]
        if thisCase.isBomb and thisCase.isUnveiled:
            winVerdict = False
            finish = True
            return finish, winVerdict #finish, lose bcz bomb clicked
        
        for case in caseList: 
            if not case.isBomb and not case.isUnveiled: 
                winVerdict = False
                finish = False
                return finish, winVerdict #act like break, if 1 case still not unveiled, then not finish 
        
        #finish, win bcz it passed through 2 above situations 
        finish = True if bombLeft == 0 else False
        winVerdict = True 
        return finish, winVerdict
    
    def endingScreen(verdict): 
        #display msg depending the result of the game
        if verdict:
            alert("""You successfully avoided all bombs
                    ◦°˚\(*❛‿❛)/˚°◦
                  """) 
        else:
            alert("""You clicked on a bomb
                            _ ._  _ , _ ._
                            (_ ' ( `  )_  .__)
                        ( (  (    )   `)  ) _)
                        (__ (_   (_ . _) _) ,__)
                            `~~`\ ' . /`~~`
                                ;   ;
                                /   \
                    _____________/_ __ \_____________
                """)
            unveiledBombs()
    
    #_______________End of local function_________________
    # Work diagram of click(id,event):
    #1. initBomb after firstclick
    #2. plant/unplant flag/unveiled case depend on user actions
    #3. check if win
    if firstClick: 
        firstClick = False
        firstClickPos = id
        initBomb()
        
    if event.shiftKey and not finish: 
        plantOrUnplantFlag(id)
    elif not finish:
        unveiled(id)
        listToUnveiled = propagate(id)
        for elm in listToUnveiled: 
            unveiled(elm)   
            
    finish, winVerdict = checkFinish(id)
    if finish: 
        endingScreen(winVerdict)
