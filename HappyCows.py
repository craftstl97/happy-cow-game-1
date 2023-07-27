import random
import sys
import fileinput

# handles command line input
def getFileNames(argv):
    iFile = argv[0]
    oFile = argv[1]

    return (iFile, oFile)

# checks if a given row col pair is in the grid
def inRange(row: int, col: int, gridSize: int) -> bool:
    if row < 0 or col < 0 or row > gridSize-1 or col > gridSize-1:
        return False
    return True

# checks adjacent spaces for cows, haystacks, and ponds
def setFlags(row: int, col: int, grid: list, gridSize: int) -> tuple:
    offsets = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
    cow = False
    hay = False
    pond = False

    # iterate through offsets
    for dir in range(8):
        testRow = row + offsets[dir][0]
        testCol = col + offsets[dir][1]
        if inRange(testRow, testCol, gridSize):
            # check all spaces for cows
            if grid[testRow][testCol] == "C":
                cow = True

            # don't check corners for hay or ponds
            if dir % 2 == 1:
                if grid[testRow][testCol] == "@":
                    hay = True
                if grid[testRow][testCol] == "#":
                    pond = True

        # return if all flags are set
        if cow and hay and pond:
            return (cow, hay, pond)

    # otherwise return all flags when done
    return (cow, hay, pond)

# returns the score of a given placement
def scorePlacement(grid: list, gridSize: int) -> int:
    cowScore = 0
    totalScore = 0

    # flags to identify adjacent tiles
    haystack = False
    pond = False
    cow = False

    # iterate through the entire grid
    for x in range(gridSize):
        for y in range(gridSize):
            # check for cow
            if grid[x][y] == "C":

                # check the surrounding tiles and update flags
                flags = setFlags(x, y, grid, gridSize)
                cow = flags[0]
                haystack = flags[1]
                pond = flags[2]

                # haystack = +1
                if haystack:
                    cowScore += 1
                    # haystack and pond = +3
                    if pond:
                        cowScore += 2
                # cow = -3
                if cow:
                    cowScore -= 3

                # update score and reset flags
                totalScore += cowScore
                haystack = False
                pond = False
                cow = False
                cowScore = 0

    return totalScore

# AI places a cow, currently determined randomly (no AI)
def placeCow(grid: list, gridSize: int):
    # generate random coordinates
    x = random.randint(0, gridSize - 1)
    y = random.randint(0, gridSize - 1)

    # check if the placement is valid
    while grid[x][y] != ".":
        x = random.randint(0, gridSize - 1)
        y = random.randint(0, gridSize - 1)

    # place a cow there
    line = list(grid[x])
    line[y] = "C"
    grid[x] = "".join(line)

# writes to output file
def writeToFile(fileName: str, gridSize: int, grid: list):
    file = open(fileName, 'w')
    # grid size
    file.write(str(gridSize) + "\n")

    # grid
    for line in grid:
        file.write(line + "\n")

    # Score
    file.write(str(scorePlacement(grid, gridSize)))
    file.close()

# main driver function
if __name__ == "__main__":
    grid = []
    IO = getFileNames(sys.argv[1:])

    for line in fileinput.input(files = IO[0]):
        grid.append(line.strip())

    # removes the grid size line and stores it as an integer
    gridSize = int(grid.pop(0))

    # counts the haystacks
    haystacks = 0
    for line in grid:
        for placement in line:
            if placement == "@":
                haystacks += 1

    # place one cow for every haystack
    for x in range(haystacks):
        placeCow(grid, gridSize)

    # write the grid size, grid, and score to the file
    writeToFile(IO[1], gridSize, grid)
