import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import os

# ============================================================
# Output folder
# ============================================================
os.makedirs("figures", exist_ok=True)

# ============================================================
# Physical parameters for conservative Hamiltonian pendulum
# ============================================================
g = 9.81
L = 1.0
m = 1.0

# ============================================================
# Parameters for nondimensional driven damped pendulum
# theta'' + q theta' + sin(theta) = b cos(Omega t)
# ============================================================
q = 0.5
b = 1.2
Omega = 2.0 / 3.0


# ============================================================
# Helper: wrap angle to [-pi, pi]
# ============================================================
def wrap_angle(theta):
    return (theta + np.pi) % (2 * np.pi) - np.pi


# ============================================================
# Conservative Hamiltonian pendulum
# theta' = omega
# omega' = -(g/L) sin(theta)
# ============================================================
def f_hamiltonian(theta, omega, time):
    dtheta = omega
    domega = -(g / L) * np.sin(theta)
    return np.array([dtheta, domega])


# ============================================================
# Driven damped pendulum
# theta' = omega
# omega' = -q omega - sin(theta) + b cos(Omega t)
# ============================================================
def f_driven(theta, omega, time):
    dtheta = omega
    domega = -q * omega - np.sin(theta) + b * np.cos(Omega * time)
    return np.array([dtheta, domega])


# ============================================================
# Generic RK4 solver
# ============================================================
def rk4_system(theta0, omega0, t, system_func, wrap=False):
    y = np.zeros((len(t), 2))
    y[0] = [theta0, omega0]

    for i in range(len(t) - 1):
        h = t[i + 1] - t[i]
        th, om = y[i]

        k1 = system_func(th, om, t[i])
        k2 = system_func(
            th + 0.5 * h * k1[0],
            om + 0.5 * h * k1[1],
            t[i] + 0.5 * h
        )
        k3 = system_func(
            th + 0.5 * h * k2[0],
            om + 0.5 * h * k2[1],
            t[i] + 0.5 * h
        )
        k4 = system_func(
            th + h * k3[0],
            om + h * k3[1],
            t[i] + h
        )

        y[i + 1] = y[i] + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        if wrap:
            y[i + 1, 0] = wrap_angle(y[i + 1, 0])

    return y[:, 0], y[:, 1]


# ============================================================
# Energy for conservative pendulum
# ============================================================
def pendulum_energy(theta, omega):
    kinetic = 0.5 * m * (L ** 2) * omega ** 2
    potential = m * g * L * (1 - np.cos(theta))
    return kinetic + potential


# ============================================================
# Figure 1: Conservative Hamiltonian phase portrait
# ============================================================
t_ham = np.arange(0, 20, 0.01)

theta_ham, omega_ham = rk4_system(
    theta0=1.2,
    omega0=0.0,
    t=t_ham,
    system_func=f_hamiltonian,
    wrap=False
)

plt.figure(figsize=(7, 5))
plt.plot(theta_ham, omega_ham)
plt.title("Phase Portrait of Conservative Hamiltonian Pendulum")
plt.xlabel(r"$\theta$")
plt.ylabel(r"$\omega$")
plt.grid(True)
plt.savefig("figures/hamiltonian_phase_portrait.png", dpi=200, bbox_inches="tight")
plt.close()


# ============================================================
# Figure 2: Conservative Hamiltonian energy drift
# ============================================================
E_ham = pendulum_energy(theta_ham, omega_ham)
E0_ham = E_ham[0]

plt.figure(figsize=(7, 5))
plt.plot(t_ham, E_ham - E0_ham)
plt.title("Energy Drift in Conservative Hamiltonian Pendulum")
plt.xlabel("Time")
plt.ylabel(r"$E(t)-E(0)$")
plt.grid(True)
plt.savefig("figures/hamiltonian_energy_drift.png", dpi=200, bbox_inches="tight")
plt.close()


# ============================================================
# Figure 3: Driven damped phase portrait
# ============================================================
t_drive_short = np.arange(0, 100, 0.02)

theta_drive, omega_drive = rk4_system(
    theta0=1.2,
    omega0=0.0,
    t=t_drive_short,
    system_func=f_driven,
    wrap=True
)

