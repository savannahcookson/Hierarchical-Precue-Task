#!/usr/bin/env python
from psychopy import gui, core, event, logging
#Turns off annoying warnings literally every trial
logging.console.setLevel(logging.CRITICAL)
from time import strftime
import random
import numpy
import linecache
from collections import defaultdict
from operator import itemgetter, sub
import os, sys

###########
#Constants#
###########

DEBUG = False

# BEWARE: changing this also requires a manual update to the EXPECTED_KEY_MAPPING constant
NUM_GROUPS = 8
NUM_SESSIONS = 2

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

SHOW_SCREEN = 1

# in seconds
MAX_STIMULI_WAIT_TIME = 1.9

SHAPE_SIZE = 70
TEXT_WIDTH = round(0.8 * WINDOW_WIDTH)

# TODO: fix these ranges; seem to be flipped
WARM_COLOR_RANGE = [0, 75]
COOL_COLOR_RANGE = [180, 255]

NUM_RESPONSE_PRACTICES = 1
NUM_PAIR_CUE_PRACTICES = 1

NUM_TIME = 246
NUM_COLOR_PRACTICES = 4
NUM_CONVEXITY_PRACTICES = 4
NUM_VERTICAL_HEMIFIELD_PRACTICES = 4
NUM_HORIZONTAL_LOCATION_PRACTICES = 4
NUM_PAIR_PRACTICES = 4
NUMBER_OF_BLOCKS = 12


# definitions of the dimensions and cues. we use the length of these to determine how many trials to run, but currently do not
# have an advanced setup to make it "automatically work" if you just add a new dimension here
# BEWARE: changing this requires manual ly updating the EXPECTED_KEY_MAPPINGS constant
DIMENSIONS = {0: 'isInside', 1: 'isWarm', 2: 'isConvex', 3: 'isAbove'}
CUES = {
    '2O': 'both',
    '2S': 'both',
    '1H': 'hand',
    '1J': 'judgment',
    '0O': 'none',
    '0S': 'none'}
HAND = {'L': 'LEFT', 'R': 'RIGHT'}
TRIALTYPES = ['0OL', '0OR', '0SL', '0SR', '1HOL', '1HOR', '1HSL', '1HSR', '1JOL', '1JOR', '1JSL', '1JSR', '2OL', '2OR', '2SL', '2SR']
JITTER = [.25, .5, .75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4]

# this is hardcoded as we are not doing a standard combination or permutation across all options.
# 3D array of group_number[dimension[choice(true or false)]] => expected key
# translated from mappings.txt in project folder
GROUP_TRIALTYPE_TO_DIMENSION = {
    '1': {'OL': 1, 'OR': 2, 'SL': 3, 'SR': 0},
    '2': {'OL': 2, 'OR': 1, 'SL': 0, 'SR': 3},
    '3': {'OL': 1, 'OR': 2, 'SL': 0, 'SR': 3},
    '4': {'OL': 2, 'OR': 1, 'SL': 3, 'SR': 0},
    '5': {'OL': 1, 'OR': 2, 'SL': 3, 'SR': 0},
    '6': {'OL': 2, 'OR': 1, 'SL': 0, 'SR': 3},
    '7': {'OL': 1, 'OR': 2, 'SL': 0, 'SR': 3},
    '8': {'OL': 2, 'OR': 1, 'SL': 3, 'SR': 0},
    }

EXPECTED_KEY_MAPPING = {
    '1': {0: {True: '9', False: '8'}, 1: {True: '3', False: '4'}, 2: {True: '9', False: '8'}, 3: {True: '3', False: '4'}},
    '2': {0: {True: '4', False: '3'}, 1: {True: '8', False: '9'}, 2: {True: '4', False: '3'}, 3: {True: '8', False: '9'}},
    '3': {0: {True: '4', False: '3'}, 1: {True: '3', False: '4'}, 2: {True: '9', False: '8'}, 3: {True: '8', False: '9'}},
    '4': {0: {True: '9', False: '8'}, 1: {True: '8', False: '9'}, 2: {True: '4', False: '3'}, 3: {True: '3', False: '4'}},
    '5': {0: {True: '8', False: '9'}, 1: {True: '4', False: '3'}, 2: {True: '8', False: '9'}, 3: {True: '4', False: '3'}},
    '6': {0: {True: '3', False: '4'}, 1: {True: '9', False: '8'}, 2: {True: '3', False: '4'}, 3: {True: '9', False: '8'}},
    '7': {0: {True: '3', False: '4'}, 1: {True: '4', False: '3'}, 2: {True: '8', False: '9'}, 3: {True: '9', False: '8'}},
    '8': {0: {True: '8', False: '9'}, 1: {True: '9', False: '8'}, 2: {True: '3', False: '4'}, 3: {True: '4', False: '3'}},
}

KEY_TO_FINGER = {
    '3': 'MIDDLE',
    '4': 'INDEX',
    '9': 'INDEX',
    '8': 'MIDDLE'
}

KEY_TO_HAND = {
    '3': 'LEFT',
    '4': 'LEFT',
    '9': 'RIGHT',
    '8': 'RIGHT'
}

INDEX_TO_TRIALTYPE = {
    0: '0OL',
    1: '0OL',
    2: '0OR',
    3: '0OR',
    4: '0SL',
    5: '0SL',
    6: '0SR',
    7: '0SR',
    8: '1HOL',
    9: '1HOL',
    10: '1HOR',
    11: '1HOR',
    12: '1HSL',
    13: '1HSL',
    14: '1HSR',
    15: '1HSR',
    16: '1JOL',
    17: '1JOL',
    18: '1JOR',
    19: '1JOR',
    20: '1JSL',
    21: '1JSL',
    22: '1JSR',
    23: '1JSR',
    24: '2OL',
    25: '2OL',
    26: '2OR',
    27: '2OR',
    28: '2SL',
    29: '2SL',
    30: '2SR',
    31: '2SR'

}

# is set in experimentSetup, which should be called first
PARTICIPANT_DATA = None

# we are going to dynamically record the framerate and use it for super accurate timing of our stimuli => reponse
FRAME_RATE = None

GLOBAL_CLOCK = core.MonotonicClock()

#################
#Setup Functions#
#################

# Prompts for subject input
def experimentSetup():
    dialogInfo = {'Participant Number': '', 'Group': range(1, NUM_GROUPS + 1), 'Session': range(1, NUM_SESSIONS+1)}
    dialog = gui.DlgFromDict(dictionary = dialogInfo, title = 'RCDV Cuing')
    if dialog.OK and dialogInfo['Participant Number'] != '':
        # TODO (craig) there has got to be a better way to update this global. works perfectly fine for now
        globals()['PARTICIPANT_DATA'] = {'time': strftime("%Y-%m-%d  %H:%M:%S"),
            'subject': dialogInfo['Participant Number'], 'group': dialogInfo['Group'], 'session': dialogInfo['Session']}

def fileSetup():
    participantFile = 'behavioralResults/RCDV_{}_{}.csv'.format(PARTICIPANT_DATA['subject'], PARTICIPANT_DATA['session'])
    fh = open(participantFile, 'a')
    fh.write('Participant,Session,Group,Time,BlockName,BlockNum,Trial,Dim,CSI,ITI,Acc,RT,eyeMvt,Expected,Actual,Stim1IsInside,Stim1IsWarm,Stim1IsConvex,'\
        'Stim1IsAbove,Stim2IsInside,Stim2IsWarm,Stim2IsConvex,Stim2IsAbove,StimCue,RespCue,TrialType\n')
    return fh

