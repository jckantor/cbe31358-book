#!/usr/bin/env python
# coding: utf-8

# # Lab Assignment
# 
# For this project you will measure and analyze the performance of two types of heat exchanger over a range of operating conditions in both co-current and counter-flow configurations. One the heat exchangers must be the double pipe exchanger. For the second you can choose any of the other four heat exchangers mounted on the GUNT WL 315C equipment. 
# 
# ## Experiments
# 
# 1. Familiarize yourself with GUNT WL 315C equipment (30-45 minutes).
#     * Using the schematic mounted on the equipment, trace all lines so you are understand the valve settings need to bring hot and cold water into the equipment, route flow to a specific heat exchanger whilst keeping flow away from all other heat exchangers, change flows from co-current to counter current flow.
#     * Identify [ball valves and their operation](https://en.wikipedia.org/wiki/Ball_valve), including the multi-port ball valves used to configure co-current and counter-current operation.
#     * Turn on the instrumentation and laboratory computer. Familiarize yourself with setting the instruments to display and log data from a selected heat exchanger. 
#     * Operate the equipment by varying flowrates, heat-exchangers, and display options.
#     
#     <br>
#     
# 2. Plan a set of experiments for each heat exchanger / flow configuration that you will operating. You will need to collect measurements over the full operating range of the equipment. Design your experiments by selecting at least 3 levels for the cold water flow, 3 levels for the hot water flow, and a desired number of replications for each operational setting. You will repeat this set of experiments for each heat exchanger, for co-current and counter-current flow.
# 
# 3. Collect your data. You can use the data logging feature of the GUNT WL 315 C software installed on the laboratory computer. As back up, you should manually record your data into your laboatory notebook. Use "Tidy Data" principles for data collection.
# 
# ## Analysis
# 
# The analysis of your data should include the following elements:
# 
# 1. Compute the enthalpy change for the hot and cold streams for every measurement. Compute the heat exchanger efficiency. Describe your findings.
# 
# 2. Compute the heat transfer coefficient $U$ using the log mean temperature difference observed for each measurement. Create a chart of $U$ as functions of hot and cold water flowrates. Describe your findings.
# 
# 3. For each heat exchanger, flow configuration combination, fit the model for the heat transfer coefficient described in the prior notebooks. Use the model to predict $U$ for each measurement. How well do your measurements of $U$ fit this model? Do you observe any systematic error in the comparison of the model predictions to the measurements?
# 
# 4. For the double-pipe heat exchanger, using the inlet water flow rates and temperatures, and the heat transfer coefficient predicted by the model you fit above, compute the temperature profile and the estimated heat duty. Overlay your measured temperatures on this plot. How well does the model predict the measurements? Do this for at least one set of flowrates for co-current and counter-current operation.
# 
# ## Progress Report
# 
# Your progress report is due prior to the start of the second lab session. The progress report describe the experimental design, a preliminary analysis (items 1 and 2 above) for at least one heat exchanger in at least one flow configuration, and a description of any additional measurements you need to do in the second lab session. Any questions regarding the further analysis should be addressed following submission of the progress report.
# 
# ## Final Report
# 
# This is a "writing intensive" lab report. Special attention should be given to the instructions delivered during the third lab session. All analytical elements should be completed and included in the report. Data tables and any Python coding should be included in appendices to the report. 
# 
# Keep in mind that the audience for this report would be an engineer familiar with heat exchangers and seeking specific information on the your modeling and your analysis of the performance of this particular set of equipment.
