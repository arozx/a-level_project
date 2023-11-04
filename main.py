import svgwrite

class Board:
    def __init__(self):
        self.board=[[None for i in range(8)] for j in range(8)]
        self.board[0][0]="R"
        self.board[0][1]="N"

    def move_svg_right(path_data):
        new_path_data = ""
        for command in path_data.split(" "):
            if command.startswith("M") or command.startswith("L"):
                x, y = command[1:].split(",")
                x = str(float(x) + 100)
                new_path_data += f"{command[0]}{x},{y} "
            else:
                new_path_data += command + " "
        return new_path_data.strip()

    def printBoard(self, type):
        if type=="ascii":
            for i in range(8):
                print(self.board[i])
        elif type=="svg":

            # Create board
            board=Board()

            boardSVG=svgwrite.Drawing(filename="board.svg",size=(800,800))
            boardSVG.add(boardSVG.rect(insert=(0,0),size=(800,800),fill="white"))

            # draw svg
            for i in range(8):
                for j in range(8):

                    # draw squares
                    if (i+j)%2==0:
                        boardSVG.add(boardSVG.rect(insert=(i*100,j*100),size=(100,100),fill="black"))
                    else:
                        boardSVG.add(boardSVG.rect(insert=(i*100,j*100),size=(100,100),fill="white"))

                    match (self.board[i][j]):
                        case "R":
                            # get the path of the image file and add it to the svg
                            path_data = [
                                "M 20,88 L 80,88 L 80,80 L 20,80 L 20,88 z ",
                                "M 27.8,71.1 L 31.1,65.6 L 68.9,65.6 L 72.2,71.1 L 27.8,71.1 z ",
                                "M 22.2,80 L 22.2,71.1 L 73.3,71.1 L 73.3,80 L 22.2,80 z ",
                                "M 31.1,65.6 L 31.1,36.7 L 68.9,36.7 L 68.9,65.6 L 31.1,65.6 z ",
                                "M 31.1,36.7 L 24.4,31.1 L 77.8,31.1 L 68.9,36.7 L 31.1,36.7 z "
                                "M 24.4,31.1 L 24.4,20 L 33.3,20 L 33.3,22.2 L 44.4,22.2 L 44.4,20 L 55.6,20 L 55.6,22.2 L 66.7,22.2 L 66.7,20 L 75.6,20 L 75.6,31.1 L 24.4,31.1 z ",
                                "M 22.2,78.9 L 73.3,78.9 L 73.3,78.9",
                                "M 25.6,70 L 71.1,70",
                                "M 31.1,65.6 L 68.9,65.6",
                                "M 31.1,36.7 L 68.9,36.7",
                                "M 24.4,31.1 L 77.8,31.1"
                            ]

                            for x in path_data:
                                boardSVG.add(boardSVG.path(d=path_data, fill="red"))  

                        case "N":
                            path_data = [
                                "M 20,88 L 80,88 L 80,80 L 20,80 L 20,88 z ",
                                "M 27.8,71.1 L 31.1,65.6 L 68.9,65.6 L 72.2,71.1 L 27.8,71.1 z ",
                                "M 22.2,80 L 22.2,71.1 L 73.3,71.1 L 73.3,80 L 22.2,80 z ",
                                "M 31.1,65.6 L 31.1,36.7 L 68.9,36.7 L 68.9,65.6 L 31.1,65.6 z ",
                                "M 31.1,36.7 L 24.4,31.1 L 77.8,31.1 L 68.9,36.7 L 31.1,36.7 z ",
                                "M 24.4,31.1 L 24.4,20 L 33.3,20 L 33.3,22.2 L 44.4,22.2 L 44.4,20 L 55.6,20 L 55.6,22.2 L 66.7,22.2 L 66.7,20 L 75.6,20 L 75.6,31.1 L 24.4,31.1 z ",
                                "M 22.2,78.9 L 73.3,78.9 L 73.3,78.9",
                                "M 25.6,70 L 71.1,70",
                                "M 31.1,65.6 L 68.9,65.6",
                                "M 31.1,36.7 L 68.9,36.7",
                                "M 24.4,31.1 L 77.8,31.1"
                            ]
                            path_data = board.move_svg_right(path_data)
                            for x in path_data:
                                boardSVG.add(boardSVG.path(d=path_data, fill="red"))
                        case "B":
                            pass
                        case "Q":
                            pass
                        case "K":
                            pass
                        case "P":
                            pass
            # wrtie to file
            boardSVG.save(pretty=True)
