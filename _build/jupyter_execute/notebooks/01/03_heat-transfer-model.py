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
