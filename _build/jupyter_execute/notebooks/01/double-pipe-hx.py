#!/usr/bin/env python
# coding: utf-8

# # Double Pipe Heat Exchanger
# 

# ## Background
# 
# 
# [GUNT WL 315C Comparison of various heat exchangers](https://www.gunt.de/en/products/comparison-of-various-heat-exchangers/060.315C0/wl315c/glct-1:pa-148:pr-1495) product description.
# 
# 
# ### General Information
# 
# https://www.thomasnet.com/articles/process-equipment/double-pipe-heat-exchangers/
# 
# https://www.kochheattransfer.com/products/hairpins,-double-pipes-closures
# 
# ### Examples
# 
# <p><a href="https://commons.wikimedia.org/wiki/File:Double-Pipe_Heat_Exchanger.png#/media/File:Double-Pipe_Heat_Exchanger.png"><img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Double-Pipe_Heat_Exchanger.png" alt="Double-Pipe Heat Exchanger.png"></a><br>By &lt;a href="//commons.wikimedia.org/wiki/User:Turbojet" title="User:Turbojet"&gt;Turbojet&lt;/a&gt; - &lt;span class="int-own-work" lang="en"&gt;Own work&lt;/span&gt;, <a href="https://creativecommons.org/licenses/by-sa/4.0" title="Creative Commons Attribution-Share Alike 4.0">CC BY-SA 4.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=9718368">Link</a></p>
# 
# <p><a href="https://commons.wikimedia.org/wiki/File:Arm_counter-current_flow.jpg#/media/File:Arm_counter-current_flow.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/1/18/Arm_counter-current_flow.jpg" alt="Arm counter-current flow.jpg"></a><br>By &lt;a href="//commons.wikimedia.org/wiki/User:Cruithne9" title="User:Cruithne9"&gt;Cruithne9&lt;/a&gt; - &lt;span class="int-own-work" lang="en"&gt;Own work&lt;/span&gt;, <a href="https://creativecommons.org/licenses/by-sa/4.0" title="Creative Commons Attribution-Share Alike 4.0">CC BY-SA 4.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=57511814">Link</a></p>
# 
# 
# [Wading birds](https://www2.nau.edu/~gaud/bio300b/cntch.htm)
# 

# ## Experimental Goals
# 
# There are three basic calculations for heat exchanger design.
# 
# * **Rating.** Given the size, geometry, entering flowrates and streaam temperatures, compute the heat transferred.
# 
# * **Performance.** Given measurements of stream flowrates and temperatures, estimate the heat transfer coefficient.
# 
# * **Sizing.** Given the heat transfer requirements and stream flowrates, compute the required size and other design parameters. Sizing calculations generally require consideration of heat exchanger geometry, economics, and is considerably more complex thaan rating or performance calculations.
# 
# In this experiment, you will conduct experiments and gather data needed characterize heat exchanger performance to create a preditive model for rating calculations. You will then test your models ability to predict heat exchanger performance for other operating conditions.
# 

# ## Co-Current Operation
# 
# ### Rating Calculations
# 
# Consider a heat exchanger in a co-current configuration. Label one end $z=0$ and the other $z=1$. $z$ changes continuously from 0 to 1 over the length of the heat exchanger. If the cross-sectional for heat transfer is constant then
# 
# $$dA = A dz$$
# 
# where $A$ is the total area for heat transfer. According to the Second Law of Thermodynamics, heat transfers from the hot stream to the cold stream. A model for differential amount of heat transferred, $dQ$ over a length $dz$ is
# 
# $$dQ = UA (T_h - T_c) dz$$
# 
# where the temperture difference $T_h - T_c$ is the driving force for heat transfer. 
# 
# In a co-current configuration, let $\dot{m}_h$ and $\dot{m}_c$ denote flow in the positive $z$ direction. Heat transfer results in a cooling of the hot stream and a waarming of the cold stream relative to the same direction.
# 
# \begin{align*}
# -\dot{m}_h C_{p,h} dT_h & = dQ \\
# \dot{m}_c C_{p,c} dT_c & = dQ
# \end{align*}
# 
# In co-current operation the temperature of both inlet flows are known at $z=0$. After substitution for $dQ$, the temperature profile is  given by a pair of first order differential equations with  initial conditions for $T_h(0)$ and $T_c(0)$
# 
# \begin{align*}
# \frac{dT_h}{dz} & = -\frac{UA}{\dot{m}_hC_{p,h}}(T_h - T_c)  & T_h(z=0) = T_{h,0}\\
# \frac{dT_c}{dz} & = \frac{UA}{\dot{m}_cC_{p,c}}(T_h - T_c) & T_c(z=0) = T_{c, 0}
# \end{align*}
# 
# This is an initial value problem of two differential equations that can be solved numerically with ``scipy.integrate.solve_ivp`` as demonstrated below. 
# 
# The results of the temperature calculation can be used to complete the rating calculation.
# 
# \begin{align*}
# Q_h & = \dot{m}_h C_{p,h} (T_{h,0} - T_{h,1}) \\
# Q_c & = \dot{m}_c C_{p,c} (T_{c,1} - T_{c,0})
# \end{align*}
# 
# where we expect $Q = Q_h = Q_c$ at steady state and with negligible heat losses.
# 

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# parameter values
A = 0.1 #square meters
U = 700
mh = 600
mc = 1200
Cp = 4.0

