import json


def check_capacity(capacity, guests):
    s = []
    for guest in guests:
        s.append((guest["check-in"], 1))
        s.append((guest["check-out"], -1))
    s.sort(key=lambda x: (x[0], x[1]))
    counter = 0
    for (date, delta) in s:
        counter += delta
        if counter > capacity:
            return False
    return True


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())


    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)


    result = check_capacity(max_capacity, guests)
    print(result)