def timingSetup(line):
    cueTimes = []
    stimTimes = []

    for trialtype in TRIALTYPES:
        cueFilename = 's' + getSubNum() + '/s' + getSession() + '/' + trialtype + '_C.1D'
        stimFilename = 's' + getSubNum() + '/s' + getSession() + '/' + trialtype + '_S.1D'

        #if DEBUG:
            #print cueFilename, stimFilename

        cueLine = linecache.getline(cueFilename, line)
        cueTimes=cueTimes + map(float, cueLine.split())
        linecache.clearcache()
        stimLine = linecache.getline(stimFilename, line)
        stimTimes = stimTimes + map(float, stimLine.split())
        linecache.clearcache()

    indices = [i[0] for i in sorted(enumerate(cueTimes), key=itemgetter(1))]
    cueTimes = sorted(cueTimes)
    stimTimes = sorted(stimTimes)

    return(cueTimes, stimTimes, indices)

# Sets up visual window and GUI for experiment
def windowSetup():
    win = visual.Window(size=(WINDOW_WIDTH, WINDOW_HEIGHT), color="black", units='pix', allowGUI='False', winType='pyglet', screen=SHOW_SCREEN)
    event.Mouse(visible=False)
    globals()['FRAME_RATE'] = win.getActualFrameRate()
    if DEBUG:
        print 'FRAME_RATE: ', FRAME_RATE

    visual.TextStim(
                    win, text='Welcome! In this experiment, you will see a series of cues and stimulus pairs on screen and make button presses based on judgments of those '\
                    'stimulus pairs. If at any point you want to end your participation, just let the experimenter know.  We will first go over the task in more detail.',
                    height=30, color='white', pos=[0,100], wrapWidth = TEXT_WIDTH
                    ).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)
    return win

#####################
#Getters and Setters#
#####################
def getAnswer(answerTracker, trial, indices):
    currIndex = indices[trial]
    currCond = TRIALTYPES.index(INDEX_TO_TRIALTYPE[currIndex])

    if answerTracker[currCond] == -1:
        answerTracker[currCond] = bool(random.getrandbits(1))
    else:
        answerTracker[currCond] = not answerTracker[currCond]

    return answerTracker, answerTracker[currCond]

def getCueType(condition):
    return CUES[condition]

def getDimType(condition):
    return GROUP_TRIALTYPE_TO_DIMENSION[getGroup()][condition]

def getHandType(condition):
    return HAND[condition]

def getExpectedFinger(dimension,answer):
    return KEY_TO_FINGER[getExpectedKey(dimension, answer)]

def getExpectedHand(dimension):
    return KEY_TO_HAND[getExpectedKey(dimension, True)]

def getExpectedKey(dimension, answer):
    return EXPECTED_KEY_MAPPING[getGroup()][dimension][answer]

def getExpectedKeyString(dimension, answer):
    return '{} {}'.format(getExpectedHand(dimension), KEY_TO_FINGER[getExpectedKey(dimension, answer)])

def getFixationVisual(win):
    return [visual.TextStim(win, text = u"\u00B7", height = 80, color='white', pos = [0,0]),
        visual.TextStim(win, text = u"\u00B7", height = 40, color='white', pos = [-1*(WINDOW_WIDTH/4)+(SHAPE_SIZE/4),-1*(WINDOW_HEIGHT/4)+(SHAPE_SIZE/4)]),
        visual.TextStim(win, text = u"\u00B7", height = 40, color='white', pos = [(WINDOW_WIDTH/4)-(SHAPE_SIZE/4),(WINDOW_HEIGHT/4)-(SHAPE_SIZE/4)]),
        visual.TextStim(win, text = u"\u00B7", height = 40, color='white', pos = [-1*(WINDOW_WIDTH/4)+(SHAPE_SIZE/4),(WINDOW_HEIGHT/4)-(SHAPE_SIZE/4)]),
        visual.TextStim(win, text = u"\u00B7", height = 40, color='white', pos = [(WINDOW_WIDTH/4)-(SHAPE_SIZE/4),-1*(WINDOW_HEIGHT/4)+(SHAPE_SIZE/4)])]

def getGroup():
    return PARTICIPANT_DATA['group']

def getHorizontalLoc(isInside=None, isLeft=None):
    if isInside is None:
        isInside = bool(random.getrandbits(1))
    if isLeft is None:
        isLeft = bool(random.getrandbits(1))
    if isInside and isLeft:
        return random.randint(round(-1*WINDOW_WIDTH/4.0 + SHAPE_SIZE*(5/4)), round(-1 * (SHAPE_SIZE/2)))
    if isInside and not isLeft:
        return random.randint(round(SHAPE_SIZE/2), round((1*WINDOW_WIDTH/4.0) - SHAPE_SIZE*(5/4)))
    if not isInside and isLeft:
        return random.randint(round((-1*WINDOW_WIDTH/2.0) + ((3/2) * SHAPE_SIZE)), round((-1*WINDOW_WIDTH/4.0)-SHAPE_SIZE*(1/4)))
    return random.randint(round((WINDOW_WIDTH/4.0)+SHAPE_SIZE*(1/4)), round((1*WINDOW_WIDTH/2.0) - ((3/2) * SHAPE_SIZE)))

def getJitterVector(numberOfRounds):
    vector = []
    for i in range(0,numberOfRounds):
        vector = vector + JITTER
    random.shuffle(vector)
    return vector

def getNameForKey(key):
    return '{} {}'.format(KEY_TO_HAND[key], KEY_TO_FINGER[key])

# TODO (savannah) in testing, this appears to be busted. it seems to work during the color practice phase, but not during
# the pair practice (it's backwards). i believe it is because of how Rect vs. ImageStim is utilizing the color
# (perhaps dkl is not enabled for one) needs investigation
def getRandomColor(isWarm=None):
    if isWarm is None:
        isWarm = bool(random.getrandbits(1))
    if isWarm:
        return (0, random.randint(WARM_COLOR_RANGE[0], WARM_COLOR_RANGE[1]), 1)
    return (0, random.randint(COOL_COLOR_RANGE[0], COOL_COLOR_RANGE[1]), 1)

def getRandomShapeFilename(isConvex=None):
    if isConvex is None:
        isConvex = bool(random.getrandbits(1))
    if isConvex:
        return 'images/convex_%d.png' % random.randint(25,75)
    return 'images/concave_%d.png' % random.randint(-75,-25)

def getRTVector(rtRawVector, accuracyVector):
    rtVector = []
    for i in range(0,len(accuracyVector)-1):
        if accuracyVector[i] == 1:
            rtVector.append(rtRawVector[i])
    return rtVector

def getSession():
    return PARTICIPANT_DATA['session']

def getSubNum():
    return PARTICIPANT_DATA['subject']

#DIMENSIONS = {0: 'isInside', 1: 'isWarm', 2: 'isConvex', 3: 'isAbove'}
def getStimulus(isInside=None, isWarm=None, isConvex=None, isAbove=None, x=None, y=None, isLeft=None):
    if isInside is None:
        isInside = bool(random.getrandbits(1))
    if isWarm is None:
        isWarm = bool(random.getrandbits(1))
    if isConvex is None:
        isConvex = bool(random.getrandbits(1))
    if isAbove is None:
        isAbove = bool(random.getrandbits(1))
    for v in getFixationVisual(win):
        v.draw()
    return [visual.GratingStim(
                        win,
                        pos=(x if x is not None else getHorizontalLoc(isInside=isInside, isLeft=isLeft), y if y is not None else getVerticalHemi(isAbove)),
                        size=(SHAPE_SIZE, SHAPE_SIZE),
                        sf=0.0,
                        mask=getRandomShapeFilename(isConvex),
                        colorSpace='dkl',
                        color=getRandomColor(isWarm)),
                        isInside, isWarm, isConvex, isAbove]

def getTrialType(index):
    return INDEX_TO_TRIALTYPE[index]

def getVerticalHemi(isAbove=None):
    if isAbove is None:
        isAbove = bool(random.getrandbits(1))
    if isAbove:
        return random.randint((SHAPE_SIZE/4), round(WINDOW_HEIGHT/2.0) - ((3/2) * SHAPE_SIZE))
    return random.randint(round(-1*WINDOW_HEIGHT/2.0) + ((3/2) * SHAPE_SIZE),-1*(SHAPE_SIZE/4))

##################
#Helper Functions#
##################

# our own wait function that utilizes frame count and actual framerate for uber accurate timing vs. using core.wait. downside is that we need to pass in
# references to reach of the visuals that we want to be redrawn on each frame
# returns tuple of a list of keysPressed and the total EXACT elapsed time the visuals were displayed (regardless of whether it was cut short by a keypress)
def cleanShutdown(win, fh):
    drawAndWait(win, 1, getFixationVisual(win))
    fh.close()
    core.quit()

def drawAndWait(win, seconds, visuals=[]):
    framesToWait = int(numpy.ceil(seconds * FRAME_RATE))
    #if DEBUG:
        #print 'Waiting: ', framesToWait, ' frames'
    keyPresses = []
    clock = core.Clock()
    performBorder(win)
    for i in range(0, framesToWait):
        frameKey = event.getKeys(keyList=['3', '4', '8', '9', 'space', 'm'], timeStamped = clock)
        if frameKey != []:
            keyPresses.append(frameKey[0])
            #if DEBUG:
                #print keyPresses[0]
        for v in visuals:
            v.draw()
        performBorder(win)
        win.flip()
    return [keyPresses, framesToWait/FRAME_RATE]

def evaluateEyeMvt(eyeMvtKey):
    trialEyeMvt = 0
    if eyeMvtKey == []:
        return trialEyeMvt
    if 'm' == eyeMvtKey[0][0]:
        trialEyeMvt = 1
    return trialEyeMvt

def evaluateResponse(pressedKeys, dim, answer, iti, win, keyName=None, feedbackOff=False):
    #if DEBUG:
        #print 'Expected Key: ', expectedKey
        #print 'Received Key: ', pressedKeys
        #print 'Elapsed time: ', elapsedTime
    response = [visual.TextStim(win,text='Success!', height=30, color='white',pos=[0,0], wrapWidth = TEXT_WIDTH)]
    accuracy = 1
    key = pressedKeys[0][0] if pressedKeys else None

    if 'space' == key:
        cleanShutdown(win,fh)
    elif keyName is None:
        expectedKey = getExpectedKey(dim, answer)
        if key is None:
            response = [visual.TextStim(win,text='Sorry, you took too long to respond. You should have pressed your {} finger '\
                'on your {} hand.'.format(getExpectedFinger(dim, answer), getExpectedHand(dim)), height=30, color='white',pos=[0,0], wrapWidth = TEXT_WIDTH)]
            accuracy = 0
        elif expectedKey != key:
            response = [visual.TextStim(win,text='Sorry, that was not correct. You should have pressed your {} finger '\
                'on your {} hand'.format(getExpectedFinger(dim, answer), getExpectedHand(dim)), height=30, color='white',pos=[0,0], wrapWidth = TEXT_WIDTH)]
            accuracy = 0
    else:
        if key is None:
            response = [visual.TextStim(win,text='Sorry, you took too long to respond. You should have pressed your {} finger '\
                'on your {} hand.'.format(KEY_TO_FINGER[keyName], KEY_TO_HAND[keyName]), height=30, color='white',pos=[0,0], wrapWidth = TEXT_WIDTH)]
            accuracy = 0
        elif keyName != key:
            response = [visual.TextStim(win,text='Sorry, that was not correct. You should have pressed your {} finger '\
                'on your {} hand'.format(KEY_TO_FINGER[keyName], KEY_TO_HAND[keyName]), height=30, color='white',pos=[0,0], wrapWidth = TEXT_WIDTH)]
            accuracy = 0
    if feedbackOff:
        response = getFixationVisual(win)
    [eyeMvtKey, elapsedTime] = drawAndWait(win, iti, response)

    #drawAndWait(win, JITTER[random.randInt(0,4)], [getFixationVisual(win)])
    if keyName is None:
        return [accuracy, eyeMvtKey, expectedKey]
    else:
        return [accuracy, eyeMvtKey]

#DIMENSIONS = {0: 'isInside', 1: 'isWarm', 2: 'isConvex', 3: 'isAbove'}
def fullTrialDraw(win, csi, iti, dim, answer, cueChoice=None, lockedInside=None, lockedWarm=None, lockedConvex=None, lockedAbove=None, feedbackOff = False):
    [judgmentCue, handCue] = performCue(win, dim, csi, cueChoice, lockedInside, lockedWarm, lockedConvex, lockedAbove)

    v1 = getStimulus(isInside=lockedInside, isWarm=lockedWarm, isConvex=lockedConvex, isAbove=lockedAbove, isLeft=True)
    v2 = getStimulus(
                      isInside=lockedInside if lockedInside is not None else not v1[1],
                      isWarm=lockedWarm if lockedWarm is not None else not v1[2],
                      isConvex=lockedConvex if lockedConvex is not None else not v1[3],
                      isAbove=lockedAbove if lockedAbove is not None else not v1[4],
                      isLeft=False
                      )
    [keysPressed, elapsedTime] = drawAndWait(
        win,
        1.9,
        [v1[0], v2[0],] + getFixationVisual(win)
    )
    #if DEBUG:
        #print 'Dimension: ', DIMENSIONS[dim]
        #print 'Answer: ', answer
        #print 'Expected Key: ', getExpectedKey(dim, answer)
    [trialAccuracy, eyeMvtKey, keys] = evaluateResponse(keysPressed, dim, answer, iti, win, feedbackOff=feedbackOff)
    trialRT = None
    trialResponse = None
    trialEyeMvt = evaluateEyeMvt(eyeMvtKey)
    if keysPressed != []:
        trialRT = keysPressed[0][1]
        trialResponse = keysPressed[0][0]
    return [trialAccuracy, trialRT, trialResponse, trialEyeMvt, elapsedTime, v1, v2, judgmentCue, handCue]


#DIMENSIONS = {0: 'isInside', 1: 'isWarm', 2: 'isConvex', 3: 'isAbove'}
def performBorder(win):
    #visual.Rect(win, width=WINDOW_WIDTH, height=SHAPE_SIZE/2, pos=[0,(WINDOW_HEIGHT/2-SHAPE_SIZE/4)], fillColor="dimGrey", lineColor=None).draw() #pos=(0,(WINDOW_HEIGHT-SHAPE_SIZE))
    visual.Rect(win, width=SHAPE_SIZE/2, height=WINDOW_HEIGHT, pos=[(WINDOW_WIDTH/2-(SHAPE_SIZE/4)),0], fillColor="dimGrey", lineColor=None).draw() # pos=((WINDOW_WIDTH-SHAPE_SIZE),0)
    #visual.Rect(win, width=WINDOW_WIDTH, height=SHAPE_SIZE/2, pos=[0,-1*(WINDOW_HEIGHT/2-SHAPE_SIZE/4)], fillColor="dimGrey", lineColor=None).draw() #, pos=(0,(-1*(WINDOW_HEIGHT-SHAPE_SIZE))
    visual.Rect(win, width=SHAPE_SIZE/2, height=WINDOW_HEIGHT, pos=[-1*(WINDOW_WIDTH/2-(SHAPE_SIZE/4)),0], fillColor="dimGrey", lineColor=None).draw() #, pos=((-1*(WINDOW_WIDTH-SHAPE_SIZE)),0)
    return