# feed temperatures
Th0 = 55.0
Tc0 = 18.0

# number of points
n = 201

# differential equation model
def deriv(z, y):
    Th, Tc = y
    return [-U*A*(Th - Tc)/(mh*Cp), U*A*(Th-Tc)/(mc*Cp)]

# initial conditions
IC = [Th0, Tc0]

# evaluate solution
z_eval = np.linspace(0, 1, n)
soln = solve_ivp(deriv, [0, 1], IC,  t_eval=z_eval)

# plot solution
z = soln.t
y = soln.y
plt.plot(z, y[0,:], 'r', label="T_h")
plt.plot(z, y[1,:], 'b', label="T_c")
plt.legend()
plt.plot(0, Th0, 'r.', ms=20)
plt.plot(0, Tc0, 'b.', ms=20)
plt.xlabel("fractional distance z")
plt.ylabel("deg C")
plt.title("Co-current Heat Exchanger")
plt.grid(True)


# ### Measuring Heat Transfer Coefficient
# 
# An analytical solution for the difference $T_h - T_c$ is possible for this system of equations. Subtracting the second equation from the first gives
# 
# $$\frac{d(T_h - T_c)}{dz} = -UA\left(\frac{1}{\dot{m}_hC_{p,h}} + \frac{1}{\dot{m}_cC_{p,c}}\right) (T_h - T_c)$$
# 
# This is a first-order linear differentiaal equation with constant coefficients that can be solved by a separation of variables. One form of the solution is
# 
# $$\ln \frac{T_h - T_c}{T_{h,0} - T_{c,0}} = -UA\left(\frac{1}{\dot{m}_hC_{p,h}} + \frac{1}{\dot{m}_cC_{p,c}}\right)z$$
# 
# where $T_h$ and $T_c$ are functions of $z$ on the interval $0 \leq z \leq 1$.
# 
# An overall balance for the total heat transferred between the hot and cold streams is given by
# 
# \begin{align*}
# Q_h & = \dot{m}_h C_{p,h} (T_{h,0} - T_{h,1}) \\
# Q_c & = \dot{m}_c C_{p,c} (T_{c,1} - T_{c,0})
# \end{align*}
# 
# Rearranging
# 
# \begin{align*}
# \frac{1}{\dot{m}_hC_{p,h}} & = \frac{T_{h,0} - T_{h,1}}{Q_h} \\
# \frac{1}{\dot{m}_cC_{p,c}} & = \frac{T_{c,1} - T_{c,0}}{Q_c}
# \end{align*}
# 
# At steady-state $Q_h = Q_c$. With a little more algebra this leaves 
# 
# $$Q = UA \frac{(T_{h,1} - T_{c,1}) - (T_{h,0} - T_{c,0})}{\ln \frac{T_{h,1} - T_{c,1}}{T_{h,0} - T_{c,0}}}$$
# 
# The temperature dependent term multiplying $UA$ is call the **log mean temperature difference**.
# 
# $$\text{LMTD} = \frac{(T_{h,1} - T_{c,1}) - (T_{h,0} - T_{c,0})}{\ln \frac{T_{h,1} - T_{c,1}}{T_{h,0} - T_{c,0}}}$$
# 
# Given experimental data, these relationships can be used to estimate the heat transfer coefficient $U$ from steady-state measurements of inlet and outlet temperataures and heat duty.
# 
# 

# The following code provides estimates the value of $U$ from experimental data in two steps. The first step uses the temperatures measured at both ends of the exchanger and the measured heat duty to compute the LMTD and $U$. The second step refines the estimate by fitting a model to the experimental results.

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fmin

# known parameter values
A = 5.0
mh = 600
mc = 1200
Cp = 4.0

# experimental data
z_expt = np.linspace(0, 1, 5)
Th_expt = np.array([55.0, 48.0, 42.0, 38.0, 33.0])
Tc_expt = np.array([18.0, 22.0, 25.0, 28.0, 29.0])

# LMTD calculation of heat transfer coefficient
Th0, Th1 = Th_expt[0], Th_expt[-1]
Tc0, Tc1 = Tc_expt[0], Tc_expt[-1]

