# import statements
from src.ensembler import Ensembler
from src.plot_spec import PlotSpec
from src.renderers import (IndividualLinesRenderer, MeanSDRenderer,
                           CompositeRenderer, ViolinRenderer, EventOverlayRenderer,
                           BlandAltmanRenderer)
from src.helpers import ConditionSpec, ConditionSource


# Set up variables.
fld = "/Users/Werk/Documents/Postdoc-McGill/areve-mcgill/data/Round2/16-qc"

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
rows = 1
cols = 1

# lines_and_mean = CompositeRenderer(IndividualLinesRenderer(), MeanSDRenderer())
# lines_and_events = CompositeRenderer(IndividualLinesRenderer(), EventOverlayRenderer())
#
# fig = (
#     Ensembler(in_folder=fld, channels=channels, n_rows = rows,  n_cols =cols, str_match=str_match, condition_spec=spec)
#     .add_subplot(PlotSpec('RS_abduction', "vicon", row=1, col=1, renderer=lines_and_events, events=events))
#     .add_subplot(PlotSpec('RS_abduction', "areve", row=1, col=1, renderer=lines_and_events, events=events))
#     .add_subplot(PlotSpec('RS_abduction', "pig", row=1, col=1, renderer=lines_and_events,events=events))
#
#     .add_subplot(PlotSpec('RS_abduction', "vicon", row=1, col=2, renderer=MeanSDRenderer(), events=events))
#     .add_subplot(PlotSpec('RS_abduction', "areve", row=1, col=2, renderer=MeanSDRenderer(), events=events))
#     .add_subplot(PlotSpec('RS_abduction', "pig", row=1, col=2, renderer=MeanSDRenderer(),events=events))
#
#     .add_subplot(PlotSpec('RS_abduction', "vicon", row=1, col=3, renderer=lines_and_mean))
#
#     .build(title="Shoulder abduction - AReve vs Vicon vs Plug-in Gait")
# )
# fig.show()


# ## Extras
# The returned fig from the ensembler allows the user all the functionality of plotly figures.
# e.g. add annotations to the plot
# fig.add_annotation(x=80, y=80, showarrow=False,
#             text="RMSE: 24 deg",
#             yshift=10, font=dict(size=18), row=1,col=2)

## Bland-Altman plot
fig = (
    Ensembler(in_folder=fld, channels=channels, n_rows= rows, n_cols =cols, str_match=str_match, condition_spec=spec)
    .add_subplot(PlotSpec(channel='RS_abduction',
                          condition="areve", companions=["pig"],
                          row=1, col=1, renderer=BlandAltmanRenderer(use_events=True, show_subjects=True), events=events))
    .build(title="Max Right Shoulder Abduction")
)

fig.show()

# # Set up variables
# fld = "/Users/Werk/Documents/Postdoc-McGill/breast-reduction/data/stats"
# spec = ConditionSpec(
#     source = ConditionSource.FOLDER,
#     conditions = ["Pre-surgery", "Post-surgery"]
# )
#
# channels = ['ax_pelvis_tilt_corr']
# str_match = [r"\b\d{3}[A-Z]{2}\b", r"\b\d{3}[A-Z]{3}\b"]
# events = ['impact_peak_mean', 'loading_rate_mean']
# rows = 1
# cols = 3
#
#
# fig = (
#     Ensembler(in_folder=fld, channels=channels, n_rows = rows,  n_cols =cols, str_match=str_match, condition_spec=spec, events=events)
#     .add_subplot(PlotSpec(
#         channel="ax_pelvis_tilt_corr", condition = "Pre-surgery", companions = ["Post-surgery"],
#         row=1, col=1, renderer=ViolinRenderer(), events=['impact_peak_mean'],)
#     )
#     .add_subplot(PlotSpec(
#         channel="ax_pelvis_tilt_corr", condition="Pre-surgery", companions=["Post-surgery"],
#         row=1, col=2, renderer=ViolinRenderer(), events=['loading_rate_mean'])
#     )
#     .build(title="Metrics pre- & post-BVRS")
# )
# fig.show()

