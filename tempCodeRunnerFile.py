def shift_floors(dic, start_floor=1, end_floor=6, rooms_per_floor=16):
    # 1. 先做原始快照（按楼层、按房间）
    snapshot = {}
    for floor in range(start_floor, end_floor + 1):
        floor_dict = {}
        for r in range(1, rooms_per_floor + 1):
            room_no = floor * 100 + r
            if room_no in dic:
                floor_dict[room_no] = list(dic[room_no])  # 拷贝列表
        snapshot[floor] = floor_dict

    # 2. 从高楼层往下回填，避免链式污染
    for floor in range(end_floor, start_floor, -1):  # end_floor, ..., start_floor+1
        src_floor = floor - 1
        if src_floor not in snapshot:
            continue
        for r in range(1, rooms_per_floor + 1):
            src_room = src_floor * 100 + r
            dst_room = floor * 100 + r
            if src_room in snapshot[src_floor]:
                dic[dst_room] = list(snapshot[src_floor][src_room])  # 独立列表
    return dic
