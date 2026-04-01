import os
from biomechzoo.utils.zload import zload
from biomechzoo.utils.engine import engine

from src.ensembler import Ensembler
from src.plot_spec import PlotSpec
from src.renderers import IndividualLinesRenderer, MeanSDRenderer

fld = "/Users/Werk/Documents/Postdoc-McGill/areve-mcgill/data/14-qc"
fl = engine(fld, extension='.zoo')
data = zload(fl[0])

# conditions = ["Pre-surgery", "Post-surgery"]
channels = ['shoulder_abduction_angle_vicon-offset', 'shoulder_abduction_angle-offset',]
str_match = [r"\b\d{3}[A-Z]{2}\b", r"\b\d{3}[A-Z]{3}\b"]

fig = (Ensembler(in_folder=fld, channels=channels, n_rows = 2,  n_cols =2, str_match=str_match,)
    .add_subplot(PlotSpec(channels[0], row=1, col=1, renderer=IndividualLinesRenderer()))
    .add_subplot(PlotSpec(channels[1], row=1, col=2, renderer=IndividualLinesRenderer()))

    .add_subplot(PlotSpec(channels[0], row=2, col=1, renderer=MeanSDRenderer()))
    .add_subplot(PlotSpec(channels[1],  row=2, col=2, renderer=MeanSDRenderer()))
    .build(title="Shoulder abduction - AReve vs Vicon")
)

fig.show()

