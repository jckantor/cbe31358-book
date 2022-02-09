#!/usr/bin/env python
# coding: utf-8

# # Case Study: Analysis of a Double Pipe Heat Exchanger
# 
# A stalwart of undergraduate chemical engineering laboratories is study of a double-pipe heat exchanger in counter-current flow. In this case, a student group collected multiple measurements of flow and temperature data from a heat exchanger with sensors configured as shown in the following diagram. (Note: The diagram shows co-current flow. The data was collected with the valves configured for counter-current flow of the hot stream.)
# 
# ![](https://www.gunt.de/images/datasheet/1495/WL-315C-Comparison-of-various-heat-exchangers-gunt-1495-zeichnung_einzelheit_2.jpg)
# Source: [Gunt WL315C Product Description](https://www.gunt.de/en/products/comparison-of-various-heat-exchangers/060.315C0/wl315c/glct-1:pa-148:pr-1495)

# ## Tidy Data
# 
# The student group designed a series of experiments measuring the performance of the heat exchanger to high (H), medium (M), and low (L) flowrates for both the hot and cold streams --- a total of nine flowrate combinations. For each combination they reported data for three repeated observations. [A portion of their data is available on Google Sheets](https://docs.google.com/spreadsheets/d/1wuJq3B4z0tmTIsRpm5zZUP-PBBxT6OpuJKeBlQcQ4Z0/edit?usp=sharing). From this data they intend to compute the overall heat transfer coefficient $UA$, and attempt to fit a regression model for the heat transfer coefficients as a function of the flowrates.
# 
# A screenshot of the data collected by the students is given below.
# 
# ![](../../media/pandas-google-sheets-4.png)
# 
# :::{admonition} Study Question
# 
# Before reading further, can you find three ways this data set is not consistent with Tidy Data?
# 
# :::{toggle}
# 
# * Empty rows are included for formatting that do not contain observations.
# * Missing observations for trial 9.
# * The use of vertical merging to indicate values by position rather than by actual content.
# * The "Flow Rate (H/C)" includes two values in each cell.
# * Information in the first column is meta-data, not a useful value to include in the observations.
# 
# :::
# :::

# ## Reading Data
# 
# The raw data was copied to a new sheet in the same Google Sheets file, edited to conform with Tidy Data, and a link created using the procedures outlined above for reading data from Google Sheets. The data is read in the following cell.

# In[20]:


hx = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSNUCEFMaGZ-y18p-AnDoImEeenMLbRxXBABwFNeP8I3xiUejolPJx-kr4aUywD0szRel81Kftr8J0R/pub?gid=865146464&single=true&output=csv")
hx.head()


# ## Energy Balances
# 
# The first step in this analysis is to verify the energy balance. 
# 
# $$
# \begin{align*}
# Q_h & = \dot{q}_h \rho C_p (T_{h,in} - T_{h,out}) \\
# Q_c & = \dot{q}_c \rho C_p (T_{c,out} - T_{c, in})
# \end{align*}
# $$
# 
# The next cell creates two new calculated variables in the dataframe for $Q_h$ and $Q_c$, and uses the pandas plotting facility to visualize the results. This calculation takes advantage of the "one variable per column" rule of Tidy Data which enables calculations for all observations to be done in a single line of code.

# In[21]:


# heat capacity of water 
rho = 1.00                # kg / liter
Cp = 4.18                 # kJ/ kg / deg C

# heat balances
hx["Qh"] = rho * Cp * hx["Hot Flow (L/hr)"] * (hx["H Inlet"] - hx["H Outlet"]) / 3600
hx["Qc"] = rho * Cp * hx["Cold Flow (L/hr)"] * (hx["C Outlet"] - hx["C Inlet"]) / 3600
hx["Loss (%)"] = 100 * (1 - hx["Qc"]/hx["Qh"])

# plot
display(hx[["Qh", "Qc", "Loss (%)"]].style.format(precision=2))
hx.plot(y = ["Qh", "Qc"], ylim = (0, 15), grid=True, xlabel="Observation", ylabel="kW")


# ## Overall Heat Transfer Coefficient $UA$
# 
# The performance of a counter-current heat exchanger is given the relationship
# 
# $$Q = U A \Delta T_{lm} $$
# 
# where $\Delta T_{lm}$ is the log-mean temperature given by
# 
# $$
# \begin{align*}
# \Delta T_0 & = T_{h, out} - T_{c, in} \\
# \Delta T_1 & = T_{h, in} - T_{c, out} \\
# \\
# \Delta T_{lm} & = \frac{\Delta T_1 - \Delta T_0}{\ln\frac{\Delta T_1}{\Delta T_0}}
# \end{align*}
# $$

