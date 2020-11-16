import re
import matplotlib.pyplot as plt
import numpy as np

"""
Upload Files here
Raw data is the heat released from the experiment.
Modeled data is what is resulted from Nanoanalyze modeling.
"""
raw_heat_data='ITC_R133A_Raw.txt'
modeled_data='ITC_R133A_Model.txt'

"""
Raw data paramater
Interval is the time between injections
The first injection is the time at which you have your first injection_number
Interval to baseline is the region that you are integrating. Modify this parameter to change how your graph baseline looks)
"""

interval=300
first_injection=320
interval_to_baseline=30

"""
This modifies how your 2 graphs are orientated to one another. Stacked stacks the graphs on top of each other.
You may also play with the size of the graph
Change the one you wish to True.
"""

Stacked=False
Side_by_Side=False
Width_of_graph=10
Height_of_graph=9

"""
These parameters modify the raw data graph.
You may modify both the x-axis and y-axis increments (the range is between 0 and the highest value in your data)
You may modify the x and y-axis labels as wel. The time is divided by 1000, so your graph will represent 1 as 1000. Thus, I would not touch the x-axis label.
For small greek letters, use the below format, if its a capital greek letter, replace SMALL with CAPITAL. If no greek letter, remove the "\N{GREEK SMALL LETTER MU}"
Fontsize for all labels may be modified
"""

raw_data_x_axis_intervals=1
raw_data_y_axis_intervals=0.5
raw_data_x_axis_fontsize=15
raw_data_y_axis_fontsize=15
raw_data_x_axis_label = f'Time, (sec x 10\N{SUPERSCRIPT THREE})'
raw_data_x_axis_label_fontsize = 15
raw_data_y_axis_label = f'Heat Rate, (\N{GREEK SMALL LETTER MU}J/s)'
raw_data_y_axis_label_fontsize = 15

"""
The raw data will have a textbox that describes what is being titrated into what.
You may modify its position i nthe graph using the x and y-axis location.
The same labeleing rules apply as above. If no Greek letter remove "\N{GREEK SMALL LETTER GAMMA}"
"""

raw_data_textbox_x_axis_location = 0.60
raw_data_textbox_y_axis_location = 0.65
raw_data_textbox_label = f'\N{GREEK SMALL LETTER GAMMA} ML R133A+ATP'
raw_data_textbox_fontsize = 14

"""
Same as raw data above, but now this is the modeled data.
You may modify both the x and y-axis intervals, fontsize, and set_xticklabels
"""
modeled_data_x_axis_intervals=0.5
modeled_data_y_axis_intervals=-10
modeled_data_x_axis_fontsize=15
modeled_data_y_axis_fontsize=15
modeled_data_x_axis_label= f'Mole Ratio, (\N{GREEK SMALL LETTER GAMMA} ML R133A:ATP)'
modeled_data_x_axis_label_fontsize = 15
modeled_data_y_axis_label = 'Heat, (kJ/mol)'

"""
Same as the raw text box above.
Modify the position and label of the textbox as desired.
Change the values of kd, error, n, n_error, and enthalpy.
"""
modeled_data_y_axis_label_fontsize = 15
modeled_data_textbox_x_axis_location = 0.55
modeled_data_textbox_y_axis_location = 0.60
modeled_data_textbox_fontsize = 14

modeled_data_textbox_label_kD = 11
modeled_data_textbox_label_kD_error = 4
modeled_data_textbox_label_n = 0.7
modeled_data_textbox_label_n_error= 0.04
modeled_data_textbox_label_enthalpy = -16
modeled_data_textbox_label_enthalpy_error= 1

