import os

day = os.path.basename(os.getcwd())

lines = open(f"{day}.in").read().splitlines()
    
directory_tree = {"/" : {}}
curr_dir = ["/"]

for line in lines:
    tokens = line.split()
    if tokens[0] == "$":
        if tokens[1] == "cd":
            location = tokens[2]
            if location == "..":
                curr_dir.pop()
            elif location == "/":
                curr_dir = ["/"]
            else:
                curr_dir.append(location)
    else:
        dir_or_size, name = tokens
        curr_tree = directory_tree
        for d in curr_dir:
            curr_tree = curr_tree[d]
        curr_tree[name] = {} if dir_or_size == "dir" else int(dir_or_size)

sizes = {}
def get_dir_size(tree, tot_dir="/"):
    size = 0
    for k, v in tree.items():
        if isinstance(v, dict):
            size += get_dir_size(tree[k], tot_dir=tot_dir+"/"+k)
        else:
            size += v
    sizes[tot_dir] = size
    return size

get_dir_size(directory_tree["/"])


part_1 = sum([v for _,v in sizes.items() if v < 100000])

currently_unused = 70000000 - sizes["/"]
needed = 30000000 - currently_unused
part_2 = [s for s in sorted(sizes.values()) if s > needed][0]


print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