def performCue(win, dim, csi, cueChoice, lockedInside=None, lockedWarm=None, lockedConvex=None, lockedAbove=None):
    if cueChoice == None:
        judgmentCue = handCue = csi = None
        return [judgmentCue, handCue]

    judgmentCue = 'XXXXX'
    handCue = 'XXXXX'
    if cueChoice == 'both' or cueChoice == 'judgment':
        if lockedWarm is not None or lockedConvex is not None:
            judgmentCue = 'OBJECT'
        else:
            judgmentCue = 'SPATIAL'
    if cueChoice == 'both' or cueChoice == 'hand':
        handCue = getExpectedHand(dim)

    top = visual.TextStim(win,text = judgmentCue, height=30, color='white', pos=[0,40], wrapWidth=TEXT_WIDTH)
    bottom = visual.TextStim(win,text = handCue, height=30, color='white', pos=[0,-40], wrapWidth=TEXT_WIDTH)
    drawAndWait(win, 1.9, [top, bottom] + getFixationVisual(win))
    drawAndWait(win, csi, getFixationVisual(win))
    return [judgmentCue, handCue]

def performFeedback(accuracyVector, rtRawVector, win):

    accuracy = 0
    if accuracyVector != []:
        accuracy = 100.*sum(accuracyVector)/len(accuracyVector)

    if accuracy == 0:
        rt = 0
    else:
        rt = round(sum(getRTVector(rtRawVector, accuracyVector))/sum(accuracyVector),4)

    visual.TextStim(win, text = 'Accuracy: {}%'.format(accuracy), height=30, color='white', pos=[0,40], wrapWidth=TEXT_WIDTH).draw()
    visual.TextStim(win, text = 'Reaction Time: {} seconds'.format(rt), height=30, color='white', pos=[0,-40], wrapWidth=TEXT_WIDTH).draw()
    performSpacer(win, userDriven = True)

    return accuracy

def performSpacer(win, userDriven = False):
    performBorder(win)
    if userDriven == True:
        #if DEBUG:
            #print userDriven
        visual.TextStim(win, text = "Press any button on your response box to continue.", height = 30, color = 'white', pos = [0,-250], wrapWidth = TEXT_WIDTH).draw()
        win.flip()
        event.waitKeys(keyList=['1', '2', '3', '4', '9', '8', '7', '6', 'space'])
    else:
        visual.TextStim(win, text = "EXPERIMENTER: Press the space bar to continue.", height = 30, color = 'white', pos = [0,-250], wrapWidth = TEXT_WIDTH).draw()
        win.flip()
        event.waitKeys(keyList='space')

def performMRISync(win):
    performBorder(win)
    visual.TextStim(win, text = "Syncing with scanner - Get ready!", height = 30, color = 'white', pos = [0,-250], wrapWidth = TEXT_WIDTH).draw()
    win.flip()
    event.waitKeys(keyList='t')

#'Participant,Session,Group,BlockName,BlockNum,Trial,Dim,Acc,RT,Expected,Actual,Stim1IsInside,Stim1IsWarm,Stim1IsConvex,'\
#'Stim1IsAbove,Stim2IsInside,Stim2IsWarm,Stim2IsConvex,Stim2IsAbove,StimCue,RespCue,TrialType'
def writeToFile(fh, blockName, blockNum, trial, dim, csi, iti, acc, rt, eyeMvt, expectedKey, actualkey, stim1IsInside, stim1IsWarm, stim1IsConvex, stim1IsAbove, stim2IsInside, stim2IsWarm, stim2IsConvex, stim2IsAbove, stimCue, respCue, trialType):
    trialList = [PARTICIPANT_DATA['subject'], PARTICIPANT_DATA['session'], PARTICIPANT_DATA['group'], GLOBAL_CLOCK.getTime(), blockName, blockNum, trial,
        dim, csi, iti, acc, rt, eyeMvt, expectedKey, actualkey, stim1IsInside, stim1IsWarm, stim1IsConvex, stim1IsAbove, stim2IsInside, stim2IsWarm,
        stim2IsConvex, stim2IsAbove, stimCue, respCue, trialType]

    for i in range(0,len(trialList)):
        if trialList[i] is None:
            trialList[i] = 'None'

    trialString = ','.join(map(str,trialList))
    fh.write('{}\n'.format(trialString))

###################
#Block Definitions#
###################

# Practice sequence for subjects to learn the finger => key mappings
def responsePractice(win, fh):
    visual.TextStim(
        win, text='First, we will orient you to the responses you will be making in this experiment. You will be using the index and middle finger on each '\
        'hand to make your responses. On the next screens, you will see explicit instructions to press different buttons; for example, "Please press the RIGHT INDEX finger." Please make the appropriate responses when '\
        'requested.', height = 30, color = 'white', pos = [0,100], wrapWidth = TEXT_WIDTH
    ).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

    itiList = getJitterVector(NUM_RESPONSE_PRACTICES)

    accuracy = []
    rt = []
    for i in range(0, NUM_RESPONSE_PRACTICES):
        keys = KEY_TO_FINGER.keys()
        random.shuffle(keys)
        j = 1
        for key in keys:
            iti = itiList.pop()
            [pressedKeys, elapsedTime] = drawAndWait(
                win,
                MAX_STIMULI_WAIT_TIME,
                [visual.TextStim(win, text = "Please press the {} finger.".format(getNameForKey(key)), height = 30, color = 'white', pos = [0,0], wrapWidth = TEXT_WIDTH)],
            )
            [trialAccuracy, eyeMvtKey] = evaluateResponse(pressedKeys, None, None, iti, win, keyName=key)
            trialRT = None
            trialResponse = None
            trialEyeMvt = evaluateEyeMvt(eyeMvtKey)
            if pressedKeys != []:
                trialRT = pressedKeys[0][1]
                trialResponse = pressedKeys[0][0]

            writeToFile(fh, 'ResponsePractice', 0, i*len(keys)+j, None, None, iti, trialAccuracy, trialRT, trialEyeMvt, key, trialResponse, None, None, None, None, None,
                None, None, None, None, None, None)

            accuracy.append(trialAccuracy)
            rt.append(trialRT)
            j += 1

    performFeedback(accuracy, rt, win)

    visual.TextStim(win,text = 'Great job! Next, we will learn how to respond to the stimuli that you will see onscreen. While in the real experiment you will see stimulus pairs, we will start with single stimuli. Each stimulus will have four dimensions associated with it, and you will respond to one of these dimensions on each trial. We will start by learning the responses for each dimension one at a time.',
        height=30, color='white',pos=[0,100],wrapWidth=TEXT_WIDTH).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

