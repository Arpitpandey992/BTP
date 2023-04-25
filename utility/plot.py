from utility.constants import nslots, updateWindow, grid_prices, delta
import matplotlib.pyplot as plt


def plot_temp_vs_time(room_temperatures, external_temperatures, save_path):
    time_hour: list[float] = [0]
    external_temps = [room_temperatures[0]]
    room_temps = []
    gp = []
    for tx in range(0, nslots, updateWindow):
        time_hour.append((tx + delta * updateWindow) / 60)
        time_hour.append((tx + updateWindow) / 60)
    for room_temperature in room_temperatures:
        external_temps.append(room_temperature)
        external_temps.append(room_temperature)
    for grid_price in grid_prices:
        for i in range(8):
            gp.append(grid_price)
    for external_temperature in external_temperatures:
        room_temps.append(external_temperature)
        room_temps.append(external_temperature)
    gp.append(gp[-1])
    room_temps.append(room_temps[-1])
    plt.plot(time_hour, external_temps, 'blue', label='External Temperatures')
    plt.plot(time_hour, room_temps, 'red', label='Room Temperatures')
    plt.xlabel('Hours')
    plt.ylabel('Temperature')
    plt.title('External and Room Temperature over Time')
    plt.legend()
    plt.savefig(save_path)
    plt.close()
