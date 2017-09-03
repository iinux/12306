import random


def play():
    n = 3

    # 0 not excluded 2 excluded
    data = [0] * (n + 1)

    correct_pos = random.randint(1, n)
    select_pos = random.randint(1, n)
    exclude_num = n - 2
    i = 0
    while i < exclude_num:
        exclude_pos = random.randint(1, n)
        if exclude_pos == correct_pos:
            continue
        elif exclude_pos == select_pos:
            continue
        elif data[exclude_pos] == 2:
            continue
        else:
            data[exclude_pos] = 2
            i += 1

    target_pos = -1
    for i in range(1, n + 1):
        if data[i] == 0 and i != select_pos:
            target_pos = i

    if target_pos == -1:
        raise 'error'

    if target_pos == correct_pos:
        return True
    else:
        return False


play_times = 100
i = 0
change_win_times = 0
not_change_win_times = 0
while i < play_times:
    if play():
        change_win_times += 1
    else:
        not_change_win_times += 1
    i += 1

print ('change win times ' + str(change_win_times))
print ('not change win times ' + str(not_change_win_times))
print ('change win rate ' + str(change_win_times * 1.0 / play_times))
print ('not change win rate ' + str(not_change_win_times * 1.0 / play_times))
