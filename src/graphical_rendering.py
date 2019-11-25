import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

month = mdates.MonthLocator()
days = mdates.DayLocator()


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

        x = np.arange(len(dates))
        plt.figure(figsize=(8, 7))
        ax1 = plt.subplot(2, 1, 1)
        ax1.xaxis.set_major_locator(MultipleLocator(7))
        ax1.xaxis.set_minor_locator(MultipleLocator(1))
        plt.plot(x, y, "r--")
        plt.plot(x, z, "k-")
        ticks = [i for i in range(len(y)) if i % 7 == 0]
        plt.xticks(ticks)
        plt.grid(True)

        plt.title(f"{self.title} ({dates[0]} - {dates[-1]})")
        plt.legend(["Moving average price", "Average selling price"])
        plt.ylabel("Prices (platinum)")

        ax2 = plt.subplot(2, 1, 2)
        plt.bar(x, d, label="Bars")
        plt.legend(["Volume sold"])
        plt.xlabel("Time (last 90 days)")
        plt.ylabel("Volume")
        plt.xticks(ticks)
        ax2.xaxis.set_major_locator(MultipleLocator(7))
        ax2.xaxis.set_minor_locator(MultipleLocator(1))
        plt.grid(True)
        plt.savefig("graphs/"+self.url_name+".png")
        plt.close('all')
        # plt.show()
