def index_valid(row, col, r_count, c_count):
    return 0 <= row < r_count and 0 <= col < c_count


# Finds all adjacent cells of the color.
# Returns a set of tuples (coordinates of the cells) including current cell.
def adjacent_cells(r, c, matrix, r_count, c_count, color):
    adj_cells = [(r, c)]
    if index_valid(r, c + 1, r_count, c_count) and matrix[r][c + 1] == color:
        adj_cells.append((r, c + 1))
    if index_valid(r + 1, c, r_count, c_count) and matrix[r + 1][c] == color:
        adj_cells.append((r + 1, c))
    if index_valid(r, c - 1, r_count, c_count) and matrix[r][c - 1] == color:
        adj_cells.append((r, c - 1))
    if index_valid(r - 1, c, r_count, c_count) and matrix[r - 1][c] == color:
        adj_cells.append((r - 1, c))
    return set(adj_cells)


# Appends a new set of tuples of adjacent coordinates
# if intersection with any other set makes union with the set.
def append_combine_sets(list_of_sets, set_of_adj_coordinates):
    if len(list_of_sets) == 0:
        list_of_sets.append(set_of_adj_coordinates)
    else:
        for i in range(len(list_of_sets)):
            if not list_of_sets[i].isdisjoint(set_of_adj_coordinates):
                list_of_sets[i] = list_of_sets[i].union(set_of_adj_coordinates)
                break
            else:
                list_of_sets.append(set_of_adj_coordinates)
    return list_of_sets


# Sort a list of sets in descending order.
# Pop shortest set and check if any intersection with another set then make union
# Do this until only the longest set remains in the list
def shorten_list(list_of_sets):
    while True:
        if len(list_of_sets) == 1 or len(list_of_sets) == 0:
            break
        list_of_sets.sort(key=lambda x: len(x), reverse=True)
        last_set = list_of_sets.pop()
        for i in range(len(list_of_sets)):
            if not list_of_sets[i].isdisjoint(last_set):
                list_of_sets[i] = list_of_sets[i].union(last_set)
    return list_of_sets


# returns length of first element of the list of sets (if there is one)
def get_length(color_list):
    if len(color_list) == 0:
        return 1
    return len(color_list[0])


test_path = "..\\tests\\test_2"
test = open(test_path, "r")

rows_count, columns_count = [int(x) for x in test.readline().split()]

matrix = []

while True:
    line = test.readline()
    if not line:
        break
    matrix.append([x for x in line.split()])

test.close()

reds = []
greens = []
blues = []

for r in range(rows_count):
    for c in range(columns_count):
        current_color = matrix[r][c]
        adj_cells = adjacent_cells(r, c, matrix, rows_count, columns_count, current_color)
        if len(adj_cells) == 1:
            continue
        if current_color == "R":
            reds = append_combine_sets(reds, adj_cells)
        elif current_color == "G":
            greens = append_combine_sets(greens, adj_cells)
        elif current_color == "B":
            blues = append_combine_sets(blues, adj_cells)

reds = shorten_list(reds)
greens = shorten_list(greens)
blues = shorten_list(blues)

longest = max(get_length(reds), get_length(greens), get_length(blues))
print(longest)
