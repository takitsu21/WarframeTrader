import numpy as np
from matplotlib import pyplot as plt

class GraphProcess:
    """render statistics as graph"""
    def __init__(self, title: str, url_name: str):
        self.title = title
        self.url_name = url_name


    
    def save_graph(self, data: dict) -> bytes:
        try:
            zz = data["payload"]["statistics_closed"]["90days"][0]["mod_rank"]
            is_mod = True
        except:
            is_mod = False
        x, y, z, d = [], [], [], []
            #     # ddate_f = stats["datetime"][:len(stats["datetime"])-19]
            #     # ddate_plan = datetime.datetime.strptime(ddate_f,"%Y-%m-%d")

        for i, stats in enumerate(data["payload"]["statistics_closed"]["90days"]):
            if is_mod:
                if i % 2 != 0:
                    y.append(stats["wa_price"])
                    z.append(stats["moving_avg"])
                    d.append(stats["volume"])
            else:
                y.append(stats["wa_price"])
                z.append(stats["moving_avg"])
                d.append(stats["volume"])

        x = np.arange(len(y))
        plt.figure(figsize=(8, 7))
        plt.subplot(2, 1, 1)
        plt.plot(x, y, "-")
        plt.plot(x, z, ":")

        plt.title(self.title)
        plt.legend(["Average selling price", "Moving average selling price"])
        plt.xlabel("Time(last 90 days)")
        plt.ylabel("Prices(platinum)")

        plt.subplot(2, 1, 2)
        plt.bar(x, d, label="Bars")
        plt.legend(["Volume sold"])
        plt.xlabel("Time(last 90 days)")
        plt.ylabel("Volume")

        plt.savefig("graphs/"+self.url_name+".png")
        # plt.show()

# if __name__ == "__main__":
#     api = WfmApi("items", "ash_prime_blueprint", "statistics")
#     graph = GraphProcess("ash", "ash_prime_blueprint")
#     graph.save_graph(run(api.data()))