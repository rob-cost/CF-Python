import os

numbers = [str(numb) for numb in range(50, 101)]
numbers = [n + "\n" for n in numbers]

print(numbers)
print(os.getcwd())