def plot_ITC_Data():
    if Stacked is True:
        number_of_rows=2
        number_of_cols=1
    if Side_by_Side is True:
        number_of_rows=1
        number_of_cols=2
    fig, axs = plt.subplots(nrows=number_of_rows, ncols=number_of_cols,figsize=(Height_of_graph, Width_of_graph))
    injection_time=[]
    heat_release=[]
    baseline=[]
    deviation_from_first_injection=(first_injection-interval)
    injections = 1
    counter=0
    with open(raw_heat_data) as file:
        for lines in file:
            if re.search('^\d+\s+\-\d+\.\d+',lines) is None:
                continue
            time=float(lines.strip().split()[0])
            heat=float(lines.strip().split()[1])
            if time < first_injection:
                baseline.append(heat)
            if time == (interval*injections+deviation_from_first_injection):
                injections+=1
                counter=0
            if time > ((interval*(injections-1)+deviation_from_first_injection)+interval_to_baseline) and injections > 1:
                if counter == 0:
                    baseline.clear()
                counter+=1
                baseline.append(heat)
            baseline_average=sum(baseline)/len(baseline)
            value = heat-baseline_average
            if value < 0:
                value = 0
            injection_time.append(time/1000)
            heat_release.append(value)

    mole_ratio=[]
    model_heat=[]
    model_plot=[]
    with open(modeled_data) as file:
        for lines in file:
            if re.search('^\d+\s+\-\d+\.\d+',lines) is None:
                continue
            injection_number=int(lines.strip().split()[0])
            moles=float(lines.strip().split()[5])
            heat=float(lines.strip().split()[1])
            model=float(lines.strip().split()[8])
            if injection_number == 1:
                continue
            mole_ratio.append(moles)
            model_heat.append(heat)
            model_plot.append(model)
    y_axis_1=np.arange(0,max(heat_release),raw_data_y_axis_intervals)
    y_axis_2=np.arange(0,min(model_heat),modeled_data_y_axis_intervals)
    x_axis_1=np.arange(0,max(injection_time),raw_data_x_axis_intervals)
    x_axis_2=np.arange(0,max(mole_ratio),modeled_data_x_axis_intervals)
    axs[0].set_yticks(y_axis_1)
    axs[0].set_xticks(x_axis_1)
    axs[0].set_yticklabels(y_axis_1,fontsize = raw_data_y_axis_fontsize)
    axs[0].set_xticklabels(x_axis_1,fontsize= raw_data_x_axis_fontsize)
    axs[0].plot(injection_time,heat_release,'-r')
    axs[0].set_xlabel(raw_data_x_axis_label,fontsize= raw_data_x_axis_label_fontsize)
    axs[0].set_ylabel(raw_data_y_axis_label,fontsize= raw_data_y_axis_label_fontsize)
    axs[1].plot(mole_ratio,model_heat,'ro',mole_ratio,model_plot,'-b')
    axs[1].set_yticks(y_axis_2)
    axs[1].set_xticks(x_axis_2)
    axs[1].set_yticklabels(y_axis_2,fontsize= modeled_data_y_axis_fontsize)
    axs[1].set_xticklabels(x_axis_2,fontsize= modeled_data_x_axis_fontsize)
    axs[1].set_xlabel(modeled_data_x_axis_label,fontsize=modeled_data_x_axis_label_fontsize)
    axs[1].set_ylabel(modeled_data_y_axis_label,fontsize= modeled_data_y_axis_label_fontsize)

    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    plot_text_box=raw_data_textbox_label
    axs[0].text(raw_data_textbox_x_axis_location, raw_data_textbox_y_axis_location, plot_text_box, transform=axs[0].transAxes, fontsize=raw_data_textbox_fontsize,
    verticalalignment='top', bbox=props)
    model_text_box = f'Kd = {modeled_data_textbox_label_kD}\N{GREEK SMALL LETTER MU}M \u00B1 {modeled_data_textbox_label_kD_error}\N{GREEK SMALL LETTER MU}M\n n = {modeled_data_textbox_label_n} \u00B1 {modeled_data_textbox_label_n_error}\n\N{GREEK CAPITAL LETTER DELTA}H = {modeled_data_textbox_label_enthalpy} (kJ/mol) \u00B1 {modeled_data_textbox_label_enthalpy_error}'
    axs[1].text(modeled_data_textbox_x_axis_location, modeled_data_textbox_y_axis_location, model_text_box, transform=axs[1].transAxes, fontsize=modeled_data_textbox_fontsize,
        verticalalignment='bottom', bbox=props)



    plt.show()
plot_ITC_Data()
