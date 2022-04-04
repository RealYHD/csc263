# Python code for problem set 1 question 1 part c.

# Import only "sys" and optionally "typing" packages.
# Output number of possible routes under a given scenario.
# python3 Routes.py inputfilepath
#     where input filepath represents the format use for board configurations desigaed in part b of question 1.

### Parse the input data ###

import string
import sys


def parse_input_list(filepath) -> tuple[list[list[int]], dict[str, int]]:
    headers = {}
    res = []
    file = open(filepath)
    lines_no_header = []

    header_ind = 0
    for line in file:
        if len(line) > 0 and not line.isspace():
            split = line.split(":")
            headers[split[0].strip()] = header_ind
            header_ind += 1
            # No case where there is no adjacent vertex (connected graph)
            lines_no_header.append(split[1])
    file.close()

    for line in lines_no_header:
        line = line.replace(",", " ")
        segmented = line.split(" ")
        row_items = []
        for segment in segmented:
            if not segment.isspace() and len(segment) > 0:
                row_items.append(headers[segment.strip().replace("\n", "")])
        if len(row_items) > 0:
            res.append(row_items)
    return res, headers


def parse_input_mat(filepath) -> tuple[list[list[int]], list[str]]:
    header = []
    mat = []
    file = open(filepath)
    colHeaderComplete = False
    num_verts = None
    for line in file:
        if (not line.startswith("#") and not line.isspace()):
            segments = line.split()
            row = []
            for segment in segments:
                if (segment.startswith("#")):
                    break  # the rest of the line is a comment.
                if (colHeaderComplete):
                    if segment.isnumeric():
                        row.append(int(segment))
                else:
                    row.append(segment.lower())
            if not colHeaderComplete:
                header = row
                colHeaderComplete = True
            else:
                mat.append(row)
            if not num_verts:
                num_verts = len(row)
            elif num_verts != len(row):
                return None
    file.close()
    return mat, header


def gen_city_mask(headers: dict) -> list:
    keys = headers.keys()
    res = [0] * len(keys)
    for key in keys:
        if "*" in key:
            res[headers[key]] = 1
    return res


def count_routes_1(adj_lst: list[list[int]], length: int, start, end) -> int:
    path = [0] * length
    return count_routes_visit_1(length, adj_lst, path, start, end, 0)


def count_routes_visit_1(length: int, adj: list[list[int]], path: list[int], curr_node: int, end_node: int, ends_found: int):
    if curr_node == end_node:
        return 1 + ends_found
    for dest_node in adj[curr_node]:
        if path[dest_node] < 1:
            # enter node
            path[curr_node] += 1
            ends_found = count_routes_visit_1(length, adj, path,
                                              dest_node, end_node, ends_found)
            path[curr_node] -= 1
    return 0 + ends_found


def count_routes_2(adj_lst: list[list[int]], length: int, start, end, city_mask: list) -> int:
    path = [0] * length
    return count_routes_visit_2(length, adj_lst, path, start, end, 0, city_mask)


def count_routes_visit_2(length: int, adj: list[list[int]], path: list[int], curr_node: int, end_node: int, ends_found: int, city_mask: list):
    if curr_node == end_node:
        return 1 + ends_found
    for dest_node in adj[curr_node]:
        if (path[dest_node] < 1 or city_mask[dest_node] > 0):
            # enter node
            path[curr_node] += 1
            ends_found = count_routes_visit_2(length, adj, path,
                                              dest_node, end_node, ends_found, city_mask)
            path[curr_node] -= 1
    return 0 + ends_found


def count_routes_3(adj_lst: list[list[int]], length: int, start, end, city_mask: list) -> int:
    path = [0] * length
    return count_routes_visit_3(length, adj_lst, path, start, start, end, 0, city_mask, False)


def count_routes_visit_3(length: int, adj: list[list[int]], path: list[int], curr_node: int, start_node: int, end_node: int, ends_found: int, city_mask: list, ticket_used: bool):
    if curr_node == end_node:
        return 1 + ends_found
    for dest_node in adj[curr_node]:
        if dest_node != start_node:
            if (path[dest_node] < 1 or city_mask[dest_node] > 0 or not ticket_used):
                handed_ticket = False
                if path[dest_node] > 0 and city_mask[dest_node] < 1:
                    ticket_used = True
                    handed_ticket = True
                # enter node
                path[curr_node] += 1
                ends_found = count_routes_visit_3(length, adj, path,
                                                  dest_node, start_node, end_node, ends_found, city_mask, ticket_used)
                if handed_ticket:
                    handed_ticket = False
                    ticket_used = False
                path[curr_node] -= 1
    return 0 + ends_found


if __name__ == "__main__":
    adj_lst, header = parse_input_list(sys.argv[1])
    if not adj_lst:
        print("There was an error trying to parse the given input file.")

    print("Scenario 1: {0}".format(count_routes_1(
        adj_lst, len(adj_lst), header["start"], header["end"])))

    city_mask = gen_city_mask(header)
    print("Scenario 2: {0}".format(count_routes_2(adj_lst, len(adj_lst),
          header["start"], header["end"], city_mask)))

    print("Scenario 3: {0}".format(count_routes_3(adj_lst, len(adj_lst),
          header["start"], header["end"], city_mask)))
