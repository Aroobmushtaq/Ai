import numpy as np
import matplotlib.pyplot as plt
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


# indexing and slicing
print(arr2[0, 1])  # Accesses the element at row 0, column 1 of arr2
print(arr2[1, :])  # Accesses the entire second row of arr2
print(arr2[:, 1])   # Accesses the entire second column of arr2
print(arr2[0:2, 1:3])  # Slices arr2 to get a sub-array from rows 0 to 1 and columns 1 to 2

# rendom number generation
print(np.random.rand(2, 3))  # Generates a 2D array of shape (2, 3) with random numbers from a uniform distribution over [0.0, 1.0)
print(np.random.randint(0, 10, (2, 3))) # Generates a 2D array of shape (2, 3) with random integers between 0 and 10

# Stock Price Simulation (Monte Carlo)
np.random.seed(0)
days = 365
initial_price = 100
returns = np.random.normal(0, 1, days)
prices = initial_price * np.cumprod(1 + returns / 100)

import matplotlib.pyplot as plt
plt.plot(prices)
plt.title("Simulated Stock Prices")
plt.show()