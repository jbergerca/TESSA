import os

file = open("test1.txt", "r")
data = file.readlines()
file.close()

total = [i for i in range(len(data)) if (data[i] == '* **************************************************\n' and data[i - 1] == '\n')]
if (os.path.isdir("./pazdir") == False):
    os.mkdir("./pazdir")

name = []
for idx in total:
    net = data[idx + 1].split()[-1]
    stat = data[idx + 2].split()[-1]
    loc = data[idx + 3].split()[-1] if data[idx + 3].split()[-1] != ":" else ""
    chan = data[idx + 4].split()[-1]
    name.append(f"PZ_{net}_{stat}_{loc}_{chan}")

for i in range(len(total)):
    file = open(f"./pazdir/{name[i]}", "w")
    new = "".join(data[total[i]:total[i+1]]) if i != (len(total) - 1) else "".join(data[total[i]::])
    file.write(new)
    file.close()