Qh = mh*Cp*(Th0 - Th1)
Qc = mc*Cp*(Tc1 - Tc0)
Q = (Qh + Qc)/2
print(f"Heat duty = {Q:.1f} watts")

NTU = np.log((Th1 - Tc1)/(Th0 - Th1))
LMTD = ((Th1 - Tc1) - (Th0 - Tc0))/NTU
U = Q / (LMTD * A)
print(f"NTU = {-NTU:.2f}")
print(f"LMTD = {LMTD:.2f} deg C")
print(f"U (LMTD estimate) = {U:.1f} watt/deg C/m**2")

# initial estimate of fitted parameters
p_estimate = [U, Th0, Tc0]

# simulate double pipe heat exchange given parameter vector p
def double_pipe_cocurrent(z_eval, parameters):
    U, Th0, Tc0 = parameters
    def deriv(z, y):
        Th, Tc = y
        return [-U*A*(Th - Tc)/(mh*Cp), U*A*(Th-Tc)/(mc*Cp)]
    soln = solve_ivp(deriv, [0, 1], [Th0, Tc0], t_eval=z_eval, max_step=0.01)
    Th = soln.y[0,:]
    Tc = soln.y[1,:]
    return Th, Tc
 
# compute residuals between experiment and model
def residuals(p):
    Th_pred, Tc_pred = double_pipe_cocurrent(z_expt, p)
    return sum((Th_expt - Th_pred)**2) + sum((Tc_expt - Tc_pred)**2)

# minimize residuals
p_min = fmin(residuals, p_estimate)
U_min = p_min[0]
print(f"U (model fit) = {U_min:.1f} watt/deg C/m**2")

# compute temperature profile using the best least squares fit
z_eval = np.linspace(0, 1, 201)
Th_pred, Tc_pred = double_pipe_cocurrent(z_eval, p_min)

# plot solution
plt.plot(z_eval, Th_pred, 'r', label="T_h")
plt.plot(z_eval, Tc_pred, 'b', label="T_c")
plt.legend()
plt.plot(z_expt, Th_expt, 'r.', ms=20)
plt.plot(z_expt, Tc_expt, 'b.', ms=20)
plt.xlabel("fractional distance z")
plt.ylabel("deg C")
plt.title(f"Co-current Heat Exchanger: U = {U_min:.1f} watts/deg/m**2")
plt.grid(True)


# ### Rating, revisited
# 
# Integrating
# 
# $$dQ = UA (T_h - T_c) dz$$
# 
# So that 
# 
# $$Q = UA \int_0^1 (T_h(z) - T_c(z)) dz$$
# 
# We have a solution for the difference $T_h(z) - T_c(z)$ that can be written
# 
# $$T_h(z) - T_c(z) = (T_{h,0} - T_{c,0}) \exp\left(-UA\left(\frac{1}{\dot{m}_hC_{p,h}} + \frac{1}{\dot{m}_cC_{p,c}}\right)z\right)$$
# 
# Performing the integrations produces a rating equation
# 
# \begin{align*}
# Q & = UA(T_{h,0} - T_{c,0}) \int_0^1 \exp\left(-UA\left(\frac{1}{\dot{m}_hC_{p,h}} + \frac{1}{\dot{m}_cC_{p,c}}\right)z\right)dz \\
# & = -\frac{T_{h,0} - T_{c,0}}{\frac{1}{\dot{m}_hC_{p,h}} + \frac{1}{\dot{m}_cC_{p,c}}}\left[\exp\left(-UA\left(\frac{1}{\dot{m}_hC_{p,h}} + \frac{1}{\dot{m}_cC_{p,c}}\right)z\right)\right]\biggr\rvert_0^1 \\
# \end{align*}
# 
# which provides a solution
# 
# \begin{align*}
# \implies Q & = \frac{T_{h,0} - T_{c,0}}{\frac{1}{\dot{m}_hC_{p,h}} + \frac{1}{\dot{m}_cC_{p,c}}}\left[1 - \exp\left(-UA\left(\frac{1}{\dot{m}_hC_{p,h}} + \frac{1}{\dot{m}_cC_{p,c}}\right)\right)\right]
# \end{align*}
# 
# This is an equation that predicts the heat transfer in terms of the known stream input temperatures and flowrates.

