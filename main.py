import os

from plotly.subplots import make_subplots
import plotly.graph_objs as go

from src.data_store import DataStore
from src.ensembler import Ensembler
from src.plot_spec import PlotSpec
from src.renderers import IndividualLinesRenderer

fld = "/Users/Werk/Documents/Postdoc-McGill/breast-reduction/data/nld analysis"


conditions = ["Pre-surgery", "Post-surgery"]
channels = ["ax_pelvis_tilt_corr", "ay_pelvis_tilt_corr"]
str_match = [r"\b\d{3}[A-Z]{2}\b", r"\b\d{3}[A-Z]{3}\b"]


ens = Ensembler(in_folder=fld,  channels=channels, conditions=conditions, n_rows = 2,  n_cols =2, str_match=str_match,)


ens.add_subplot(PlotSpec(channels[0], "Pre-surgery", 1, 1, IndividualLinesRenderer()))
ens.add_subplot(PlotSpec(channels[1], "Pre-surgery", 2, 1, IndividualLinesRenderer()))
ens.add_subplot(PlotSpec(channels[0], "Post-surgery", 1, 2, IndividualLinesRenderer()))
ens.add_subplot(PlotSpec(channels[1], "Post-surgery", 2, 2, IndividualLinesRenderer()))
fig = ens.build(title="Breast motion - Pre vs Post")


fig.show()