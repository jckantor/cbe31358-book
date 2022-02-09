#!/usr/bin/env python
# coding: utf-8

# # Heat Transfer Coeffient Model
# 

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
# where $C$ is a constant, $Re$ is the Reynold's number that is proportional to flowrate $\dot{q}$, and $Pr$ is the Prandtl number determined by fluid properties.
# 
# Experimentally, consider a set of values for $U$ determined by varying volumetric flowrates $\dot{q}_h$ and $\dot{q}_c$ over range of values. Because Reynold's number is proportional to flowrate, we propose a model
# 
# $$\frac{1}{U} = R_{tube} + r_h \dot{q}_h^{-0.8} + r_c \dot{q}_c^{-0.8}$$
# 
# This suggests a regression procedure:
# 
# * Plot $\frac{1}{U}$ as a function of $\dot{q}_h^{-0.8}$ for fixed values of $\dot{q}_c$. Esitmate $r_h$ from the slope.
# * Plot $\frac{1}{U}$ as a function of $\dot{q}_c^{-0.8}$ for fixed values of $\dot{q}_h$. Estimate r_c from the slope.
# * Use the data and estimates of $r_h$ and $r_c$ to estimate $R_{tube}$.
# 
# Alternatively, one could consider using a regression procedure from the [`scikit-learn`](https://scikit-learn.org/stable/) machine learning toolkit where 
# 
# $$Y = \frac{1}{U}$$
# 
# is the variable to predicted, and where
# 
# \begin{align*}
# X_h & = \dot{q}_h^{-0.8}\\
# X_c & = \dot{q}_c^{-0.8}
# \end{align*}
# 
# are the features. The linear model to be fitted is then
# 
# $$Y = w_0 + w_h X_h + w_c X_c$$
# 
# where $w_0$, $w_h X_h$ and $w_c X_c$ correspond to resistances to heat transfer.  The range of regression techniques available in `scikit-learn` opens up opportunities to explore alternative feature sets and models for heat transfer.

# In[ ]:




