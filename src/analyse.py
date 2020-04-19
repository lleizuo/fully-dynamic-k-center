f = open("output", "r")
line = f.readline()
line = f.readline()
cummu = 0
count = 0
while line:
    stab = float(line.split(":")[1])
    cummu += stab
    count += 1
    line = f.readline()
    line = f.readline()
# print(cummu/count)
print("Number of center deletion: %d, Average stability: %.8f" % (count, cummu/count))
f.close()