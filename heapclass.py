class basic_info:
    def __init__(self, home, away, point_differential):
        self.home = home
        self.away = away
        self.pd = point_differential


class minHeap:
    def __init__(self):
        self.heap = []

    def insert(self, game):
        self.heap.append(game)
        self.build_min_heap()

    def min_heapify(self, position):
        left_child = self.left(position)
        right_child = self.right(position)
        if left_child < len(self.heap) and self.heap[left_child].pd < self.heap[position].pd:
            smallest = left_child
        else:
            smallest = position
        if right_child < len(self.heap) and self.heap[right_child].pd < self.heap[smallest].pd:
            smallest = right_child
        if smallest != position:
            self.heap[position], self.heap[smallest] = self.heap[smallest], self.heap[position]
            self.min_heapify(smallest)

    def left(self, k):
        return 2 * k + 1

    def right(self, k):
        return 2 * k + 2

    def build_min_heap(self):
        n = int((len(self.heap)//2)-1)
        for k in range(n, -1, -1):
            self.min_heapify(k)

    def pop_top(self):
        self.heap.pop(0)    
        self.build_min_heap()


##### EXAMPLE USAGE ########
data = [basic_info("raptors", "warriors", 10), basic_info("cavs", "thunder", 1), 
        basic_info("heat", "bulls", 0), basic_info("celtics", "irish", 100),
        basic_info("nugs", "blazers", 7), basic_info("pistons", "magic", 3),
        basic_info("rockets", "chiefs", 11)]




heap = minHeap()

for game in data:
    heap.insert(game)

heap.pop_top()

for obj in heap.heap:
    print(obj.home, obj.away, obj.pd)