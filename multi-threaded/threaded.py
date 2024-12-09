import os
import random
import threading
import time


#! FUNCTIONS
def printMatrix(M, n):
    print(
        "==========================================================================================================================="
    )
    for i in range(n):
        for j in range(n):
            print(M[i][j], end="\t")
        print()
    print(
        "==========================================================================================================================="
    )


def randomizeDivisible(M, n):
    # randomize values of all divisible by 10
    for row in range(n):
        for col in range(n):
            if (row % 10 == 0) and (col % 10 == 0):
                M[row][col] = float(random.randint(1, 1000))

    return M


def terrain_inter_row(M, n, row):
    for index in range(n):
        if M[row][index] == 0:
            x = index  # provide x based on the x-coordinate

            # apply the formula for FCC
            M[row][index] = round((y1 + ((x - x1) / (x2 - x1)) * (y2 - y1)), 2)
        else:
            # print(index, "index")
            x1 = index
            x2 = index + 10

            try:
                y1 = M[row][x1]
                y2 = M[row][x2]
            except:
                pass


def terrain_inter_col(M, n, col):
    for index in range(n):
        if M[index][col] == 0:
            x = index
            M[index][col] = round((y1 + ((x - x1) / (x2 - x1)) * (y2 - y1)), 2)

        else:
            x1 = index
            x2 = index + 10

            try:
                y1 = M[x1][col]
                y2 = M[x2][col]
            except:
                pass

    return M


def elevate(M, n, index, index2):
    print(f"Divided matrix {index} to {index2-1}")
    print(
        "==========================================================================================================================="
    )

    for row in range(index, index2):
        terrain_inter_row(M, n, row)

    for i in range(index, index2):
        for j in range(n):
            print(M[i][j], end="\t")
        print()
    print(
        "==========================================================================================================================="
    )
    print()


#! MAIN
if __name__ == "__main__":
    os.system("clear")

    # user input
    n = int(input("Input: ")) + 1
    t = int(input("Number of submatrices: "))

    # matrix
    M = [[0 for column in range(n)] for row in range(n)]
    M = randomizeDivisible(M, n)

    print("Randomized Matrix")
    printMatrix(M, n)
    print()

    #! FCC
    # calculate
    time_before = time.time()

    # fill the columns whose rows are divisible by 10
    col = 0
    while col < n:
        M = terrain_inter_col(M, n, col)
        col += 10

    print("1st and Last Columns")
    printMatrix(M, n)
    print()

    # printMatrix(M, n)
    # print()

    #! get submatrices (per row)

    num_per_group = n // t
    remainder = n % t
    elements = [num_per_group] * t

    # Distribute the remainder evenly
    for i in range(remainder):
        elements[i] += 1

    # print(elements)

    # put into a list the starting indexes of the submatrices
    start_index = 0
    start_list = [0]  # starting will always be 0th index
    for item in range(len(elements) - 1):
        start_list.append(start_index + elements[item])
        start_index += elements[item]

    threads = []

    for i in range(t):
        index = start_list[i]
        if i == t - 1:  # last row
            index2 = n
        else:
            index2 = start_list[i + 1]

        my_thread = threading.Thread(
            target=elevate,
            args=(
                M,
                n,
                index,
                index2,
            ),
        )
        threads.append(my_thread)

    for p in threads:
        p.start()

    for p in threads:
        p.join()

    time_elapsed = time.time() - time_before

    print("time elapsed:", time_elapsed)
