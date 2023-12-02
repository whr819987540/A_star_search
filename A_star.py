import torch

start = torch.tensor([0, 5], dtype=torch.long)
end = torch.tensor([6, 9], dtype=torch.long)
map = torch.zeros((end[0]+1, end[1]+1), dtype=torch.int)
map[4, 3:] = 1
print(map)


def h(point: torch.Tensor):
    return torch.abs(point-end).sum()

def g(dis: int):
    return dis + 1

class Array:
    def __init__(self, data: list) -> None:
        self.data = data

    def empty(self):
        return self.len() == 0

    def len(self):
        return len(self.data)

    def pop_min(self):
        if self.empty():
            return None
        else:
            return self.data.pop(0)

    def put(self, x: dict):
        index = -1
        for i in range(self.len()):
            if self.data[i]["f"] >= x["f"]:
                index = i
                break
        if index == -1:
            index = self.len()
        self.data.insert(index, x)

    def find(self, x: torch.Tensor):
        for data in self.data:
            if torch.equal(x, data["point"]):
                return data
        return None

    def remove(self, x: torch.Tensor):
        for i in range(self.len()):
            if torch.equal(self.data[i]["point"], x):
                self.data.pop(i)
                break

    def __str__(self) -> str:
        return str(self.data)


def is_goal(x: dict):
    return torch.equal(x["point"], end)

def print_path(point: torch.Tensor, close: Array):
    s = []
    while point is not None:
        s.append(f"({point[0]}, {point[1]})")
        point = close.find(point)["parent"]
    s.reverse()
    return "=>".join(s)

def cross_the_line(x: torch.Tensor, map: torch.Tensor):
    if x[0] < 0 or x[0] > map.shape[0]-1:
        return True
    if x[1] < 0 or x[1] > map.shape[1]-1:
        return True
    return False


# 上下左右，g(n)都只会增加1
open = Array([{"point": start, "f": 0+h(start), "g": torch.tensor(0), "h": h(start), "parent": None}])
close = Array([])
print(open, close)
while True:
    if open.empty():
        print("Path Not Found.")
        break
    next = open.pop_min()
    print(f"next:{next}")
    close.put(next)
    if is_goal(next):
        print(f"Find Goal! Path is: {print_path(next['point'],close)}.")
        break
    # 上下左右移动
    for i in [0, 1]:
        for j in [-1, 1]:
            dst = next["point"] + torch.tensor([(1-i)*j, i*j], dtype=torch.long)
            # 越界
            if cross_the_line(dst, map):
                continue
            dst_f = next["g"]+1+h(dst)
            # 障碍物
            if map[dst[0], dst[1]]:
                continue
            # 在close中
            find_result = close.find(dst)
            if find_result is not None:
                if find_result["f"] > dst_f:
                    close.remove(dst)
                    # 更新
                    open.put({"point": dst, "g": next["g"]+1, "h": h(dst), "f": dst_f, "parent": next["point"]})
                continue
            # 在open中
            find_result = open.find(dst)
            if find_result is not None and find_result["f"] > dst_f:
                open.remove(dst)
                find_result["g"], find_result["h"], find_result["f"] = next["g"]+1, h(dst), dst_f
                find_result["parent"] = next["point"]
                open.put(find_result)
            else:
                open.put({"point": dst, "g": next["g"]+1, "h": h(dst), "f": dst_f, "parent": next["point"]})
