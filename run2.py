import sys
import collections
import heapq

keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input():
    return [list(line.strip()) for line in sys.stdin]


def bfs_from(start, data):
    queue = collections.deque()
    visited = set()
    h, w = len(data), len(data[0])
    results = {}
    queue.append((start[0], start[1], 0, frozenset()))

    while queue:
        x, y, dist, doors = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        ch = data[x][y]
        if ch in keys_char:
            results[ch] = (dist, doors)
        elif ch in doors_char:
            doors = doors | {ch.lower()}

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and data[nx][ny] != '#':
                queue.append((nx, ny, dist + 1, doors))

    return results


def solve(data):
    h, w = len(data), len(data[0])
    total_keys = 0
    starts = []

    all_keys = {}
    for i in range(h):
        for j in range(w):
            ch = data[i][j]
            if ch == '@':
                starts.append((i, j))
            elif ch in keys_char:
                all_keys[ch] = (i, j)
                total_keys += 1

    positions = {}
    for idx, pos in enumerate(starts):
        positions[f'@{idx}'] = pos
    for key, pos in all_keys.items():
        positions[key] = pos

    graph = {}
    for label, pos in positions.items():
        graph[label] = bfs_from(pos, data)

    initial_state = (0, tuple(f'@{i}' for i in range(len(starts))), frozenset())
    visited = set()
    queue = [initial_state]

    while queue:
        steps, robots, keys = heapq.heappop(queue)
        state = (robots, keys)
        if state in visited:
            continue
        visited.add(state)

        if len(keys) == total_keys:
            return steps

        for i, robot in enumerate(robots):
            for target_key, (dist, required_keys) in graph[robot].items():
                if target_key not in keys and required_keys <= keys:
                    new_robots = list(robots)
                    new_robots[i] = target_key
                    new_keys = keys | {target_key}
                    heapq.heappush(queue, (steps + dist, tuple(new_robots), new_keys))

    return -1


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()
