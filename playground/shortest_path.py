import RNA


def get_shortest_path(ss, target, end_position=None):
    # get end_position
    if end_position is None:
        if ss[-1] != '.':
            end_position = len(ss) - 1
        else:
            for i in range(len(ss) - 1, -1, -1):
                if ss[i] != '.':
                    end_position = i + 1
                    break
    if end_position < target:
        raise IndexError("target out of range")
    pt = RNA.ptable(ss)
    total_length = {}
    for i in range(len(ss) - 1, -1, -1):
        if ss[i] == '.' and i == 0:
            return None
        if ss[i] == '.':
            pass
        elif ss[i] != '.':
            enter_1 = i
            enter_2 = pt[i + 1] - 1
            total_length = {1: end_position + 1 - i, 2: end_position - i + 2}
            if enter_1 <= target <= end_position:
                return end_position - target + 1
            elif target == enter_2:
                return end_position - enter_1 + 2
            else:
                break
    state = 1
    temp_enter_1 = enter_1
    while state:
        state, temp_dict, temp_exit_1, temp_exit_2 = straight_path(ss, temp_enter_1, pt, target)
        if state == 0:
            total_length[1] += temp_dict[1]
            total_length[2] += temp_dict[2]
            return min(total_length[1], total_length[2])
        elif state == 1:
            total_length[1] = min(total_length[1] + temp_dict[(1, 1)], total_length[2] + temp_dict[(2, 1)])
            total_length[2] = min(total_length[1] + temp_dict[(1, 2)], total_length[2] + temp_dict[(2, 2)])
            temp_enter_1 = temp_exit_1
            state, temp_dict, temp_exit_1, temp_exit_2 = circle_path(ss, temp_enter_1, pt, target)
            if state == 0:
                total_length[1] += temp_dict[1]
                total_length[2] += temp_dict[2]
                return min(total_length[1], total_length[2])
            elif state == 1:
                temp_enter_1 = temp_exit_1
                total_length[1] = min(total_length[1] + temp_dict[(1, 1)], total_length[2] + temp_dict[(2, 1)])
                total_length[2] = min(total_length[1] + temp_dict[(1, 2)], total_length[2] + temp_dict[(2, 2)])
            elif state == 2:
                total_length[1] += 1
                total_length[2] += 0
                state, length, temp_exit_1, temp_exit_2 = free_path(ss, temp_exit_1, pt, target)
                if state == 0:
                    total_length[1] += length
                    total_length[2] += length
                    return min(total_length[1], total_length[2])
                elif state == 1:
                    temp_enter_1 = temp_exit_1
                    total_length[1] += length
                    total_length[2] += length
        elif state == 2:
            total_length[1] += 1
            total_length[2] += 0
            state, length, temp_exit_1, temp_exit_2 = free_path(ss, temp_exit_1, pt, target)
            if state == 0:
                total_length[1] += length
                total_length[2] += length
                return min(total_length[1], total_length[2])
            elif state == 1:
                temp_enter_1 = temp_exit_1
                total_length[1] += length
                total_length[2] += length

    return None


def circle_path(ss, enter_1, pt, target):
    if pt[enter_1 + 1] - 1 > target:
        return 2, 1, pt[enter_1 + 1] - 1, None
    circle_fragments = get_circle_fragments(ss, enter_1, pt)
    right_length = 0
    left_length = 0
    if any(fragment[0] <= target <= fragment[1] for fragment in circle_fragments):
        # the target is on the circle
        for fragment in circle_fragments:
            if fragment[0] <= target <= fragment[1]:
                right_length += fragment[1] - target
            if fragment[0] > target:
                right_length += fragment[1] - fragment[0] + 1
        for fragment in circle_fragments:
            if fragment[0] <= target <= fragment[1]:
                left_length += target - fragment[0]
            if fragment[1] < target:
                left_length += fragment[1] - fragment[0] + 1
        return 0, {1: min(right_length, left_length + 1), 2: min(left_length, right_length + 1)}, None, None
        # 0 represents target on circle
    else:
        # the target is not on the circle
        for i in range(len(circle_fragments)):
            if circle_fragments[i][1] < target < circle_fragments[i + 1][0]:
                for j in range(0, i + 1):
                    left_length += circle_fragments[j][1] - circle_fragments[j][0] + 1
                for j in range(i + 1, len(circle_fragments)):
                    right_length += circle_fragments[j][1] - circle_fragments[j][0] + 1
                left_length -= 1
                right_length -= 1
                exit_1 = circle_fragments[i + 1][0]
                exit_2 = circle_fragments[i][1]
                length_dict = {(1, 1): min(right_length, left_length + 2),
                               (2, 2): min(left_length, right_length + 2),
                               (1, 2): min(right_length + 1, left_length + 1),
                               (2, 1): min(left_length + 1, right_length + 1)}
                return 1, length_dict, exit_1, exit_2


def get_circle_fragments(ss, enter_1, pt):
    scanning_position = enter_1 - 1
    circle_fragments = []
    temp = None
    while True:
        while ss[scanning_position] == '.':
            scanning_position = scanning_position - 1
        if enter_1 == pt[scanning_position + 1] - 1:
            if temp is None:
                circle_fragments.append((pt[enter_1 + 1] - 1, enter_1))
            else:
                circle_fragments.append((pt[enter_1 + 1] - 1, temp))
            break
        else:
            if temp is None:
                circle_fragments.append((scanning_position, enter_1))
            else:
                circle_fragments.append((scanning_position, temp))
            temp = pt[scanning_position + 1] - 1
            scanning_position = pt[scanning_position + 1] - 2
    return sorted(circle_fragments)

def straight_path(ss, enter_1, pt, target):
    scanning_position = enter_1
    enter_2 = pt[enter_1 + 1] - 1
    scanning_position_2 = enter_2
    while ss[scanning_position] == ')' and ss[scanning_position_2] == '(':
        scanning_position -= 1
        scanning_position_2 += 1
    exit_1 = scanning_position + 1
    exit_2 = pt[scanning_position + 2] - 1

    if exit_1 <= target <= enter_1:
        return 0, {1: enter_1 - target, 2: enter_1 - target + 1}, None, None
    elif enter_2 <= target <= exit_2:
        return 0, {1: target - enter_2 + 1, 2: target - enter_2}, None, None
    elif target < enter_2:
        return 2, 1, enter_2, None
    else:
        length_dict = {(1, 1): enter_1 - exit_1,
                       (2, 2): enter_1 - exit_1,
                       (1, 2): enter_1 - exit_1 + 1,
                       (2, 1): enter_1 - exit_1 + 1}
        return 1, length_dict, exit_1, exit_2


def free_path(ss, enter, pt, target):
    scanning_position = enter - 1
    while ss[scanning_position] == '.' and scanning_position > 0:
        scanning_position = scanning_position - 1
    exit_1 = scanning_position
    if exit_1 <= target <= enter:
        return 0, enter - target, None, None
    if target < exit_1:
        return 1, enter - exit_1, exit_1, None
