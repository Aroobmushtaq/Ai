import numpy as np
# create a 1D array 
arr1=np.array([1,2,3,4,5])
print(arr1)
# create a 2D array
arr2=np.array([[1,2,3],[4,5,6]])
print(arr2)

# Display properties of the arrays
print(arr2.shape)  # Output: (2, 3) no. of rows and columns
print(arr2.ndim)   # Output: 2 no. of dimensions
print(arr2.size)   # Output: 6 total number of elements
print(arr2.dtype)  # Output: int64 data type of elements

# Genrating special arrays
print(np.zeros((2,3)))  # Creates a 2D array of zeros with shape (2, 3)
print(np.ones((2,3)))   # Creates a 2D array of ones with shape (2, 3)
print(np.eye(3))      # Creates a 2D identity matrix of shape (3, 3)
print(np.arange(0, 10, 2))  # Creates a 1D array with values from 0 to 10 with step of 2

#numpy operations
print(arr1 + 2)  # Adds 2 to each element of arr1
print(arr2 * 3) # Multiplies each element of arr2 by 3 
print(arr1 / 2)  # Divides each element of arr1 by 2
print(arr2 - 1)  # Subtracts 1 from each element of arr2

# statistical operations

print("mean:", np.mean(arr1))  # Calculates the mean of arr1
print("sum:", np.sum(arr2))    # Calculates the sum of all elements in arr2
print("max:", np.max(arr1)) # Finds the maximum value in arr1       
print("min:", np.min(arr2)) # Finds the minimum value in arr2
print("std:", np.std(arr1))  # Calculates the standard deviation of arr1
print("var:", np.var(arr2))  # Calculates the variance of arr2
print("median:", np.median(arr1))  # Calculates the median of arr1