# In[31]:


dT0 = hx["H Outlet"] - hx["C Inlet"]
dT1 = hx["H Inlet"] - hx["C Outlet"]
hx["LMTD"] = (dT1 - dT0) / np.log(dT1/dT0)

Q = (hx.Qh + hx.Qc)/2
hx["UA"] =  Q/hx.LMTD

hx.plot(y="UA", xlabel="Observation", ylabel="kW/deg C", grid=True)


# ## How does $UA$ depend on flowrates?
# 
# The data clearly demonstrate that the heat transfer coefficient in the double pipe heat exchanger depends on flowrates of both the cold and hot liquid streams. We can see this by inspecting the data.

# In[23]:


hx[["Flow Rate H", "Flow Rate C", "Hot Flow (L/hr)", "Cold Flow (L/hr)", "UA"]]


# The replicated measurements provide an opportunity to compute averages. Here we use the pandas `.groupby()` function to group observations and compute means. The data will be used to plot results, so we'll save the results of these calculations as a new dataframe for reuse.

# In[24]:


sx = hx.groupby(["Flow Rate H", "Flow Rate C"]).mean()[["Hot Flow (L/hr)", "Cold Flow (L/hr)", "UA"]]
sx


# In[25]:


import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1)
sx.sort_values("Cold Flow (L/hr)").groupby("Flow Rate H").plot(x = "Cold Flow (L/hr)", y = "UA", 
                                                               style={"UA": 'ro-'}, ax=ax)


# In[26]:


fig, ax = plt.subplots(1, 1)
sx.sort_values("Hot Flow (L/hr)").groupby("Flow Rate C").plot(x = "Hot Flow (L/hr)", y = "UA", 
                                                               style={"UA": 'ro-'}, ax=ax)


# ## Fitting a Model for $UA$
# 
# For a series of transport mechanisms, the overall heat transfer coefficient 
# 
# $$\frac{1}{UA} = \frac{1}{U_hA} + \frac{1}{U_{tubeA}} + \frac{1}{U_cA}$$
# 
# $U_{tube}A$ is a constant for this experiment. $U_h$A and $U_c$A varying with flowrate and proporitonal to dimensionless Nusselt number.  The hot and cold liquid flows in the double pipe heat exchanger are well within the range for fully developed turbulent flow. Under these conditions for flows inside closed tubes, the Dittus-Boelter equation provides an explicit expression for Nusselt number
# 
# $$Nu = C \cdot Re ^{4/5} Pr ^ n$$
# 
# where $C$ is a constant, $Re$ is the Reynold's number that is proportional to flowrate, and $Pr$ is the Prandtl number determined by fluid properties.
# 
# Experimentally, consider a set of values for $UA$ determined by varying $\dot{m}_h$ and $\dot{m}_c$ over range of values. Because Reynold's number is proportional to flowrate, we can propose a model
# 
# $$\frac{1}{UA} = R =  R_{t} + r_h \dot{q}_h^{-0.8} + r_c \dot{q}_h^{-0.8}$$
# 
# This suggests a linear regression for $R = \frac{1}{UA}$ in terms of $X_h = \dot{q}_h^{-0.8}$ and $X_c  = \dot{q}_c^{-0.8}$.
# 

# In[27]:


hx["R"] = 1.0/hx["UA"]
hx["Xh"] = hx["Hot Flow (L/hr)"]**(-0.8)
hx["Xc"] = hx["Cold Flow (L/hr)"]**(-0.8)


# In[28]:


import statsmodels.formula.api as sm

result = sm.ols(formula="R ~ Xh + Xc", data = hx).fit()
print(result.params)
print(result.summary())


# In[29]:


hx["Rh"] = 115.3 * hx["Xh"]
hx["Rc"] = 186.3 * hx["Xc"]
hx["Rt"] = 0.142

hx["R_pred"] = hx["Rt"] + hx["Rh"] + hx["Rc"]
hx[["R", "R_pred", "Rt", "Rh", "Rc"]]


# ## Comparison of Model to Experimental Data

# In[30]:


hx["UA_pred"] = 1/hx["R_pred"]
hx.plot(y = ["UA", "UA_pred"], grid=True, title="Heat Transfer Coefficient")


# In[ ]:




