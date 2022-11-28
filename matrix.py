#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#SR6


from array import array

class Matrix(object):

    def __init__(self, matrix: array):
        self.matrix = matrix

    def __matmul__(self, other):
        length_x = len(self.matrix)
        length_y = len(self.matrix[0])

        if(type(other.matrix[0]) == list):
            length_other = len(other.matrix[0])
        else:
            length_other = 1

        matrix_result = []

        for i in range(length_x):
            matrix_result.append([])
            for j in range(length_other):
                matrix_result[i].append(0)

        if(type(other.matrix[0]) == list):
            for i in range(length_x):
                for j in range(length_other):
                    for k in range(length_y):
                        matrix_result[i][j] += self.matrix[i][k] * other.matrix[k][j]
        else:
            for i in range(length_x):
                for j in range(length_other):
                    for k in range(length_y):
                        matrix_result[i][j] += self.matrix[i][k] * other.matrix[k]

        
        return Matrix(matrix_result)