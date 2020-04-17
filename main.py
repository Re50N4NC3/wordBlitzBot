import pyautogui
import time
import pickle
import codecs


# remove duplicates from array
def remove_dup(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


grid = [x for x in range(16)]  # initialize main board grid
path = [[[] for i in range(16)] for j in range(16)]  # possible paths from [cell] of [length]
done = [0 for x in range(10)]  # initialize done paths for specific lengths
doneFound = []  # initialize found paths array for longer words
read = []  # array to read pickled paths
board = []  # letters on board

board = "jćocobmkanlńnzał"
print(len(board))
print(board)

# create list for longer words (needed only one time, to create dictionaries)
longList = False
saveLen = 7  # length of saved words

if longList is True:
    slowaLong = []
    # open file and read the content in a list
    with open('slowa.txt', 'r') as filehandle:
        filecontents = filehandle.readlines()

        for line in filecontents:
            if len(line[:-1].encode('utf-8')) == saveLen:
                curLine = line[:-1]
                slowaLong.append(curLine)  # add item to the list

    # save the words in a file
    with open('slowa' + str(saveLen) + '.txt', 'w') as filehandle:
        filehandle.writelines("%s\n" % i for i in slowaLong)

# unpickle all possible moves
for i in [2, 3, 4, 5, 6]:
    name = 'list' + str(i) + '.txt'

    with open (name, 'rb') as read:
        done[i] = pickle.load(read)

# find long words on the board
done[8] = done[3]  # allows to bruteforce anyways in the end
words = {}  # words read from list
guess = ""  # guessed word by path (temporary)
avP = []  # temporary path
doneTemp = []  # temporary done paths array
remove = set(remove_dup(board))  # remove duplicate letters from the board list

# find words of specific length containing letters from board
for lngth in [3, 4, 5, 6]:
    with open('slowa' + str(lngth) + '.txt', 'r') as filehandle:  # load file with all words of length "lngth"
        wordsAll = filehandle.readlines()

    print("Started removing...")
    # remove impossible words
    words = [x for x in wordsAll
         if remove & set(str(x))]
    print("Removed unnecessary words.")

    for i in range(0, len(done[lngth])):  # loop through bruteforce instructions to find words
        if done[lngth][i] != ";":  # found instruction
            guess += str(board[done[lngth][i]])
            avP.append(done[lngth][i])
        else:
            if guess + "\n" in words:
                avP.append(";")
                doneTemp += avP

                percentDone = int((i/len(done[lngth]))*100)
                print("Percent done of the %s length: %s %%" %(lngth, percentDone))
            # reset temporary containers
            guess = ""
            avP = []
    print("Done with words of %s length..." %(lngth))
    done[lngth] = doneTemp
    words = {}  # words read from list
    guess = ""  # guessed word by path
    avP = []  # temporary path
    doneTemp = []  # temporary done paths array

# mouse execution switch False / True
ini = True
if ini is True:
    time.sleep(1)  # wait for set up (debug)
    pyautogui.PAUSE = 0.0143  # fastest possible time between mouse moves
    click = False  # click boolean

    # execute clicks
    for lngth in [6, 5, 4, 3, 2, 8]:  # order is from longest dictionary words, to shortest, then bruteforcing starts
        click = False
        for i in range(0, len(done[lngth])):
            if done[lngth][i] != ";":  # found instruction
                rw = int(done[lngth][i] % 4)
                cl = int(done[lngth][i] / 4)
                pyautogui.moveTo(364+rw*70, 380+cl*70)

                if click is False:  # mouse button down
                    pyautogui.mouseDown(button='left')
                    click = True

            else:  # mouse button up
                pyautogui.mouseUp(button='left')
                click = False
