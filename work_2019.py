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
i = 0
for v in list(range(a,b,1)):
    # Test length
    if len(str(v)) != 6:
        continue
    # Test within
    if v < a | v > b:
        continue
    # Test decreasing
    x = sorted([int(vi) for vi in str(v)])
    if "".join(str(s) for s in x) != str(v):
        continue
    # Test adjacent pair digits (at least one)
    yi = [(i, i + 1) for i in range(6 - 1)]
    y = [x[yi[i][0]]==x[yi[i][1]] for i in range(6-1)]
    if not y:
        continue
    # Else
    i+=1
# Return
print(f"Count numbers that match password criteria:{i}")

## Day 5
in5 = Path(os.path.join("2019","input","day5.txt")).read_text(encoding='utf-8')
