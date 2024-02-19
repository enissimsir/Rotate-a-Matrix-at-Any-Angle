import numpy as np
import math
import pandas as pd
import os
import matplotlib.pyplot as plt

you_want_it_to_be_mirrored = True

# CSV dosyasını oku ve verileri bir NumPy dizisine yükle
csv_path = '/home/enis/Downloads/rescalingscripts/csv/20230802-143330_t_4V8.csv'
with open(csv_path, 'r') as file:
    lines = file.readlines()
    data = [list(map(int, line.strip().split(';'))) for line in lines]


# Verileri kullanarak bir NumPy dizisi oluştur
csv = np.array(data)

#csv = np.ones((100,100))

rows, cols = csv.shape
print("cols, rows ",cols,rows)

mid_row = rows//2
mid_col = cols//2
print("midcol, midrow = ",mid_col,mid_row)
angle = 5
angle_in_radiant = math.radians(angle)
print("angle in radian = ", angle_in_radiant)

if angle < 0:
    col_size = int(math.cos(-angle_in_radiant) * cols + math.sin(-angle_in_radiant) * rows)
    row_size = int(math.sin(-angle_in_radiant) * cols + math.cos(-angle_in_radiant) * rows)
else:
    col_size = int(math.cos(angle_in_radiant) * cols + math.sin(angle_in_radiant) * rows)
    row_size = int(math.sin(angle_in_radiant) * cols + math.cos(angle_in_radiant) * rows)

#rotated = np.ones((row_size + 1, col_size + 1))

rotated = np.full((row_size+1, col_size+1), 10000)

print("col_size, row_size",col_size,row_size)


def calculate(row, col):
    y = row - mid_row
    x = col - mid_col
    z = math.sqrt(y * y + x * x)
#    print("x, y, z = ",x,y,z)
    beta = math.atan2(y, x) + angle_in_radiant
#    print("beta = ",beta)
    new_x = int(math.cos(beta) * z + mid_col)
    new_y = int(math.sin(beta) * z + mid_row)
#    print("new x and new y = ",new_x,new_y)
    return new_x, new_y

for row in range(rows):
    for col in range(cols):
     #   if csv[row][col] != 0:
    #    print("col: ",col,"row: ",row)
        x, y = calculate(row, col)
            
        rotated[y][x] = csv[row][col]
            #print("rotated[%d][%d] = ",y,x,rotated[y][x])
        #print()

for i in range(1, row_size):
    for j in range(1, col_size):
        if rotated[i][j] == 10000:
            if all(rotated[i + dx][j + dy] not in range(1, 5001) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]):
                rotated[i][j] = 0
            else:
                sum=0
                num=0
                if rotated[i-1][j] in range(1,5001):
                    sum+=rotated[i-1][j]
                    num+=1
                if rotated[i+1][j] in range(1,5001):
                    sum+=rotated[i+1][j]
                    num+=1
                if rotated[i][j-1] in range(1,5001):
                    sum+=rotated[i][j-1]
                    num+=1
                if rotated[i][j+1] in range(1,5001):
                    sum+=rotated[i][j+1]
                    num+=1
                rotated[i][j] = int(sum/num)

rotated[rotated == 10000] = 0

#Mirroring the matrix
if you_want_it_to_be_mirrored:
    rotated =np.fliplr(rotated)

plt.imshow(csv, cmap='viridis')  # Viridis is a color map
plt.colorbar()  # Renk ölçeği
plt.show()

plt.imshow(rotated, cmap='viridis')  # Viridis is a color map
plt.colorbar()  
plt.show()

#to name the file
seperated_string = csv_path.split("/")
file_name = seperated_string[-1]
file_name = "rotated_" + file_name

cwd = os.getcwd()
path = cwd + "/csv"


DF = pd.DataFrame(rotated)
DF = DF.astype(int)
DF.to_csv(os.path.join(path, file_name), header=None, index=None, sep=';')
print('rotated file saved!') 