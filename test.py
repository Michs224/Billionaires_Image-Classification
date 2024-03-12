import numpy as np
list=[1,2,3,5]

print(np.array(list).reshape(1,-1).shape)

import numpy as geek
 
#Working on 1D
arr = geek.arange(5)
print("1D arr : \n", arr)
print("Shape : ", arr.shape)
 
# value = 9
# index = 1   
# Insertion before first index
a = geek.insert(arr, 1, 9)
print("\nArray after insertion : ", a)
print("Shape : ", a.shape)
 
 
# Working on 2D array 
arr = geek.arange(12).reshape(3, 4)
print("\n\n2D arr : \n", arr)
print("Shape : ", arr.shape)
 
a = geek.insert(arr, 1, 9, axis = 1)
print("\nArray after insertion : \n", a)
print("Shape : ", a.shape)