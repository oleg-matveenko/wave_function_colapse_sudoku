
const_SQ_SIZE = 3

class Board_itterator:
    def __init__(self, cell, board):
        self.cell = cell
        self.board = board
        self.x = self.y = 0
        self.corner_x = self.sqx = (cell[0] // const_SQ_SIZE) * const_SQ_SIZE
        self.corner_y = self.sqy = (cell[1] // const_SQ_SIZE) * const_SQ_SIZE
       
    def __iter__(self):
        return self
    def __next__(self):
        if self.x < len(self.board):
            self.x += 1
            return (self.x-1,self.cell[1])

        if self.y < len(self.board[self.cell[0]]):
            self.y += 1
            return (self.cell[0],self.y-1)
           
        if self.sqx < self.corner_x + const_SQ_SIZE:
            self.sqx += 1
            return (self.sqx-1,self.sqy)
        else:
            self.sqx = self.corner_x
            if self.sqy < self.corner_y:
                self.sqy += 1
                return (self.sqx,self.sqy)
        raise StopIteration


class Board:
    def calculate_cell_entropy(self,cell):
        entropy = [i+1 for i in range(len(self.board))]
        it = Board_itterator(cell,self.board)
        for i in it:
            if self.board[i[0]][i[1]] in entropy:
                entropy.remove(self.board[i[0]][i[1]])
        return entropy

    def populate_cells_entropy(self):
        res = {}
        cells = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if not self.board[i][j]:
                    cells.append((i,j))
               
        for cell in cells:
            res[cell] = self.calculate_cell_entropy(cell)
        return res
           
    def __init__(self, board):
        self.board = board
        self.cell_entropy = self.populate_cells_entropy()
       
    def step(self):
        min_value = min(self.cell_entropy.values(),key=len)
        min_index = None
        for i in self.cell_entropy:
            if self.cell_entropy[i]==min_value:
                min_index = i
                break
        #this would be where we have to potentially backtrack
        self.board[min_index[0]][min_index[1]] = min_value[0]
        del self.cell_entropy[min_index]
        it = Board_itterator(min_index,self.board)
        for i in it:
            if i in self.cell_entropy and min_value[0] in self.cell_entropy[i]:
                self.cell_entropy[i].remove(min_value[0])
               
    def print_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]:
                    print(self.board[i][j],end=' ')
                else:
                    print(u'\u25A1',end=' ')
            print('\n',end='')
        print('\n',end='')
       


b = [[4,3,None,None], [1,2,3,None], [None,None,2,None], [2,1,None,None]]
b2 = [  [5,None,None,None,1,None,None,None,4],
        [2,7,4,None,None,None,6,None,None],
        [None,8,None,9,None,4,None,None,None],
        [8,1,None,4,6,None,3,None,2],
        [None,None,2,None,3,None,1,None,None],
        [7,None,6,None,9,1,None,5,8],
        [None,None,None,5,None,3,None,1,None],
        [None,None,5,None,None,None,9,2,7],
        [1,None,None,None,2,None,None,None,3],]
board = Board(b2)
board.print_board()
while board.cell_entropy:
    board.step()
board.print_board()
