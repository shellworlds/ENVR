# SN-112BA: 2D/3D graphs and 4s GIF for quantum/stress/swarm. Main developer: shellworlds.
"""Generates 10 graph types: phase, stress map, swarm, biometric, QFT, etc."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "output"
OUT.mkdir(parents=True, exist_ok=True)


def graph_phase_2d():
    x = np.linspace(0, 4 * np.pi, 200)
    y = np.sin(x) * np.exp(-0.1 * x)
    plt.figure(figsize=(6, 4))
    plt.plot(x, y)
    plt.xlabel("Phase")
    plt.ylabel("Amplitude")
    plt.title("SN-112BA Phase evolution 2D")
    plt.savefig(OUT / "graph_phase_2d.png", dpi=100)
    plt.close()


def graph_stress_heatmap():
    data = np.random.rand(20, 20).cumsum(axis=0).cumsum(axis=1)
    data = (data - data.min()) / (data.max() - data.min() + 1e-8)
    plt.figure(figsize=(6, 5))
    plt.imshow(data, cmap="hot", aspect="auto")
    plt.colorbar(label="Stress index")
    plt.title("SN-112BA Stress map 2D")
    plt.savefig(OUT / "graph_stress_2d.png", dpi=100)
    plt.close()


def graph_swarm_3d():
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection="3d")
    n = 50
    x = np.random.randn(n).cumsum()
    y = np.random.randn(n).cumsum()
    z = np.random.randn(n).cumsum()
    ax.scatter(x, y, z, c=range(n), cmap="viridis")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("SN-112BA Swarm 3D")
    plt.savefig(OUT / "graph_swarm_3d.png", dpi=100)
    plt.close()


def graph_biometric_2d():
    t = np.linspace(0, 4, 400)
    sig = np.sin(2 * np.pi * 1.2 * t) * np.exp(-0.2 * t) + 0.1 * np.random.randn(400)
    plt.figure(figsize=(6, 4))
    plt.plot(t, sig)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("SN-112BA Biometric signal 2D")
    plt.savefig(OUT / "graph_biometric_2d.png", dpi=100)
    plt.close()


def graph_qft_magnitude():
    n = 64
    x = np.fft.fft(np.random.randn(n))
    mag = np.abs(x)
    plt.figure(figsize=(6, 4))
    plt.stem(range(n), mag, basefmt=" ")
    plt.xlabel("Frequency bin")
    plt.ylabel("Magnitude")
    plt.title("SN-112BA QFT magnitude 2D")
    plt.savefig(OUT / "graph_qft_2d.png", dpi=100)
    plt.close()


def graph_surface_3d():
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(x, y, z, cmap="coolwarm", alpha=0.8)
    ax.set_title("SN-112BA Surface 3D")
    plt.savefig(OUT / "graph_surface_3d.png", dpi=100)
    plt.close()


def graph_contour_2d():
    x = np.linspace(-2, 2, 80)
    y = np.linspace(-2, 2, 80)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2)) * np.sin(2 * X)
    plt.figure(figsize=(6, 5))
    plt.contourf(X, Y, Z, levels=20, cmap="RdYlBu_r")
    plt.colorbar()
    plt.title("SN-112BA Contour 2D")
    plt.savefig(OUT / "graph_contour_2d.png", dpi=100)
    plt.close()


def graph_evolution_2d():
    t = np.linspace(0, 4, 100)
    series = [np.sin(2 * np.pi * (1 + i * 0.2) * t) for i in range(5)]
    plt.figure(figsize=(6, 4))
    for i, s in enumerate(series):
        plt.plot(t, s + i * 0.5, label=f"Mode {i}")
    plt.legend()
    plt.xlabel("Time")
    plt.title("SN-112BA Evolution 2D")
    plt.savefig(OUT / "graph_evolution_2d.png", dpi=100)
    plt.close()


def graph_qubit_phases():
    phases = np.linspace(0, 2 * np.pi, 20)
    probs = (np.sin(phases) ** 2 + 1) / 2
    plt.figure(figsize=(6, 4))
    plt.bar(range(20), probs, color="steelblue")
    plt.xlabel("Qubit index")
    plt.ylabel("Probability")
    plt.title("SN-112BA Qubit phases 2D")
    plt.savefig(OUT / "graph_qubit_2d.png", dpi=100)
    plt.close()


def graph_vector_3d():
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.quiver(0, 0, 0, 1, 1, 1, color="b")
    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, 1.5)
    ax.set_zlim(0, 1.5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("SN-112BA Vector 3D")
    plt.savefig(OUT / "graph_vector_3d.png", dpi=100)
    plt.close()


def generate_gif_4s():
    try:
        import imageio.v2 as imageio
    except ImportError:
        return
    from io import BytesIO
    n_frames = 40
    duration = 4.0
    fps = n_frames / duration
    frames = []
    for i in range(n_frames):
        fig, ax = plt.subplots(figsize=(4, 3))
        t = np.linspace(0, 4, 200)
        y = np.sin(2 * np.pi * t + i * 0.2) * np.exp(-0.3 * t)
        ax.plot(t, y)
        ax.set_title("SN-112BA 4s simulation")
        ax.set_ylim(-1.2, 1.2)
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=80)
        plt.close(fig)
        buf.seek(0)
        frames.append(imageio.imread(buf))
    imageio.mimsave(OUT / "simulation_4s.gif", frames, fps=fps, loop=0)


def run_all():
    graph_phase_2d()
    graph_stress_heatmap()
    graph_swarm_3d()
    graph_biometric_2d()
    graph_qft_magnitude()
    graph_surface_3d()
    graph_contour_2d()
    graph_evolution_2d()
    graph_qubit_phases()
    graph_vector_3d()
    generate_gif_4s()
    print("Graphs written to", OUT)


if __name__ == "__main__":
    run_all()
