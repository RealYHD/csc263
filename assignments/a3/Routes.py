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
    for line in file:  # Generate the row headers first for substitution later.
        if len(line) > 0 and not line.isspace():
            split = line.split(":")
            # Indice for substitution later.
            headers[split[0].strip()] = header_ind
            header_ind += 1
            # No case where there is no adjacent vertex (connected graph)
            lines_no_header.append(split[1])
    file.close()

    for line in lines_no_header:
        # Ignore commas. They are for readability purposes only.
        line = line.replace(",", " ")
        segmented = line.split(" ")
        row_items = []
        for segment in segmented:
            if not segment.isspace() and len(segment) > 0:
                # Perform the substitution of labels with their indicies.
                row_items.append(headers[segment.strip().replace("\n", "")])
        # In case there was a line that was complete white-space.
        if len(row_items) > 0:
            res.append(row_items)
    return res, headers


# Generates an array of length n where n is the number of vertices in the graph.
def gen_city_mask(headers: dict) -> list:
    keys = headers.keys()
    res = [0] * len(keys)  # Prepare the array of length n
    for key in keys:
        if "*" in key:  # Use asterisk as notation for cities.
            # Set the index at the respective vertices to 1 if they are cities.
            res[headers[key]] = 1
    return res


def count_routes_1(adj_lst: list[list[int]], length: int, start, end) -> int:
    path = [0] * length
    return count_routes_visit_1(length, adj_lst, path, start, end, 0)


def count_routes_visit_1(length: int, adj: list[list[int]], path: list[int], curr_node: int, end_node: int, ends_found: int):
    if curr_node == end_node:  # If current node is the end port, count it.
        return 1 + ends_found
    # Iterate over the connected vertices of the current vertex.
    for dest_node in adj[curr_node]:
        # Check to see if this node has not been traversed on the path to the current node.
        if path[dest_node] < 1:
            # enter node
            # Indicate that the current node was used to traverse to the next node.
            path[curr_node] += 1
            ends_found = count_routes_visit_1(length, adj, path,
                                              dest_node, end_node, ends_found)  # Traverse to next node.
            # After returning, the current node is no longer an ancestor of the current node.
            path[curr_node] -= 1
    return 0 + ends_found  # Dead end, no way to get to the end port here.


def count_routes_2(adj_lst: list[list[int]], length: int, start, end, city_mask: list) -> int:
    path = [0] * length
    return count_routes_visit_2(length, adj_lst, path, start, end, 0, city_mask)


def count_routes_visit_2(length: int, adj: list[list[int]], path: list[int], curr_node: int, end_node: int, ends_found: int, city_mask: list):
    if curr_node == end_node:
        return 1 + ends_found
    for dest_node in adj[curr_node]:
        # Make exceptions to this check for city nodes.
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
            # Check the ticket hasn't been used yet. If so, then it may be used.
            if (path[dest_node] < 1 or city_mask[dest_node] > 0 or not ticket_used):
                handed_ticket = False
                if path[dest_node] > 0 and city_mask[dest_node] < 1:
                    ticket_used = True
                    # To indicate this was the call in the stack that used the ticket.
                    handed_ticket = True
                # enter node
                path[curr_node] += 1
                ends_found = count_routes_visit_3(length, adj, path,
                                                  dest_node, start_node, end_node, ends_found, city_mask, ticket_used)
                if handed_ticket:  # Check if we've returned to the stack at which we used our ticket, if so, that means we're done the route that used the ticket.
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
