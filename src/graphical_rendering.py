import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

class GraphProcess:
    """render statistics as graph"""
    def __init__(self, title: str, url_name: str):
        self.title = title
        self.url_name = url_name

    def save_graph(self, data: dict) -> bytes:
        # with open('graph.json', 'w') as f:
        #     f.write(str(data))
        try:
            if isinstance(
                    data["payload"]["statistics_closed"]["90days"][0]["mod_rank"],
                    int
                    ):
                is_mod = True
        except Exception:
            is_mod = False
        y, z, d = [], [], []
        dates = []
        for i, stats in enumerate(data["payload"]["statistics_closed"]["90days"]):
            if is_mod:
                if i % 2 != 0:
                    y.append(stats["moving_avg"])
                    z.append(stats["avg_price"])
                    d.append(stats["volume"])
                    dates.append(stats["datetime"][0:10])
            else:
                y.append(stats["moving_avg"])
                z.append(stats["avg_price"])
                d.append(stats["volume"])
                dates.append(stats["datetime"][0:10])
        # print()
        print(len(dates))
        x = np.arange(len(dates))
        plt.figure(figsize=(8, 7))
        plt.subplot(2, 1, 1)
        plt.plot(x, y, "b--")
        plt.plot(x, z, "g-")
        locs, label = plt.xticks()
        new_xticks = [p for i, p in enumerate(dates) if i % 7 == 0]
        plt.xticks(locs, new_xticks)
        # plt.xticks([p for i, p in enumerate(dates) if i % 7 == 0])

        plt.title(self.title)
        plt.legend(["Moving average price", "Average selling price"])
        plt.xlabel("Time(last 90 days)")
        plt.ylabel("Prices(platinum)")

        plt.subplot(2, 1, 2)
        plt.bar(x, d, label="Bars")
        plt.legend(["Volume sold"])
        plt.xlabel("Time(last 90 days)")
        plt.ylabel("Volume")
        plt.xticks(locs, new_xticks)

        plt.savefig("graphs/"+self.url_name+".png")
        # plt.show()
