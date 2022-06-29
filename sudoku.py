
# think of it as a graph coloring problem?

import copy


class Sudoku:

    def __init__(self, values, changed):
        self.values = values
        self.changed = True

    def buildPermutations(self, nums):
        ans = []
        for i in range(len(nums)):
            ans = self.buildPermutationsUtil(ans, nums[i])
        return ans

    def buildPermutationsUtil(self, ans, num):
        if ans == []:
            return [[num]]

        temp = []
        length = len(ans[0])
        for i in range(length):
            for j in range(length+1):
                add = copy.deepcopy(ans[i])
                add.insert(j, num)
                temp.append(add)
        return temp

    def printBoard(self, values):
        if values is None:
            print("error")
        else:
            ans = ""
            for i in values:
                for j in i:
                    ans += str(j) + " "
                ans += '\n'
            ans += '\n'
            print(ans)

    def getValues(self):
        values = [[0 for x in range(9)] for y in range(9)]
        for i in range(9):
            for j in range(9):
                temp = input(
                    "Value? (insert row row from top to bottom)" + '\n')
                values[i][j] = int(temp)
        return values

    def searchColumn(self, values, i, j):
        possible = [True for x in range(9)]
        for z in range(9):
            if values[z][j] != 0:
                possible[values[z][j]-1] = False
        return possible

    # i is row number and j is column number

    def searchRow(self, values, i, j):
        possible = [True for x in range(9)]
        for z in range(9):
            if values[i][z] != 0:
                possible[values[i][z]-1] = False
        return possible

    def searchBox(self, values, i, j):
        possible = [True for x in range(9)]
        for x in range(3):
            for y in range(3):
                if values[(int)(i/3) * 3+x][(int)(j/3) * 3+y] != 0:
                    possible[values[(int)(i/3) * 3+x]
                             [(int)(j/3) * 3+y]-1] = False
        return possible

    def boxElimination(self, values, bx, by):
        box_possible = self.searchBox(values, bx*3, by*3)
        for i in range(9):
            if box_possible[i]:

                for x in range(3):
                    for y in range(3):
                        arr1 = self.searchRow(values, bx*3+x, by*3+y)
                        arr2 = self.searchColumn(values, bx*3+x, by*3+y)
                        if values[bx*3+x][by*3+y] == 0:
                            if self.countSolutions(arr1) == 1:
                                if not arr2[self.findIndex(arr1)]:
                                    print("f1")
                                    return
                                else:
                                    values[bx*3+x][by*3 +
                                                   y] = self.findIndex(arr1)+1
                                    self.changed = True
                            elif self.countSolutions(arr2) == 1:
                                if not arr1[self.findIndex(arr2)]:
                                    print("f1")
                                    return
                                else:
                                    values[bx*3+x][by*3 +
                                                   y] = self.findIndex(arr2)+1
                                    self.changed = True
                            elif self.countSolutions(box_possible) == 1:
                                if not arr1[self.findIndex(box_possible)] or not arr2[self.findIndex(box_possible)]:
                                    print("f1")
                                    return
                                else:
                                    values[bx*3+x][by*3 +
                                                   y] = self.findIndex(box_possible)+1
                                    self.changed = True

                if not self.changed:
                    is_first = True
                    first = []
                    for x in range(3):
                        for y in range(3):
                            arr1 = self.searchRow(values, bx*3+x, by*3+y)
                            arr2 = self.searchColumn(values, bx*3+x, by*3+y)
                            if values[bx*3+x][by*3+y] == 0:
                                arr1 = self.searchRow(values, bx*3+x, by*3+y)
                                arr2 = self.searchColumn(values, bx*3+x, by*3+y)
                                if arr1[i] and arr2[i]:
                                    if is_first:
                                        first = [bx*3+x, by*3+y]
                                        is_first = False
                                    else:
                                        first[0] = -1
                    if is_first:
                        print("could not fit in box")
                        return
                    if first[0] != -1:
                        values[first[0]][first[1]] = i+1
                        self.changed = True

        return values

    def elimination(self, values):
        for i in range(3):
            for j in range(3):
                if values is None:
                    return
                values = self.boxElimination(values, i, j)
        return values

    def guessFirstRow(self, values):

        # get the row that will be guessed
        row = -1
        for i in range(9):
            for j in range(9):
                if values[i][j] == 0:
                    row = i
                    break
            if row != -1:
                break

        # find all permutations of first row
        possible = self.searchRow(values, row, 0)
        nums = []
        for i in range(9):
            if possible[i]:
                nums.append(i+1)

        permutations = self.buildPermutations(nums)

        ans = None
        for i in permutations:
            temp = self.guessFirstRowUtil(values, i, row)
            if temp is not None:
                self.printBoard(temp)
                ans = temp
        return ans

    def guessFirstRowUtil(self, values, fill, row):
        count = 0
        temp = copy.deepcopy(values)
        for i in range(9):
            if values[row][i] == 0:
                temp[row][i] = fill[count]
                count += 1

        self.changed = True
        while self.changed:
            self.changed = False
            temp = self.elimination(temp)
            if temp is None:
                return
        return temp

    def check_complete(self, values):
        for i in range(9):
            for j in range(9):
                if values[i][j] == 0:
                    return False
        return True

    # iterates solve_board until it is done, completes anything that can be done trivially

    def solveBoard(self, values):
        while self.changed:
            self.changed = False
            values = self.elimination(values)
            if values is None:
                return
        self.printBoard(values)
        print("INITIAL SOLUTION")
        values = self.guessFirstRow(values)
        return values

    # checks if a solution satisfies sudokus conditions

    def check_solution(self, values):
        if not self.check_complete(values):
            return False

        for i in range(9):
            nums = [0 for w in range(9)]
            for j in range(9):
                if nums[values[i][j]] == 1:
                    return False
                nums[values[i][j]] += 1

        for i in range(9):
            nums = [0 for w in range(9)]
            for j in range(9):
                if nums[values[j][i]] == 1:
                    return False
                nums[values[j][i]] += 1

        for i in range(3):
            for j in range(3):
                nums = [0 for w in range(9)]
                for x in range(3):
                    for y in range(3):
                        if nums[values[3*i+x][3*j+y]] == 1:
                            return False
                        nums[values[3*i+x][3*j+y]] += 1
        return True

    def countSolutions(self, possible):
        count = 0
        for i in range(9):
            if possible[i]:
                count += 1
        return count

    def findIndex(self, possible):
        for i in range(9):
            if possible[i]:
                return i


def main():
    # values = getValues()
    values = [[0, 0, 6, 0, 0, 0, 8, 0, 2],
              [7, 0, 0, 4, 2, 8, 0, 9, 6],
              [2, 1, 0, 0, 3, 0, 7, 0, 5],
              [0, 3, 1, 0, 0, 0, 9, 8, 0],
              [0, 0, 0, 1, 0, 0, 0, 0, 7],
              [8, 2, 0, 9, 5, 0, 0, 0, 3],
              [3, 0, 0, 0, 0, 2, 0, 6, 0],
              [0, 8, 5, 0, 7, 6, 0, 0, 0],
              [9, 0, 2, 5, 0, 1, 3, 0, 8]]
    s = Sudoku(values, True)
    s.printBoard(values)
    s.printBoard(s.solveBoard(values))


if __name__ == '__main__':
    main()
