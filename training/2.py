import sys

nums = [int(n) for n in sys.argv[1]]
print('\n')
def determine_offset(index):
    if index + int((len(nums)/2)) > len(nums)-1:
        new = nums[index + int(len(nums)/2) - len(nums)]
    else:
        new = nums[index + int(len(nums)/2)]
    return new

i = 0
total = 0
for num in nums:
   if num == determine_offset(i):
       total += num
   i += 1
print(total)
