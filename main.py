# import statements
from src.ensembler import Ensembler
from src.plot_spec import PlotSpec
from src.renderers import IndividualLinesRenderer, MeanSDRenderer, CompositeRenderer, ViolinRenderer, EventOverlayRenderer
from src.helpers import ConditionSpec, ConditionSource

#%%
# Set up variables.
fld = "/Users/Werk/Documents/Postdoc-McGill/areve-mcgill/data/Round1/16-qc"

spec = ConditionSpec(
    source     = ConditionSource.CHANNEL,
    conditions = ["vicon", "areve", 'pig'],
    channel_map = {
        "vicon": "RS_abduction_vicon",
        "areve": "RS_abduction_areve",
        "pig" : "RS_abduction_pig",
    }
)
channels = ['RS_abduction']
str_match = [r"\b\d{3}[A-Z]{2}\b", r"\b\d{3}[A-Z]{3}\b"]
# subj_list = ["001CEJ"]
events = ["max"]
rows = 2
cols = 3

lines_and_mean = CompositeRenderer(IndividualLinesRenderer(), MeanSDRenderer())
fig = (
    Ensembler(in_folder=fld, channels=channels, n_rows = rows,  n_cols =cols, str_match=str_match, condition_spec=spec)
    .add_subplot(PlotSpec('RS_abduction', "vicon", row=1, col=1, renderer=IndividualLinesRenderer()))
    .add_subplot(PlotSpec('RS_abduction', "areve", row=1, col=2, renderer=IndividualLinesRenderer()))
    .add_subplot(PlotSpec('RS_abduction', "pig", row=1, col=3, renderer=IndividualLinesRenderer()))

       .build(title="Shoulder abduction - AReve vs Vicon vs Plug-in Gait")
)
fig.show()