# ## Counter-Current Operation
# 
# ### Rating Calculations
# 
# Counter-current operation requires a different method of solution. For this case we will assume the cold water stream enters at $z=0$ while the hot stream enters at $z=1$. As before, heat is transferred from the hot stream to the cold stream
# 
# $$dQ = UA (T_h - T_c) dz$$
# 
# Because of the counter-current flow, $T_h$ and $T_c$ both increase in the direction of increasaing $z$
# 
# \begin{align*}
# \dot{m}_h C_{p,h} dT_h & = dQ \\
# \dot{m}_c C_{p,c} dT_c & = dQ
# \end{align*}
# 
# Substitution yields
# 
# \begin{align*}
# \frac{dT_h}{dz} & = \frac{UA}{\dot{m}_hC_{p,h}}(T_h - T_c) & T_h(z=1) = T_{h,1} \\
# \frac{dT_c}{dz} & = \frac{UA}{\dot{m}_cC_{p,c}}(T_h - T_c) & T_c(z=0) = T_{c,0}
# \end{align*}
# 
# where $T_c(0)$ and $T_h(1)$ are specified at opposite ends of the heat exchanger. For this reason, these equations for the counter-current heat exchanger comprise a two point boundary value problem.
# 
# [``scipy.integrate.solve_bvp``](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_bvp.html)

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_bvp

# parameter values
A = 5
U = 700
mh = 600
mc = 1200
Cp = 4.0

# feed temperatures
Th1 = 55.0
Tc0 = 18.0

# number of points
n = 201

# differential equation model
def deriv(z, y):
    Th, Tc = y
    return [U*A*(Th - Tc)/(mh*Cp), U*A*(Th-Tc)/(mc*Cp)]

def bc(y0, y1):
    return [y1[0] - Th1,  # bc for Th at z=1
            y0[1] - Tc0]  # bc for Tc at z=0

# evaluate solution
z_eval = np.linspace(0, 1, n)
y_guess = (Th1 + Tc0)*np.ones((2, n))/2  # initial guess
soln = solve_bvp(deriv, bc, z_eval, y_guess)


# plot solution
z = soln.x
y = soln.y
plt.plot(z, y[0,:], 'r', label="T_h")
plt.plot(z, y[1,:], 'b', label="T_c")
plt.legend()
plt.plot(1, Th1, 'r.', ms=20)
plt.plot(0, Tc0, 'b.', ms=20)
plt.xlabel("Distance")
plt.ylabel("deg C")
plt.grid(True)


# ## Heat Transfer Coefficient
# 
# The key performance parameter for the heat transfer device is the overall heat transfer coefficient $U$. The overall heat transfer coefficient is established by series of transport mechanisms ... 
# 
# * convective heat transfer from the bulk of the hot fluid to the wall of the exchanger tube, 
# * conductive heat transfer through the wall of the tube, 
# * convective heat transfer from the wall to the tube to the bulk of the cold fluid.
# 
# For a series of transport mechanisms, the overall heat transfer coefficient 
# 
# $$\frac{1}{U} = \frac{1}{U_h} + \frac{1}{U_{tube}} + \frac{1}{U_c}$$
# 
# $U_{tube}$ is a constant for these devices. $U_h$ and $U_c$ varying with flowrate and proporitonal to dimensionless Nusselt number. For fully developed turbulent flow in a pipe, the Dittus-Boelter equation provides an explicit function for estimating the Nusselt number
# 
# $$Nu = C \cdot Re^{4/5} \cdot Pr^n$$
# 
# where $C$ is a constant, $Re$ is the Reynold's number that is proportional to flowrate, and $Pr$ is the Prandtl number determined by fluid properties.
# 
# Experimentally, consider a set of values for $U$ determined by varying $\dot{m}_h$ and $\dot{m}_c$ over range of values. Because Reynold's number is proportional to flowrate, we can propose a model
# 
# $$\frac{1}{U} = R_{tube} + r_h \dot{m}_h^{-0.8} + r_c \dot{m}_h^{-0.8}$$
# 
# This suggests a regression procedure:
# 
# * Plot $\frac{1}{U}$ as a function of $\dot{m}_h^{-0.8}$ for fixed values of $\dot{m}_c$. Esitmate $r_h$ from the slope.
# * Plot $\frac{1}{U}$ as a function of $\dot{m}_c^{-0.8}$ for fixed values of $\dot{m}_h$. Estimate r_c from the slope.
# * Use the data and estimates of $r_h$ and $r_c$ to estimate $R_{tube}$.
# 

# In[ ]:





# ## Outline for a final report
# 
# * Perform co-current and counter-current temperature measurements for the double pipe each exchanger.
# 
# * Compute $U$ for each experiment using LMTD formula.
# 
# * Attempt to analyze the data by plotting $1/U$ as outlined above. If this fails, consult Dr. Kantor for a second approach.
# 
# * Use the rating caculations to compare model to measured temperature profiles. 
# 
# * Answer this question:  Would the correlation developed for $1/U$ provide an accurate way of predicting the performance of the double pipe heat exchanger?

# In[ ]:




