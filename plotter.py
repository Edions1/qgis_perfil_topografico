import matplotlib.pyplot as plt
import numpy as np

plt.style.use('dark_background')

plt.ion()


class ProfilePlotter:

    def __init__(self):
        self.data = {
            "x": [],
            "y": [],
            "dist": [],
            "alt": []
        }

        self.fig = plt.figure(figsize=(12, 10))

        self.ax_map = self.fig.add_subplot(2, 2, 1)
        self.ax_prof = self.fig.add_subplot(2, 2, 2)
        self.ax_slope = self.fig.add_subplot(2, 2, 3)
        self.ax_3d = self.fig.add_subplot(2, 2, 4, projection='3d')

    # ==========================================
    def reset(self):
        for k in self.data:
            self.data[k].clear()

        print("🔄 Plot resetado")

    # ==========================================
    def add_point(self, x, y, dist, alt):
        self.data["x"].append(x)
        self.data["y"].append(y)
        self.data["dist"].append(dist)
        self.data["alt"].append(alt)

    # ==========================================
    def update(self):

        green = "#00ff41"

        d = self.data

        # MAPA
        self.ax_map.clear()
        self.ax_map.set_title("Trajeto")
        self.ax_map.plot(d["x"], d["y"], 'o-', color=green)

        # PERFIL
        self.ax_prof.clear()
        self.ax_prof.set_title("Perfil")
        self.ax_prof.plot(d["dist"], d["alt"], 'o-', color=green)

        # SLOPE
        slopes = []
        sx = []

        for i in range(1, len(d["alt"])):
            dz = d["alt"][i] - d["alt"][i - 1]
            dx = d["dist"][i] - d["dist"][i - 1]
            slopes.append((dz / dx) * 100 if dx != 0 else 0)
            sx.append(d["dist"][i])

        self.ax_slope.clear()
        self.ax_slope.set_title("Inclinação")
        self.ax_slope.plot(sx, slopes, 'o-', color=green)

        # 3D
        self.ax_3d.clear()

        if len(d["alt"]) > 3:
            x = np.array(d["dist"])
            z = np.array(d["alt"])
            y = np.linspace(0, 1, len(x))

            X, Y = np.meshgrid(x, y)
            Z = np.tile(z, (len(y), 1))

            self.ax_3d.plot_surface(X, Y, Z, cmap='Greens')

        plt.tight_layout()
        plt.draw()
        plt.pause(0.01)