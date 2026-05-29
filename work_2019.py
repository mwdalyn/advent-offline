'''Days 1-3 completed previously.'''
## Imports
import os
from pathlib import  Path

## Day 1 
# Input
in1 = Path(os.path.join("2019","input","day1.txt")).read_text(encoding='utf-8').split("\n")[:-1]
# Part 1
tank = 0
for m in in1:
    fuel = int(int(m) // 3) - 2 # int = rounddown
    tank += fuel
print(f"Module fuel requirement: {tank}") # Correct

# Part 2
# Incorrect (per intuition)
fuel_req = tank
tank_total = tank
while fuel_req > 0:
    fuel_add = fuel_req // 3 - 2
    print(f"Fuel add: {fuel_add}")
    if fuel_add <= 0:
        fuel_req = 0
        break
    tank_total += fuel_add
    fuel_req = fuel_add
    print(f"Fuel req: {fuel_req}")
# Correct (per instructions)
tank_total = 0
for m in in1:
    fuel_req = int(m) // 3 - 2
    while fuel_req > 0:
        tank_total += fuel_req
        fuel_req = fuel_req // 3 - 2
print(f"Resulting tank volume: {tank_total}") # Correct
# NOTE: This is an interesting one, and is 

## Day 2
# Part 1
# Input
in2 = Path(os.path.join("2019","input","day2.txt")).read_text(encoding='utf-8').replace("\n","").split(",")
in2 = [int(i) for i in in2]
# Instructions
in2[1] = 12
in2[2] = 2
# Processing: Grab opcode entries
operations = {1: lambda x, y: x + y, # Instruction : Calc of Parameter
              2: lambda x, y: x * y,
              99: None}
for i in list(range(0,len(in2),4)):
    print(f"Position {i}, Opcode {in2[i]}:")
    opcode = in2[i] 
    if opcode == 99:
        break
    operation = operations[opcode]
    pos_x, pos_y = in2[i+1], in2[i+2]
    x, y = in2[pos_x], in2[pos_y]
    value, pos = operation(x, y), in2[i+3]
    print(f"Calculate {pos_x} ({x}), {pos_y} ({y}) => ({value}) at {pos}.")
    in2[pos] = value
# Result
in2[0] # Correct

# Part 2
in2 = Path(os.path.join("2019","input","day2.txt")).read_text(encoding='utf-8').replace("\n","").split(",")
in2 = [int(i) for i in in2]
# Same operations instructions
operations = {1: lambda x, y: x + y, 
              2: lambda x, y: x * y,
              99: None}
def computer2(noun, verb, ruleset, input, read_interval=4):
    input_seq = input.copy()
    input_seq[1], input_seq[2] = noun, verb 
    for i in list(range(0, len(input_seq), read_interval)):
        opcode = input_seq[i]
        if opcode == 99:
            return input_seq[0]
        operation = ruleset[opcode] 
        pos_x, pos_y = input_seq[i+1], input_seq[i+2]
        x, y = input_seq[pos_x], input_seq[pos_y]
        value, pos = operation(x, y), input_seq[i+3]
        # print(f"Calculate {pos_x} ({x}), {pos_y} ({y}) => ({value}) at {pos}.")
        input_seq[pos] = value
    return input_seq[0]

# Test noun (in2[1]) and verb (in2[2]) pairs.
noun_sol, verb_sol = 0, 0
for n in range(100):
    for v in range(100):
        out_sol = computer2(n, v, operations, in2)
        if out_sol == 19690720:
            print(f"Found solution: (n, v) = ({n}, {v})")
            noun_sol, verb_sol = n, v
            found = True
            break
    if out_sol == 19690720:
        break
# Result
final_sol = 100* n + v
print(f"Day 2 Part 2 Solution: {final_sol}")

## Day 3
# Input
in3 = Path(os.path.join("2019","input","day3.txt")).read_text(encoding='utf-8')

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

opcodes = {3:'save at position',
          4:'output value',
          99:'halt'}