plt.figure(figsize=(7, 5))
plt.plot(theta_drive, omega_drive, linewidth=1)
plt.title("Phase Portrait of Driven Damped Pendulum")
plt.xlabel(r"$\theta$ mod $2\pi$")
plt.ylabel(r"$\omega$")
plt.grid(True)
plt.savefig("figures/phase_portrait.png", dpi=200, bbox_inches="tight")
plt.close()


# ============================================================
# Figure 4: Energy-like quantity for driven damped system
# ============================================================
E_drive = 0.5 * omega_drive**2 + (1 - np.cos(theta_drive))

plt.figure(figsize=(7, 5))
plt.plot(t_drive_short, E_drive)
plt.title("Energy Evolution in Driven Damped Non-Conservative System")
plt.xlabel("Time")
plt.ylabel("Energy-like quantity")
plt.grid(True)
plt.savefig("figures/energy_drift.png", dpi=200, bbox_inches="tight")
plt.close()


# ============================================================
# Figure 5: Poincare section
# ============================================================
T_end = 2000
dt = 0.02
t_chaos = np.arange(0, T_end, dt)

theta_chaos, omega_chaos = rk4_system(
    theta0=1.2,
    omega0=0.0,
    t=t_chaos,
    system_func=f_driven,
    wrap=True
)

drive_period = 2 * np.pi / Omega

# Discard transient behavior
sample_times = np.arange(500, T_end, drive_period)

p_theta = np.interp(sample_times, t_chaos, theta_chaos)
p_omega = np.interp(sample_times, t_chaos, omega_chaos)
p_theta = wrap_angle(p_theta)

plt.figure(figsize=(7, 5))
plt.scatter(p_theta, p_omega, s=6)
plt.title("Poincaré Section of Driven Damped Pendulum")
plt.xlabel(r"$\theta$ mod $2\pi$")
plt.ylabel(r"$\omega$")
plt.grid(True)
plt.savefig("figures/poincare_section.png", dpi=200, bbox_inches="tight")
plt.close()


# ============================================================
# Figure 6: Sensitivity to initial conditions
# ============================================================
eps = 1e-6

theta1, omega1 = rk4_system(
    theta0=1.2,
    omega0=0.0,
    t=t_chaos,
    system_func=f_driven,
    wrap=True
)

theta2, omega2 = rk4_system(
    theta0=1.2 + eps,
    omega0=0.0,
    t=t_chaos,
    system_func=f_driven,
    wrap=True
)

dtheta = wrap_angle(theta1 - theta2)
domega = omega1 - omega2

dist = np.sqrt(dtheta**2 + domega**2)

plt.figure(figsize=(7, 5))
plt.plot(t_chaos, np.log(dist + 1e-14))
plt.title("Sensitivity to Initial Conditions")
plt.xlabel("Time")
plt.ylabel(r"$\log ||\Delta y(t)||$")
plt.grid(True)
plt.savefig("figures/lyapunov_growth.png", dpi=200, bbox_inches="tight")
plt.close()


# ============================================================
# Figure 7: Pendulum animation for driven damped system
# ============================================================
t_anim = np.arange(0, 40, 0.02)

theta_anim, omega_anim = rk4_system(
    theta0=1.2,
    omega0=0.0,
    t=t_anim,
    system_func=f_driven,
    wrap=True
)

x = L * np.sin(theta_anim)
y = -L * np.cos(theta_anim)

fig, ax = plt.subplots(figsize=(5, 5))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 0.5)
ax.set_aspect("equal")
ax.grid(True)
ax.set_title("Driven Damped Pendulum Animation")

line, = ax.plot([], [], "o-", lw=2)

def update(frame):
    i = frame
    line.set_data([0, x[i]], [0, y[i]])
    return line,

frames = range(0, len(t_anim), 3)

ani = FuncAnimation(
    fig,
    update,
    frames=frames,
    blit=True
)

ani.save("figures/pendulum.gif", writer=PillowWriter(fps=25))
plt.close()


# ============================================================
# Print summary
# ============================================================
print("All figures generated successfully in the figures/ folder:")
print("1. hamiltonian_phase_portrait.png")
print("2. hamiltonian_energy_drift.png")
print("3. phase_portrait.png")
print("4. energy_drift.png")
print("5. poincare_section.png")
print("6. lyapunov_growth.png")
print("7. pendulum.gif")