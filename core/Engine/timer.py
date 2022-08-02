import time

class Timer:
    def __init__(self, duration, player_one, player_two) -> None:
        self.duration = [duration, duration]
        self.player_one = player_one
        self.player_two = player_two
        self.c_time = time.perf_counter()
        self.p_time = time.perf_counter()
        self.r_min_tens = None
        self.r_min_ones = None
        self.r_sec_tens = None
        self.r_sec_ones = None
        

    def run(self, moving_side):
        self.c_time = time.perf_counter()
        dt = self.c_time - self.p_time
        self.duration[moving_side] -= dt
        self.duration[moving_side] = max(0, self.duration[moving_side])
        self.p_time = self.c_time
        self.r_min_tens = [(round(self.duration[i]) // 60) // 10 for i in range(2)]
        self.r_min_ones = [(round(self.duration[i]) // 60) % 10 for i in range(2)]
        self.r_sec_tens = [(round(self.duration[i]) % 60) // 10 for i in range(2)]
        self.r_sec_ones = [round(self.duration[i] % 60 % 10, 2) for i in range(2)]
        # print(*self.duration)