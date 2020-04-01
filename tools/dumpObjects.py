# Extract object data to files

import sys
import common
import StringIO

# Get common code
index = sys.argv[0].rfind('/')
if index == -1:
    directory = ''
else:
    directory = sys.argv[0][:index+1]
execfile(directory+'common.py')

if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' rom.gbc')
    print('Output goes to various files in the "objects/" directory')
    sys.exit()


# Opcode types
opcodeTypeStrings = ["obj_Conditional", "obj_NoValue", "obj_DoubleValue", "obj_Pointer",
                     "obj_BossPointer", "obj_AntiBossPointer", "obj_RandomEnemy",
                     "obj_SpecificEnemy", "obj_Part", "obj_WithParam", "obj_ItemDrop"]


class ObjectData:

    def __init__(self):
        self.group = -1

# Variables

romFile = open(sys.argv[1], 'rb')
data = bytearray(romFile.read())
rom = data

extraInteractionBankPatch = False

if romIsAges(rom):
    gameString = 'ages'
    dataBank = 0x12
    pointerBank = 0x15

    groupPointerTable = 0x15*0x4000 + 0x32b

    extraInteractionBank = 0xfa
    if rom[0x54328] == 0xc3:
        extraInteractionBankPatch = True
else:
    gameString = 'seasons'
    dataBank = 0x11
    pointerBank = 0x11

    groupPointerTable = 0x11*0x4000 + 0x1b3b

    extraInteractionBank = 0x7f
    if rom[0x458dc] == 0xcd:
        extraInteractionBankPatch = True


if extraInteractionBankPatch:
    print('INFO: "Extra Interaction Bank" patch from ZOLE detected. This is supported.')


pointerFile  = open("objects/" + gameString + "/pointers.s", 'w')
helperFile   = open("objects/" + gameString + "/extraData1.s", 'w')
helperFile2  = open("objects/" + gameString + "/extraData2.s", 'w')
helperFile3  = open("objects/" + gameString + "/extraData3.s", 'w')
mainDataFile = open("objects/" + gameString + "/mainData.s", 'w')

objectDataList = list()
mainObjectDataStr = StringIO.StringIO()

labelPositions = {}


