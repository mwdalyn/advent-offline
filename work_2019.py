'''Days 1-3 completed previously.'''
## Imports
import os
from pathlib import  Path

## Day 4
# Open
with open(os.path.join("2019","input","day4.txt"), 'r', encoding='utf-8') as file:
    in4 = file.read()
# Alternative
in4 = Path(os.path.join("2019","input","day4.txt")).read_text(encoding='utf-8')
# Processing
a, b = [int(v) for v in in4.split("-")] # in4[0], in4[-1]
sol4 = 0
sols = []
for v in list(range(a,b,1)):
    # Test length
    if len(str(v)) != 6:
        continue
    # Test within
    if v < a or v > b:
        continue
    # Test decreasing
    x = sorted([int(vi) for vi in str(v)])
    if "".join(str(s) for s in x) != str(v):
        continue
    # Test adjacent pair digits (at least one)
    yi = [(i, i + 1) for i in range(6 - 1)]
    y = [str(v)[yi[i][0]]==str(v)[yi[i][1]] for i in range(6-1)]
    if not any(y):
        continue
    # Else
    sol4+=1
    sols.append(v)
# Return
print(f"Count numbers that match password criteria:{sol4}")
# NOTE: Interesting lesson: use of "|" instead of "or" was skipping correct values, and must use not any(y) instead of not y.

## Day 5
in5 = Path(os.path.join("2019","input","day5.txt")).read_text(encoding='utf-8').replace("\n","").split(",")

