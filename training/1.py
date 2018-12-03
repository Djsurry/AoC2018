import sys

pinput = [int(n) for n in sys.argv[1]]
last = len(pinput) -1
total = 0
index = 0
for num in pinput:
    if index == last:
        if num == pinput[-1]:
            total += num
    elif num == pinput[index + 1]:
        total += num
    index += 1
print(total)
