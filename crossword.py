from collections import Counter
import json

def clue(wordle, user_input):
    # https://stackoverflow.com/questions/76450068/how-to-handle-duplicate-letters-in-wordle
    # white, yellow, green
    # clue(solution, guess)
    feedback = ["W"] * len(wordle)
    seen_counter = Counter()

    # finding the right letters in their places
    for i in range(len(wordle)):
        if user_input[i] == wordle[i]:
            feedback[i] = "G"
            seen_counter[user_input[i]] += 1

    # search for existing letters that are out of place
    for i in range(len(wordle)):
        if feedback[i] == "G":
            continue
        elif user_input[i] in wordle and seen_counter[user_input[i]] < wordle.count(user_input[i]):
            feedback[i] = "Y"
            seen_counter[user_input[i]] += 1

    return feedback

with open("CSW24.txt","r") as infile:
    raw_input = infile.readlines()
    data = [datum.strip('\n').lower() for datum in raw_input]

#grid = ["scuff", "tamil", "repay", "using", "narco", "green"]  # horizontal here
#grid = ["avila", "bodes", "allah", "steve", "essen"]
grid = ["stair", "prune", "eaten", "adopt", "rests"]

def switch(L):
    return ["".join([L[n][m] for n in range(len(L))]) for m in range(len(L[0]))]

def generate(grid, name):
    colouring = {}
    comp = len(grid[0])

    for i in data:
        if len(i) != comp:
            continue
        if i not in grid:
            colours = ""
            for j in grid:
                colours += "".join(clue(i, j)) + "\n"
            colours = colours[:-1]
            if colours in colouring:
                colouring[colours].append(i)
            else:
                colouring[colours] = [i]
        #print(i)

    with open(f"{name}.json", 'w') as info:
        json.dump(colouring, info, indent=4, sort_keys=True)

    return colouring

colour_h = generate(grid, "h")
'''
# below is single plusword. use switch(grid) for the vertical version
for k, v in colour_h.items():
    if len(v) == 1:
        print(f"FOUND: {v[0]}")
'''
        
# comment out below if you do not want double plusword
colour_v = generate(switch(grid), "v")
print("-"*31)

for k, v in colour_h.items():
    if len(v) == 1:
        s = switch(k.split("\n"))
        u = "\n".join(s)
        if u in colour_v.keys():
            t = colour_v[u]
            if len(t) == 1:
                print(f"FOUND: {v[0]} {t[0]}")
