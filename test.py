ttc = "32m 26s"

def ttc_c(time):
    new_t = time.split(" ")
    new_t_lenght = len(new_t)
    if new_t_lenght == 1:
        return time
    minute_time = 60 if new_t_lenght - 2 == 1 else 0
    min_sum = str()
    for x in new_t[new_t_lenght - 2]:
        try:
            min_sum += x if isinstance(int(x), int) else ""
        except: pass
    minute_time += int(min_sum)
    return str(minute_time) + "m"



print(ttc_c(ttc))