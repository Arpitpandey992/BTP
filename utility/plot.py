from utility.constants import nslots, updateWindow, grid_prices, delta
import matplotlib.pyplot as plt


def plot_temp_vs_time(room_temperatures, external_temperatures, save_path):
    t: list[float] = [0]
    T = [external_temperatures[0]]
    exT = []
    gp = []
    for tx in range(0, nslots, updateWindow):
        t.append(tx + delta * updateWindow)
        t.append(tx + updateWindow)
    for Tx in room_temperatures:
        T.append(Tx)
        T.append(Tx)
    for gpx in grid_prices:
        for i in range(8):
            gp.append(gpx)
    for exTx in external_temperatures:
        exT.append(exTx)
        exT.append(exTx)
    # print(t)
    # print(len(T))
    gp.append(8)
    exT.append(25)
    plt.plot(t, T)
    plt.plot(t, exT, 'red')
    plt.savefig(save_path)
    plt.close()
