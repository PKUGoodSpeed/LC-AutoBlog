### idea
- Loop through the array:
- Put the encountered numbers in to a map, mapping from number value to index.
- If at a particular senario, the encountered number is `x`, and `target - x` is already in the map.
- Which means the indices of `target-x` and `x` will be the solution.
- If no such senario appears, definitely there is no solution.

### Psudocode
```
pos := map[int->int]
for i:= range(nums):
    if target - nums[i] in pos:
        return pos[target-nums[i], i
    else:
        pos[nums[i]] = i
no solution return -1, -1
```