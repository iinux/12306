import time

import train

if __name__ == '__main__':
    r = train.TrainInfoRequest()
    date_var = '2024-02-07'
    date_var = '2024-01-29'
    train_no = '240000G33505'
    seat_var = '二等座'
    station_list = r.query_by_train_no(train_no, 'HPP', 'WHN', date_var)
    print(station_list)
    pairs = []
    for i in range(len(station_list) - 1):
        for j in range(i + 1, len(station_list)):
            pairs.append((station_list[i], station_list[j]))
    print(pairs)
    print(len(pairs))
    for pair in pairs:
        all_train_info = r.get_result(date_var, pair[0], pair[1])
        for train_info in all_train_info:
            if train_info.get_train_no() == train_no:
                print('%s -> %s %s %s' % (pair[0], pair[1], seat_var,
                                              train_info.get_seat_number(seat_var)))
        time.sleep(1)


