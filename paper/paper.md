# Numerical Investigation of Nonlinear Pendulum Dynamics

## Abstract

This project investigates nonlinear pendulum dynamics using numerical methods and dynamical systems analysis. The study begins with the conservative Hamiltonian pendulum and then extends the model to a driven damped nonlinear pendulum. Numerical experiments are performed using the fourth-order Runge-Kutta method. The project analyzes phase-space behavior, energy drift, sensitivity to initial conditions, and Poincaré sections. The results demonstrate how numerical simulation can reveal the limitations of linear approximation, the structure of Hamiltonian dynamics, and the emergence of complex behavior in driven nonlinear systems.

---

## 1. Introduction

The pendulum is one of the most classical models in mechanics and applied mathematics. Although the small-angle approximation reduces the pendulum to a linear oscillator, the full nonlinear pendulum exhibits richer behavior, especially for large amplitudes or under external forcing.

This project studies the pendulum from the perspective of numerical analysis and nonlinear dynamical systems. The purpose is to move beyond basic simulation and investigate qualitative properties such as phase-space geometry, energy behavior, and sensitivity to initial conditions.

The main research questions are:

1. When does the small-angle approximation fail?
2. How does the conservative Hamiltonian pendulum behave in phase space?
3. How small is the numerical energy drift under RK4?
4. How does forcing and damping change the system dynamics?
5. What does the Poincaré section reveal about long-term behavior?
6. Do nearby initial conditions separate over time?

---

## 2. Mathematical Model

### 2.1 Conservative Hamiltonian Pendulum

The nonlinear pendulum is governed by

$$
\theta'' + \frac{g}{L}\sin(\theta)=0.
$$

Introducing angular velocity

$$
\omega = \theta',
$$

the second-order equation can be rewritten as the first-order system

$$
\begin{aligned}
\theta' &= \omega, \
\omega' &= -\frac{g}{L}\sin(\theta).
\end{aligned}
$$

The associated Hamiltonian energy is

$$
E(\theta,\omega)
================

\frac{1}{2}mL^2\omega^2
+
mgL\left(1-\cos(\theta)\right).
$$

This system is conservative and has closed orbits in phase space for oscillatory motion.

---

### 2.2 Driven Damped Pendulum

To study more complex nonlinear dynamics, the driven damped pendulum is considered:

$$
\theta''
+
q\theta'
+
\sin(\theta)
============

b\cos(\Omega t).
$$

Introducing angular velocity

$$
\omega = \theta',
$$

the second-order equation can be rewritten as the first-order system

$$
\begin{aligned}
\theta' &= \omega, \
\omega' &= -q\omega - \sin(\theta) + b\cos(\Omega t).
\end{aligned}
$$

This system is not Hamiltonian because damping removes energy and external forcing injects energy.

---

## 3. Numerical Method

The simulations use the fourth-order Runge-Kutta method. For a first-order system

$$
y' = f(t,y),
$$

RK4 updates the solution by

$$
y_{n+1}
=======

y_n
+
\frac{h}{6}
\left(k_1+2k_2+2k_3+k_4\right).
$$

The four intermediate slopes are defined as

$$
\begin{aligned}
k_1 &= f(t_n,y_n), \
k_2 &= f\left(t_n+\frac{h}{2},, y_n+\frac{h}{2}k_1\right), \
k_3 &= f\left(t_n+\frac{h}{2},, y_n+\frac{h}{2}k_2\right), \
k_4 &= f(t_n+h,, y_n+h k_3).
\end{aligned}
$$

For time-dependent systems such as the driven damped pendulum, the intermediate time points in RK4 are essential. The implementation evaluates the forcing term at (t_n), (t_n+h/2), and (t_n+h).

---

## 4. Results

### 4.1 Small-Angle and Large-Angle Dynamics

The small-angle approximation works well when the initial displacement is small. However, for larger initial angles, the linear approximation fails to capture the nonlinear dynamics accurately.

This result demonstrates that linearization is a local approximation and should not be assumed valid for large-amplitude motion.

Relevant figure:

![Small-angle vs large-angle comparison](../figures/pendulum_small_vs_large_comparison.png)

---

### 4.2 Hamiltonian Phase Portrait

The phase portrait of the conservative pendulum forms a closed orbit. This is consistent with periodic oscillatory motion and the conservation of energy in the Hamiltonian system.

Relevant figure:

![Hamiltonian phase portrait](../figures/hamiltonian_phase_portrait.png)

---

### 4.3 Hamiltonian Energy Drift

The RK4 simulation of the conservative pendulum shows only a very small energy drift. The observed drift is on the order of numerical error and demonstrates strong short-to-medium time accuracy.

However, RK4 is not exactly energy-preserving. For very long-time simulations, symplectic integrators would be more appropriate for preserving Hamiltonian structure.

Relevant figure:

![Hamiltonian energy drift](../figures/hamiltonian_energy_drift.png)

---

### 4.4 Driven Damped Energy Evolution

The driven damped pendulum is non-conservative. Its energy-like quantity fluctuates over time due to the interaction between damping and external forcing.

This result shows that the driven damped system should not be interpreted as a Hamiltonian conservative system.

Relevant figure:

![Driven damped energy evolution](../figures/energy_drift.png)

---

### 4.5 Driven Damped Phase Portrait

The driven damped phase portrait shows a more complex long-time structure than the conservative Hamiltonian pendulum. This reflects the combined effects of nonlinearity, damping, and periodic forcing.

Relevant figure:

![Driven damped phase portrait](../figures/phase_portrait.png)

---

### 4.6 Poincaré Section

The Poincaré section samples the trajectory once per driving period after discarding transient behavior. The resulting structure reveals long-term nonlinear dynamics in a reduced discrete representation.

The observed pattern does not collapse to a single fixed point or simple periodic orbit, indicating nontrivial dynamics beyond simple periodic motion. It should be interpreted as qualitative evidence of complex nonlinear behavior rather than a rigorous proof of chaos.

Relevant figure:

![Poincaré section](../figures/poincare_section.png)

---

### 4.7 Sensitivity to Initial Conditions

Two trajectories initialized with a very small difference in initial angle are compared in phase space. The rapid early growth of the separation suggests sensitivity to initial conditions, followed by saturation due to bounded phase-space dynamics.

This provides qualitative evidence of complex nonlinear behavior, although a rigorous Lyapunov exponent calculation would be required for a formal chaos diagnosis.

Relevant figure:

![Sensitivity to initial conditions](../figures/lyapunov_growth.png)

---

## 5. Discussion

This project illustrates how numerical simulation can be used to study both conservative and non-conservative nonlinear systems.

The conservative Hamiltonian pendulum provides a clean example of phase-space structure and energy conservation. In contrast, the driven damped system demonstrates how forcing and damping create more complex long-term dynamics.

The use of Poincaré sections and sensitivity experiments moves the analysis beyond simple time-series visualization and toward dynamical systems methodology.

A key distinction in this project is that the conservative pendulum is Hamiltonian, while the driven damped pendulum is non-Hamiltonian. This separation is important because energy behavior and long-time phase-space structure differ significantly between the two systems.

---

## 6. Conclusion

This project presents a research-style numerical investigation of nonlinear pendulum dynamics. By combining RK4 simulation, Hamiltonian energy analysis, phase portraits, driven damped dynamics, Poincaré sections, and sensitivity experiments, the project connects numerical analysis with nonlinear dynamical systems.

The results show that numerical methods are powerful tools for studying systems that are difficult to analyze analytically. The project can be extended through symplectic integration, rigorous Lyapunov exponent computation, and bifurcation analysis.

---

## 7. Future Work

Future work could include:

* Implementing Velocity Verlet and other symplectic integrators
* Comparing long-time energy drift across integrators
* Computing Lyapunov exponents rigorously
* Producing bifurcation diagrams over the forcing amplitude
* Extending the analysis to Duffing oscillators or coupled nonlinear oscillators