#DIMENSIONS = {0: 'isInside', 1: 'isWarm', 2: 'isConvex', 3: 'isAbove'}
def colorPractice(win, fh):
    firstText = 'When the color is a WARM color, press the button under your {} finger'.format(getExpectedFinger(1, True))
    secondText = 'When the color of the stimulus is a COOL color, press the button under your {} finger'.format(getExpectedFinger(1, False))
    if getExpectedFinger(1, False) == 'INDEX':
        tmp = firstText
        firstText = secondText
        secondText = tmp

    visual.TextStim(win,text='First, you will learn how to respond to the color of stimuli. Colors can be categorized as warm (red, orange, yellow) or cool (green, blue, purple). To respond to color, you will use your {} hand. {}. {}. '\
        'Let\'s try some examples.'.format(getExpectedHand(1), firstText, secondText), height = 30, color = 'white',
        pos=[0,100], wrapWidth=TEXT_WIDTH
    ).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

    colorList = range(0, 2 * NUM_COLOR_PRACTICES)
    random.shuffle(colorList)

    itiList = getJitterVector(NUM_COLOR_PRACTICES)

    accuracy = []
    rt = []
    trial = 1
    for i in colorList:
        isWarm = i % 2 == 0
        iti = itiList.pop()
        #if DEBUG:
            #print 'Is warm: {}'.format(isWarm)
        [keysPressed, elapsedTime] = drawAndWait(
            win,
            1.9,
            [visual.Rect(win, width=SHAPE_SIZE, height=SHAPE_SIZE, fillColorSpace='dkl', fillColor=getRandomColor(isWarm), lineColor=None)]
        )
        [trialAccuracy, eyeMvtKey, key] = evaluateResponse(keysPressed, 1, isWarm, iti, win)
        trialRT = None
        trialResponse = None
        trialEyeMvt = evaluateEyeMvt(eyeMvtKey)
        if keysPressed != []:
            trialRT = keysPressed[0][1]
            trialResponse = keysPressed[0][0]

        writeToFile(fh, 'ColorPractice', 0, trial, 1, None, iti, trialAccuracy, trialRT, trialEyeMvt, key, trialResponse, None, isWarm, None, None, None,
                None, None, None, None, None, None)

        accuracy.append(trialAccuracy)
        rt.append(trialRT)
        trial += 1

    performFeedback(accuracy, rt, win)

    visual.TextStim(win,text = 'Great job! Next, we will learn how to respond to the convexity of the stimuli.', height=30, color='white',
        pos=[0,150], wrapWidth=TEXT_WIDTH).draw()
    firstText = 'WARM: {} {} finger'.format(getExpectedHand(1), getExpectedFinger(1, True))
    secondText = 'COOL: {} {} finger'.format(getExpectedHand(1), getExpectedFinger(1, False))
    if getExpectedFinger(1, False) == 'INDEX':
        tmp = firstText
        firstText = secondText
        secondText = tmp

    visual.TextStim(win,text='Remember!\n{}\n{}'.format(firstText, secondText), height = 30, color = 'white',
        pos=[0,-25], wrapWidth=TEXT_WIDTH
    ).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

#DIMENSIONS = {0: 'isInside', 1: 'isWarm', 2: 'isConvex', 3: 'isAbove'}
def convexityPractice(win, fh):
    firstText = 'When the stimulus is CONVEX, press the button under your {} finger'.format(getExpectedFinger(2, True))
    secondText = 'when the stimulus is CONCAVE, press the button under your {} finger'.format(getExpectedFinger(2, False))
    if getExpectedFinger(2, False) == 'INDEX':
        tmp = firstText
        firstText = secondText
        secondText = tmp

    visual.TextStim(win,text='Previously you saw colored squares; now we will warp the edges to be either concave (bowed inward) or convex (bowed '\
        'outward). In other words, if the sides of square appear pinched in toward the center, we would call it concave, as if it is "caving" in. If they appear blown outward like '\
        'a balloon, we would call it convex. To respond to convexity, you will use your {} hand. {}. {}. '\
        'Let\'s try some examples.'.format(getExpectedHand(2), firstText, secondText),
        height = 30, color = 'white', pos=[0,100], wrapWidth=TEXT_WIDTH
    ).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

    convexityList = range(0, 2 * NUM_CONVEXITY_PRACTICES)
    random.shuffle(convexityList)

    itiList = getJitterVector(NUM_CONVEXITY_PRACTICES)

    accuracy = []
    rt = []
    trial = 1
    for i in convexityList:
        isConvex = i % 2 == 0
        iti = itiList.pop()
        v1 = getStimulus(x=0, y=0, isConvex=isConvex)
        [keysPressed, elapsedTime] = drawAndWait(
            win,
            1.9,
            [v1[0]]
        )
        [trialAccuracy, eyeMvtKey, key] = evaluateResponse(keysPressed, 2, isConvex, iti, win)
        trialRT = None
        trialResponse = None
        trialEyeMvt = evaluateEyeMvt(eyeMvtKey)
        if keysPressed != []:
            trialRT = keysPressed[0][1]
            trialResponse = keysPressed[0][0]

        writeToFile(fh, 'ConvexityPractice', 0, trial, 2, None, iti, trialAccuracy, trialRT, trialEyeMvt, key, trialResponse, None, v1[2], isConvex, None, None,
                None, None, None, None, None, None)

        accuracy.append(trialAccuracy)
        rt.append(trialRT)
        trial += 1

    performFeedback(accuracy, rt, win)

    visual.TextStim(win,text = 'Great job! Next, we will learn how to respond to the various locations of the '\
        'stimuli. For the rest of the experiment, you will see a dot in the center of the screen. You should '\
        'always try to keep your eyes on this dot, even when doing the task. Your experimenter will notify you '\
        'periodically if you are moving your eyes accidentally.', height=30, color='white',
        pos=[0,150], wrapWidth=TEXT_WIDTH).draw()
    firstText = 'WARM: {} {} finger'.format(getExpectedHand(1), getExpectedFinger(1, True))
    secondText = 'COOL: {} {} finger'.format(getExpectedHand(1), getExpectedFinger(1, False))
    if getExpectedFinger(1, False) == 'INDEX':
        tmp = firstText
        firstText = secondText
        secondText = tmp
    thirdText = 'CONVEX: {} {} finger'.format(getExpectedHand(2), getExpectedFinger(2, True))
    fourthText = 'CONCAVE: {} {} finger'.format(getExpectedHand(2), getExpectedFinger(2, False))
    if getExpectedFinger(2, False) == 'INDEX':
        tmp = thirdText
        thirdText = fourthText
        fourthText = tmp

    visual.TextStim(win,text='Remember!\n{}\n{}\n{}\n{}'.format(firstText, secondText, thirdText, fourthText), height = 30, color = 'white',
        pos=[0,-35], wrapWidth=TEXT_WIDTH
    ).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