def parseObjectData(buf, pos, outFile):
    output = str()
    start = pos

    lastOpcode = -1
    while (data[pos] < 0xfe):
        # Some objects are referenced midway through
        if pos != start and labelPositions.has_key(pos):
            value = labelPositions[pos]
            if value == -1:
                output += 'objectData' + \
                    myhex((pos&0x3fff)+0x4000, 4) + ':\n'
            else:
                for intData in value:
                    output += 'group' + \
                        str(intData.group) + 'Map' + \
                        myhex(intData.map, 2) + 'ObjectData:\n'
                    intData.address = 0

        op = data[pos]
        if op < 0xf0 and lastOpcode != -1:
            op = lastOpcode
            fresh = 0
        else:
            op &= 0xf
            pos+=1
            fresh = 1

        output += '\t' + opcodeTypeStrings[op] + ' '

        if (op == 0x01):  # No-value
            output += wlahex(read16BE(buf, pos), 4) + '\n'
            pos+=2
        elif op == 0x02:  # Double-value
            output += wlahex(read16BE(buf, pos), 4) + ' '
            output += wlahex(buf[pos+2], 2) + ' '
            output += wlahex(buf[pos+3], 2) + '\n'
            pos+=4
        elif op == 0x03:  # Pointer
            output += 'objectData' + myhex(read16(buf, pos), 4) + '\n'
            #output += wlahex(read16(buf, pos), 4) + '\n'
            pointer = bankedAddress(0x12, read16(buf, pos))
            labelPositions[pointer] = -1
            pos+=2
        elif op == 0x04:  # Pointer (Bit 7 of room flags unset)
            output += 'objectData' + myhex(read16(buf, pos), 4) + '\n'
            #output += wlahex(read16(buf, pos), 4) + '\n'
            pointer = bankedAddress(0x12, read16(buf, pos))
            labelPositions[pointer] = -1
            pos+=2
        elif op == 0x05:  # Pointer (Bit 7 of room flags set)
            output += 'objectData' + myhex(read16(buf, pos), 4) + '\n'
            #output += wlahex(read16(buf, pos), 4) + '\n'
            pointer = bankedAddress(0x12, read16(buf, pos))
            labelPositions[pointer] = -1
            pos+=2
        elif op == 0x06:  # Random spawn
            output += wlahex(buf[pos], 2) + ' '
            output += wlahex(read16BE(buf, pos+1), 4) + '\n'
            pos+=3
        elif op == 0x07:  # Specific spawn
            if fresh == 1:
                output += wlahex(buf[pos], 2) + ' '
                pos+=1
            else:
                output += '    '
            output += wlahex(read16BE(buf, pos), 4) + ' '
            output += wlahex(buf[pos+2], 2) + ' '
            output += wlahex(buf[pos+3], 2) + '\n'
            pos+=4
        elif op == 0x08:  # Part
            output += wlahex(read16BE(buf, pos), 4) + ' '
            output += wlahex(buf[pos+2], 2) + '\n'
            pos+=3
        elif op == 0x09:  # Quadruple
            output += wlahex(buf[pos+0], 2) + ' '
            output += wlahex(read16BE(buf, pos+1), 4) + ' '
            output += wlahex(buf[pos+3], 2) + ' '
            output += wlahex(buf[pos+4], 2) + ' '
            output += wlahex(buf[pos+5], 2) + '\n'
            pos+=6
        elif op == 0x0a:  # Item Drop
            if fresh == 1:
                output += wlahex(buf[pos], 2) + ' '
                pos+=1
            else:
                output += '    '
            output += wlahex(buf[pos], 2) + ' '
            output += wlahex(buf[pos+1], 2) + '\n'
            pos+=2
        elif op == 0x0:  # Conditional
            output += wlahex(buf[pos], 2) + '\n'
            pos+=1
        else:
            print("UNKNOWN OP " + hex(op) + " at " + hex(pos))
            pos+=1

        lastOpcode = op

    # This is needed for address 45b3
    if pos != start and labelPositions.has_key(pos):
        output += 'objectData' + myhex((pos&0x3fff)+0x4000, 4) + ':\n'

    if (data[pos] == 0xfe):
        output += '\tobj_EndPointer\n'
    else:
        output += '\tobj_End\n'
    pos+=1

    if outFile is not None:
        outFile.write(output + '\n')

    return pos

# Main code

# Start on pointer file
pointerFile.write('objectDataGroupTable:\n')
for i in xrange(8):
    write = i
    if i > 5:
        write -= 2
    elif romIsSeasons(rom) and i >= 1 and i < 4:
        write = 1
    pointerFile.write('\t.dw group' + str(write) + 'ObjectDataTable\n')

pointerFile.write('\n')

# Go through each group's object data, store into data structures for
# later
for group in xrange(6):
    if romIsSeasons(rom) and group >= 2 and group <= 3:
        continue # Groups 2 and 3 don't really exist

    pointerTable = bankedAddress(pointerBank, read16(data, groupPointerTable + group*2))

    pointerFile.write('group' + str(group) + 'ObjectDataTable:\n')
    for map in xrange(0x100):
        rawPointer = read16(data, pointerTable+map*2)
        if rawPointer & 0xc000 == 0xc000:
            if not extraInteractionBankPatch:
                print('WARNING: "extraInteractionBank" seems to be used, but the rom isn\'t patched for it?')
            pointer = bankedAddress(extraInteractionBank, rawPointer)
        else:
            pointer = bankedAddress(dataBank, rawPointer)

        objectData = ObjectData()
        objectData.group = group
        objectData.map = map
        objectData.address = pointer

        objectDataList.append(objectData)
        if not labelPositions.has_key(pointer):
            labelPositions[pointer] = []
        labelPositions[pointer].append(objectData)

        pointerFile.write('\t.dw group' + str(group) + 'Map' +
                          myhex(map, 2) + 'ObjectData\n')

    pointerFile.write('\n')


# Piece of data not accounted for
if romIsAges(rom):
    extraData = ObjectData()
    extraData.address = 0x49f9d
    extraData.group = -1
    objectDataList.append(extraData)
elif romIsSeasons(rom):
    extraData = ObjectData()
    extraData.address = 0x46500
    extraData.group = -1
    objectDataList.append(extraData)

    extraData = ObjectData()
    extraData.address = 0x46bea
    extraData.group = -1
    objectDataList.append(extraData)

# Main data for groups
objectDataList = sorted(
    objectDataList, key=lambda obj: obj.address)

for objectData in objectDataList:
    address = objectData.address
    if address != 0:
        for data2 in objectDataList:
            if data2.address == address:
                if data2.group == -1:
                    mainObjectDataStr.write(
                        'objectData' + myhex((address&0x3fff)+0x4000, 4) + ':\n')
                else:
                    if extraInteractionBankPatch:
                        addrString = myhex(address/0x4000,2) + ':' + myhex((address&0x3fff)+0x4000, 4)
                    else:
                        addrString = myhex((address&0x3fff)+0x4000, 4)
                    mainObjectDataStr.write('group' +
                                                 str(data2.group) +
                                                 'Map' + myhex(data2.map, 2) + 'ObjectData: ; ' +
                                                 addrString + '\n')
                data2.address = 0
        parseObjectData(data, address, mainObjectDataStr)

helperOut = StringIO.StringIO()

# Search for all data blocks earlier on

if romIsAges(rom):
    pos = 0x48000

    while pos < 0x49482:
        helperOut.write('objectData' + myhex((pos&0x3fff)+0x4000, 4) + ':\n')
        pos = parseObjectData(data, pos, helperOut)

    # Weird table in the middle of everything
    helperOut.write('objectTable1:\n')
    while pos < 0x49492:
        helperOut.write(
            '\t.dw objectData' + myhex(read16(data, pos), 4) + '\n')
        pos+=2
    helperOut.write('\n')

    while pos < 0x495b6:
        helperOut.write('objectData' + myhex((pos&0x3fff)+0x4000, 4) + ':\n')
        pos = parseObjectData(data, pos, helperOut)
    # Code is after this

    # After main data is more object data, purpose unknown
    pos = 0x4b6dd
    # First a table of sorts
    helperFile2.write('objectTable2:\n')
    while pos < 0x4b705:
        helperFile2.write(
            '.dw ' + 'objectData' + myhex(read16(data, pos), 4) + '\n')
        pos += 2
    helperFile2.write('\n')
    # Now more object data
    while pos < 0x4b8bd:
        helperFile2.write(
            'objectData' + myhex((pos&0x3fff)+0x4000, 4) + ':\n')
        pos = parseObjectData(data, pos, helperFile2)
    # Another table
    helperFile2.write('objectTable3:\n')
    while pos < 0x4b8c5:
        helperFile2.write(
            '.dw ' + 'objectData' + myhex(read16(data, pos), 4) + '\n')
        pos += 2
    helperFile2.write('\n')
    # Now more object data
    while pos < 0x4b8e4:
        helperFile2.write(
            'objectData' + myhex((pos&0x3fff)+0x4000, 4) + ':\n')
        pos = parseObjectData(data, pos, helperFile2)

    # One last round of object data
    helperFile3.write('; A few objects stuffed into the very end\n\n')
    pos = 0x4be69
    while pos < 0x4be8f:
        helperFile3.write('objectData' + myhex(toGbPointer(pos), 4) + ':\n')
        pos = parseObjectData(data, pos, helperFile3)

else: # Seasons
    pos = 0x44000

    while pos < 0x45744:
        helperOut.write('objectData' + myhex((pos&0x3fff)+0x4000, 4) + ':\n')
        pos = parseObjectData(data, pos, helperOut)

    # Weird table in the middle of everything
    helperOut.write('objectTable1:\n')
    while pos < 0x4575e:
        helperOut.write(
            '\t.dw objectData' + myhex(read16(data, pos), 4) + '\n')
        pos+=2
    helperOut.write('\n')

    while pos < 0x458b5:
        helperOut.write('objectData' + myhex((pos&0x3fff)+0x4000, 4) + ':\n')
        pos = parseObjectData(data, pos, helperOut)

    # After main data is more object data
    pos = 0x47dd9
    # First a table of sorts
    while pos < 0x47eb0:
        helperFile2.write(
            'objectData' + myhex((pos&0x3fff)+0x4000, 4) + ':\n')
        pos = parseObjectData(data, pos, helperFile2)
    helperFile2.write('\n')

# Write output to files (for those which don't write directly to the files)

helperOut.seek(0)
helperFile.write(helperOut.read())

mainObjectDataStr.seek(0)
mainDataFile.write(mainObjectDataStr.read())


romFile.close()
helperFile.close()
helperFile2.close()
helperFile3.close()
mainDataFile.close()
