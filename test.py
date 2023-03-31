save_file = open("src/saves/save_file.txt", "r")

save_arr = [line for line in save_file]

# save_arr = []

# with open('src/saves/save_file.txt') as topo_file:
#     for line in topo_file:
#         save_arr += line,

print(save_arr)