#DIMENSIONS = {0: 'isInside', 1: 'isWarm', 2: 'isConvex', 3: 'isAbove'}
def verticalHemifieldPractice(win, fh):
    firstText = 'When the stimulus is ABOVE the horizontal center line, press the button under your {} finger'.format(getExpectedFinger(3, True))
    secondText = 'when the stimulus is BELOW the horizontal center line, press the button under your {} finger'.format(getExpectedFinger(3, False))
    if getExpectedFinger(3, False) == 'INDEX':
        tmp = firstText
        firstText = secondText
        secondText = tmp

    visual.TextStim(win,text='First we will learn to respond to the vertical location of the stimuli. Each stimulus that you see on screen will appear either above or below the horizontal center of the screen; that is, they could appear in the top half or the bottom half of the screen. To respond to '\
        'the vertical location of the stimuli, you will use your {} hand. {}. {}. Let\'s try some examples.'.format(
            getExpectedHand(3), firstText, secondText),
        height = 30, color = 'white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

    verticalHemifieldList = range(0, 2 * NUM_VERTICAL_HEMIFIELD_PRACTICES)
    random.shuffle(verticalHemifieldList)

    itiList = getJitterVector(NUM_VERTICAL_HEMIFIELD_PRACTICES)

    accuracy = []
    rt = []

    trial = 1
    for i in verticalHemifieldList:
        isAbove = i % 2 == 0
        iti = itiList.pop()
        v1 = getStimulus(x=0, isAbove=isAbove)
        [keysPressed, elapsedTime] = drawAndWait(
            win,
            1.9,
            [v1[0]] + getFixationVisual(win)
        )
        [trialAccuracy, eyeMvtKey, key] = evaluateResponse(keysPressed, 3, isAbove, iti, win)

        trialRT = None
        trialResponse = None
        trialEyeMvt = evaluateEyeMvt(eyeMvtKey)
        if keysPressed != []:
            trialRT = keysPressed[0][1]
            trialResponse = keysPressed[0][0]

        writeToFile(fh, 'verticalHemiPractice', 0, trial, 3, None, iti, trialAccuracy, trialRT, trialEyeMvt, key, trialResponse, None, v1[2], v1[3], isAbove, None,
                None, None, None, None, None, None)

        accuracy.append(trialAccuracy)
        rt.append(trialRT)
        trial += 1

    performFeedback(accuracy, rt, win)

    visual.TextStim(win,text = 'Great job! Next, we will learn how to respond to the horizontal location of the '\
    'stimuli. Remember to keep your eyes on the center dot at all times during the task.', height=30, color='white',
        pos=[0,150], wrapWidth=TEXT_WIDTH).draw()
    firstText = 'WARM: {} {} finger'.format(getExpectedHand(1), getExpectedFinger(1, True))
    secondText = 'COOL: {} {} finger'.format(getExpectedHand(1), getExpectedFinger(1, False))
    if getExpectedFinger(1, False) == 'INDEX':
        tmp = firstText
        firstText = secondText
        secondText = tmp
    thirdText = 'CONVEX: {} {} finger'.format(getExpectedHand(2), getExpectedFinger(2, True))
    fourthText = 'CONCAVE: {} {} finger'.format(getExpectedHand(2), getExpectedFinger(2, False))
    if getExpectedFinger(2, False) == 'INDEX':
        tmp = thirdText
        thirdText = fourthText
        fourthText = tmp
    fifthText = 'ABOVE: {} {} finger'.format(getExpectedHand(3), getExpectedFinger(3, True))
    sixthText = 'BELOW: {} {} finger'.format(getExpectedHand(3), getExpectedFinger(3, False))
    if getExpectedFinger(3, False) == 'INDEX':
        tmp = fifthText
        fifthText = sixthText
        sixthText = tmp

    visual.TextStim(win,text='Remember!\n{}\n{}\n{}\n{}\n{}\n{}'.format(firstText, secondText, thirdText, fourthText, fifthText, sixthText), height = 30, color = 'white',
        pos=[0,-35], wrapWidth=TEXT_WIDTH
    ).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

#DIMENSIONS = {0: 'isInside', 1: 'isWarm', 2: 'isConvex', 3: 'isAbove'}
def horizontalLocationPractice(win, fh):
    firstText = 'When the stimulus is near the INSIDE of the screen, press the button under your {} finger'.format(getExpectedFinger(0, True))
    secondText = 'When the stimulus is near the OUTSIDE of the screen, press the button under your {} finger'.format(getExpectedFinger(0, False))
    if getExpectedFinger(0, False) == 'INDEX':
        tmp = firstText
        firstText = secondText
        secondText = tmp

    visual.TextStim(win,text='If you were to draw a line down the vertical center of the screen, you could imagine that the screen could then be divided into a center column that surrounds this center line, and spaces near each of the outer side edges of the screen. Each stimulus that you see on screen will appear either close to the vertical center of the screen, in that center column, or toward the outer side edges. '\
        'To respond to the horizontal location of the stimuli, you will use your {} hand. {}. {}. Let\'s try some examples.'
            .format(getExpectedHand(0), firstText, secondText),
        height = 30, color = 'white', pos=[0,100], wrapWidth=TEXT_WIDTH
    ).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

    horizontalLocationList = range(0, 2 * NUM_HORIZONTAL_LOCATION_PRACTICES)
    random.shuffle(horizontalLocationList)

    itiList = getJitterVector(NUM_HORIZONTAL_LOCATION_PRACTICES)

    accuracy = []
    rt = []

    trial = 1
    for i in horizontalLocationList:
        isInside = i % 2 == 0
        iti = itiList.pop()
        v1 = getStimulus(isInside=isInside)
        [keysPressed, elapsedTime] = drawAndWait(
            win,
            1.9,
            [v1[0]] + getFixationVisual(win)
            )
        [trialAccuracy, eyeMvtKey, key] = evaluateResponse(keysPressed, 0, isInside, iti, win)
        trialRT = None
        trialResponse = None
        trialEyeMvt = evaluateEyeMvt(eyeMvtKey)
        if keysPressed != []:
            trialRT = keysPressed[0][1]
            trialResponse = keysPressed[0][0]

        writeToFile(fh, 'verticalHemiPractice', 0, trial, 0, None, iti, trialAccuracy, trialRT, trialEyeMvt, key, trialResponse, isInside, v1[2], v1[3], v1[4], None,
                None, None, None, None, None, None)

        accuracy.append(trialAccuracy)
        rt.append(trialRT)
        trial += 1

    performFeedback(accuracy, rt, win)

    visual.TextStim(win,text = 'Great job! In the real experiment, you will see two stimuli at a time, one on the left side of the screen and one on the right, and they will each have a color, convexity, vertical '\
        'position, and horizontal position. Now we will learn how to respond to those pairs of stimuli.', height=30, color='white',
        pos=[0,150], wrapWidth=TEXT_WIDTH).draw()
    firstText = 'WARM: {} {} finger'.format(getExpectedHand(1), getExpectedFinger(1, True))
    secondText = 'COOL: {} {} finger'.format(getExpectedHand(1), getExpectedFinger(1, False))
    if getExpectedFinger(1, False) == 'INDEX':
        tmp = firstText
        firstText = secondText
        secondText = tmp
    thirdText = 'CONVEX: {} {} finger'.format(getExpectedHand(2), getExpectedFinger(2, True))
    fourthText = 'CONCAVE: {} {} finger'.format(getExpectedHand(2), getExpectedFinger(2, False))
    if getExpectedFinger(2, False) == 'INDEX':
        tmp = thirdText
        thirdText = fourthText
        fourthText = tmp
    fifthText = 'ABOVE: {} {} finger'.format(getExpectedHand(3), getExpectedFinger(3, True))
    sixthText = 'BELOW: {} {} finger'.format(getExpectedHand(3), getExpectedFinger(3, False))
    if getExpectedFinger(3, False) == 'INDEX':
        tmp = fifthText
        fifthText = sixthText
        sixthText = tmp
    seventhText = 'INSIDE: {} {} finger'.format(getExpectedHand(0), getExpectedFinger(0, True))
    eighthText = 'OUTSIDE: {} {} finger'.format(getExpectedHand(0), getExpectedFinger(0, False))
    if getExpectedFinger(0, False) == 'INDEX':
        tmp = seventhText
        seventhText = eighthText
        eighthText = tmp

    visual.TextStim(win,text='Remember!\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(firstText, secondText, thirdText, fourthText, fifthText, sixthText, seventhText, eighthText), height = 30, color = 'white',
        pos=[0,-75], wrapWidth=TEXT_WIDTH
    ).draw()
    #if DEBUG:
        #print getSession()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

#DIMENSIONS = {0: 'isInside', 1: 'isWarm', 2: 'isConvex', 3: 'isAbove'}
def pairPractice(win, fh):

    visual.TextStim(win,text='Each pair of stimuli that you see will have exactly one dimension in common. That is, they could have the same judgment value for exactly one dimension at a time. For example, they could both be cool-colored;'\
        ' but then, necessarily, one would be concave and one would be convex; one would be in the top half of the screen, and one in the bottom half; and one would appear toward the vertical center, and one toward the outer side edges.'\
        ' They can share the same value along any of the four dimensions, but they will only share one of these dimensions at a time.',
        height = 30, color = 'white', pos=[0,100], wrapWidth=TEXT_WIDTH
    ).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

    visual.TextStim(win,text='Your task is to identify which of these is the shared dimension, and to indicate which value they share using the responses you '\
        'learned in the previous blocks. For example, if you see two stimuli that are both a cool color, you should press the {} finger on your {} '\
        'hand. The next block will introduce you to these stimulus pairs. This block is particularly difficult; perfect performance is not expected. Rather, we want you to get used to seeing and judging these pairs correctly, even if it takes you too long right now to respond in time. Just try your best! Remember to keep your eyes on the center dot at all times during the task.'.format(getExpectedFinger(1,False),getExpectedHand(1)),
        height = 30, color = 'white', pos=[0,100], wrapWidth=TEXT_WIDTH
    ).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

    # 4 dims * 2 choices * # of practice rounds = total number of trials
    # this random ordered list of numbers 0-4 determines the order of the dimensions we use
    trials = []
    for i in range(0, len(DIMENSIONS) * 2 * NUM_PAIR_PRACTICES):
        trials.append(i % len(DIMENSIONS))
    random.shuffle(trials)

    # same as above, but is a 2D array from dim => rondomly ordered list of correct choices
    choiceDict = defaultdict(list)
    for i in range(0, len(DIMENSIONS)):
        for j in range(0, (2 * NUM_PAIR_PRACTICES)):
            choiceDict[i].append(j % 2 == 0)
        random.shuffle(choiceDict[i])

    #if DEBUG:
        #print 'trial order: ', trials
        #print 'expected choices: ', choiceDict
    itiList = getJitterVector(len(trials) / 4)
    accuracy = []
    rt = []
    trial = 1
    for dim in trials:
        iti = itiList.pop()
        lockedInside = lockedWarm = lockedConvex = lockedAbove = cueChoice = None
        answer = choiceDict[dim].pop()

        if dim == 0:
            lockedInside = answer
        elif dim == 1:
            lockedWarm = answer
        elif dim == 2:
            lockedConvex = answer
        else:
            lockedAbove = answer
        #if DEBUG:
            #print dim
            #print answer
        key = getExpectedKey(dim, answer)
        [trialAccuracy, trialRT, trialResponse, trialEyeMvt, elapsedTime, v1, v2, judgmentCue, handCue] = fullTrialDraw(win, None, iti, dim, answer,
            cueChoice, lockedInside, lockedWarm, lockedConvex, lockedAbove) #Suck it, Trebek!

        writeToFile(fh, 'PairPractice', 0, trial, dim, None, iti, trialAccuracy, trialRT, trialEyeMvt, key, trialResponse, v1[1], v1[2], v1[3], v1[4], v2[1],
                v2[2], v2[3], v2[4], judgmentCue, handCue, None)

        accuracy.append(trialAccuracy)
        rt.append(trialRT)
        trial += 1

    performFeedback(accuracy, rt, win)

    visual.TextStim(win,text = 'Great job! Now we will add some cues that will help you do the task you just learned.', height=30, color='white', pos=[0,150], wrapWidth=TEXT_WIDTH).draw()
    firstText = 'WARM: {} {} finger'.format(getExpectedHand(1), getExpectedFinger(1, True))
    secondText = 'COOL: {} {} finger'.format(getExpectedHand(1), getExpectedFinger(1, False))
    if getExpectedFinger(1, False) == 'INDEX':
        tmp = firstText
        firstText = secondText
        secondText = tmp
    thirdText = 'CONVEX: {} {} finger'.format(getExpectedHand(2), getExpectedFinger(2, True))
    fourthText = 'CONCAVE: {} {} finger'.format(getExpectedHand(2), getExpectedFinger(2, False))
    if getExpectedFinger(2, False) == 'INDEX':
        tmp = thirdText
        thirdText = fourthText
        fourthText = tmp
    fifthText = 'ABOVE: {} {} finger'.format(getExpectedHand(3), getExpectedFinger(3, True))
    sixthText = 'BELOW: {} {} finger'.format(getExpectedHand(3), getExpectedFinger(3, False))
    if getExpectedFinger(3, False) == 'INDEX':
        tmp = fifthText
        fifthText = sixthText
        sixthText = tmp
    seventhText = 'INSIDE: {} {} finger'.format(getExpectedHand(0), getExpectedFinger(0, True))
    eighthText = 'OUTSIDE: {} {} finger'.format(getExpectedHand(0), getExpectedFinger(0, False))
    if getExpectedFinger(0, False) == 'INDEX':
        tmp = seventhText
        seventhText = eighthText
        eighthText = tmp

    visual.TextStim(win,text='Remember!\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(firstText, secondText, thirdText, fourthText, fifthText, sixthText, seventhText, eighthText), height = 30, color = 'white',
        pos=[0,-25], wrapWidth=TEXT_WIDTH
    ).draw()
    if getSession() == '2':
        performSpacer(win, userDriven = True)
    else:
        performSpacer(win)

def fullBlock(win, fh, block = 0, practice = False):
    if practice:
        visual.TextStim(win,text='Before the stimuli are presented on each trial, you will see a cue that consists of two words, one shown above the fixation dot, and one shown below it. This cue may give you some information about the upcoming '\
            'trial. You should use these cues to help you narrow down what judgment and response you have to make.',
            height = 30, color = 'white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
        if getSession() == '2':
            performSpacer(win, userDriven = True)
        else:
            performSpacer(win)
        visual.TextStim(win,text='The upper cue will tell you what type of dimension your stimuli will have in common. We will not tell you exactly which dimension, but we will categorize them for you. If the upcoming stimuli will be in the same '\
            'vertical or horizontal location, you will be cued with the word SPATIAL. If the upcoming stimuli will share the same color type or convexity, '\
            'you will be cued with the word OBJECT. These types of cues will appear above the fixation dot in the center of the screen.',
            height = 30, color = 'white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
        if getSession() == '2':
            performSpacer(win, userDriven = True)
        else:
            performSpacer(win)
        visual.TextStim(win,text='The lower cue will tell you which hand you will use to make your response. If the upcoming response will be on the left hand, '\
            'you will be cued with the word LEFT. If the upcoming response is on the right hand, you will be cued with the word RIGHT. These types of cues will appear '\
            'below the fixation dot in the center of the screen. Note that these cues also narrow down the possible judgments you have to make as well; just not in a categorical way.',
            height = 30, color = 'white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
        if getSession() == '2':
            performSpacer(win, userDriven = True)
        else:
            performSpacer(win)
        visual.TextStim(win,text='In some cases, you will receive no information for one or both of these types of cues. In this case, you will see XXXXX in '\
            'the location that the cues would otherwise appear. This means you can receive four types of cues. In some cases, you will get no information for either '\
            'cue; in some cases, you will get information for only the judgment type (SPATIAL/OBJECT) or the response hand (LEFT/RIGHT); and in some cases, you will '\
            'get information for both at once. In every case, you should use these cues to the best of your ability to help you prepare for the upcoming trial. Let\'s '\
            'try some examples.\n\nRemember to keep your eyes on the center dot at all times during the task.',
            height = 30, color = 'white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
        if getSession() == '2':
            performSpacer(win, userDriven = True)
        else:
            performSpacer(win)
    else:
        visual.TextStim(win,text='Ready for the next block?',
            height = 30, color = 'white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
        performMRISync(win)
    # 4 dims * 2 choices * 4 cues * # practices = total number of trials

    [cueTimes, stimTimes, indices] = timingSetup(block+1)

    itiList = map(sub, cueTimes[1:] + [NUM_TIME], [x + 2 for x in stimTimes])
    csiList = map(sub, stimTimes, [x + 2 for x in cueTimes])

    cueList = [getCueType(getTrialType(i)[0:2]) for i in indices]
    handList = [getHandType(getTrialType(i)[-1]) for i in indices]
    dimList = [getDimType(getTrialType(i)[-2:]) for i in indices]
    answerTracker = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    # this just looks scary, but is simple once you wrap your mind around it. for every dimension and
    # ever answer (true or false), we want to have a trial using each of the 4 cues (x how many practice
    # runs total are actually requested). This idea of adding another 'dimension' or 'variable' to the trials
    # is 100% extensible, so another variable such as 'jitter' will be just another loop and another level
    #
    # to be clear, we only need to do this advanced craziness if we want to ensure that each type of cue is
    # practiced across every other dimension with a evenly distributed rate (so each dimension and each choice
    # are guaranteed to have all 4). If you just want to randomize the jitter across trials, waaaaaay easier.
    # Across groups is even easier as well. Think about what dependencies you want for a new dimension/variable
    # before doing this complex style of loop and lookup

    #if DEBUG:
        #print 'trials: ', trials
        #print 'expected answers: ', choiceDict
        #print 'cueDict: ', cueDict
    accuracy = []
    rt = []
    trial = 1
    feedbackOff = False
    if (not practice) and getSession() == '2':
        feedbackOff = True

    blockName = 'fullBlock'
    if practice:
        blockName = 'CuePractice'

    blockLength = len(csiList)
    while trial <= blockLength:
        lockedWarm = lockedInside = lockedConvex = lockedAbove = cueChoice = None
        cueChoice = cueList.pop(0)
        csi = csiList.pop(0)
        dim = dimList.pop(0)
        iti = itiList.pop(0)

        [answerTracker, answer]=getAnswer(answerTracker, trial-1, indices)
        if dim == 0:
            lockedInside = answer
        elif dim == 1:
            lockedWarm = answer
        elif dim == 2:
            lockedConvex = answer
        else:
            lockedAbove = answer
        key = getExpectedKey(dim, answer)
        [trialAccuracy, trialRT, trialResponse, trialEyeMvt, elapsedTime, v1, v2, judgmentCue, handCue] = fullTrialDraw(win, csi, iti, dim, answer, cueChoice,
            lockedInside, lockedWarm, lockedConvex, lockedAbove, feedbackOff)

        writeToFile(fh, blockName, block, trial, dim, csi, iti, trialAccuracy, trialRT, trialEyeMvt, key, trialResponse, v1[1], v1[2], v1[3], v1[4], v2[1],
                v2[2], v2[3], v2[4], judgmentCue, handCue, INDEX_TO_TRIALTYPE[indices[trial-1]])

        accuracy.append(trialAccuracy)
        rt.append(trialRT)
        trial += 1

    return performFeedback(accuracy, rt, win)


###############
#Main Function#
###############

if __name__ == '__main__':
    experimentSetup()
    print 'Participant Data: ', PARTICIPANT_DATA
    #Must occur after experimentSetup due to pyglet to PsychoPy issue with dropdown selections
    from psychopy import visual

    if PARTICIPANT_DATA is None:
        print 'Subject pressed cancel, killing experiment'
        core.quit()

    win = windowSetup()
    fh = fileSetup()

    if getSession() == '1':
        responsePractice(win, fh)
    colorPractice(win, fh)
    convexityPractice(win, fh)
    verticalHemifieldPractice(win, fh)
    horizontalLocationPractice(win, fh)
    pairPractice(win, fh)
    test = fullBlock(win, fh, 0, practice=True)
    if getSession() == '1':
        visual.TextStim(win,text = 'Great job! That is the end of the training. We will now play sounds recorded from an MRI to simulate the MRI environment as closely as possible. You will now complete as few as 6 and as as many as 12 practice blocks to learn to do the task as quickly and accurately as possible. While there is not an easy way to know when you will be done, remember: the more quickly you become more accurate, the faster you will finish! A good goal is to be hitting 90+% accuracy by the end of the session. Remember to keep your eyes on the center dot at all times during the task.',
            height=30, color='white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
    else:
        visual.TextStim(win,text = 'Great job! That is the end of the practice. Please wait for the structural scan to finish. Next, you will complete 16 experimental blocks while we record your brain activity. Throughout the experiment, try to do the task as quickly and accurately as possible. It is important to remember to remain as still as possible at all times, but especially in the middle of each block. If you need to adjust yourself, try to do so in between blocks and do so while keeping your head as still as possible. Remember to keep your eyes on the center dot at all times during the task.',
            height=30, color='white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
    performSpacer(win)
    runningAccCheck = []
    i = 1
    while i <= NUMBER_OF_BLOCKS:
        runningAccCheck = runningAccCheck + [fullBlock(win, fh, block=i)]
        if getSession() == '1' and i >= 6 :
            #if DEBUG:
                #print runningAccCheck[-3:]
            if sum(runningAccCheck[-3:])/3 > 90 or i>=NUMBER_OF_BLOCKS:
                i = NUMBER_OF_BLOCKS + 1
                visual.TextStim(win,text = 'That\'s it! Please wait for the experimenter to bring you out.',
                    height=30, color='white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
                performSpacer(win)
            else:
                visual.TextStim(win,text = 'Great job! Take a break if you need it. Remember to keep your eyes on the '\
                    'center dot at all times during the task.',
                    height=30, color='white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
                visual.TextStim(win,text = i,
                    height=6, color='white', pos=[WINDOW_WIDTH/2-SHAPE_SIZE/2-6,WINDOW_HEIGHT/2-6]).draw()
                performSpacer(win)
                i += 1
        elif i < NUMBER_OF_BLOCKS:
            visual.TextStim(win,text = 'Great job! Remember to keep your eyes on the '\
                'center dot at all times during the task, and to stay as still as possible.',
                height=30, color='white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
            visual.TextStim(win,text = i,
                    height=6, color='white', pos=[WINDOW_WIDTH/2-SHAPE_SIZE/2-6,WINDOW_HEIGHT/2-6]).draw()
            performSpacer(win)
            i += 1
        else:
            visual.TextStim(win,text = 'That\'s it! Please wait for the experimenter to bring you out.',
                    height=30, color='white', pos=[0,100], wrapWidth=TEXT_WIDTH).draw()
            performSpacer(win)
            i += 1
        if DEBUG:
            print runningAccCheck
            print i

    cleanShutdown(win, fh)
