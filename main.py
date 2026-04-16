# import statements
from src.ensembler import Ensembler
from src.plot_spec import PlotSpec
from src.renderers import (IndividualLinesRenderer, MeanSDRenderer,
                           CompositeRenderer, ViolinRenderer, EventOverlayRenderer,
                           BlandAltmanRenderer, ScatterRenderer)
from src.helpers import ConditionSpec, ConditionSource


#%% Set up variables.
fld = "/Users/Werk/Documents/Postdoc-McGill/areve-mcgill/data/Phase2/17-Stats"

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
cols = 2

lines_and_mean = CompositeRenderer(IndividualLinesRenderer(), MeanSDRenderer())
lines_and_events = CompositeRenderer(IndividualLinesRenderer(), EventOverlayRenderer())

fig = (
    Ensembler(in_folder=fld, channels=channels, n_rows = rows,  n_cols =cols, str_match=str_match, condition_spec=spec)
    .add_subplot(PlotSpec(channel='RS_abduction',
                          condition="areve", companions=["pig"], row=1, col=1, renderer=IndividualLinesRenderer(), events=events))
    # .add_subplot(PlotSpec('RS_abduction', "areve", row=1, col=1, renderer=lines_and_events, events=events))
    # .add_subplot(PlotSpec('RS_abduction', "pig", row=1, col=1, renderer=lines_and_events,events=events))

    # .add_subplot(PlotSpec('RS_abduction', row=1, col=1, renderer=MeanSDRenderer(), events=events))
    # .add_subplot(PlotSpec('RS_abduction', "areve", row=1, col=1, renderer=MeanSDRenderer(), events=events))
    # .add_subplot(PlotSpec('RS_abduction', "pig", row=1, col=1, renderer=MeanSDRenderer(),events=events))

    # .add_subplot(PlotSpec('RS_abduction', "vicon", row=1, col=3, renderer=lines_and_mean))

    .build(title="Shoulder abduction - AReve vs Vicon vs Plug-in Gait")
)
fig.show()


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
                          condition="areve", companions=["vicon"],
                          row=1, col=1,
                          renderer=ScatterRenderer(regression_line= True, show_subjects = True), events=events))
    .add_subplot(PlotSpec(channel='RS_abduction',
                          condition="areve", companions=["pig"],
                          row=1, col=2, renderer=ScatterRenderer(regression_line=True, show_subjects=False), events=events))
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
#%% Test Josh's data
fld = "/Users/Werk/Documents/Postdoc-McGill/biomechoo_ensembler/data/line_data/OFM"
spec = ConditionSpec(
    source=ConditionSource.CHANNEL,
    conditions=["alpha_imu", "alpha_ofm"],
    channel_map={
        "alpha_imu": 'LTIB_LFOF_alpha_imu',
        "alpha_ofm": 'LTIB_LFOF_alpha_ofm',
    }
)
channels = list(spec.channel_map.values())
str_match = [r"\d{3}[A-Z]{2}"]
# subjects = ['025OF','041OF','051OF','081OF','091OF']
events = ["FS"]

fig = (
    Ensembler(
        in_folder=fld, channels=channels,
        n_rows=1, n_cols=1,
        str_match=str_match, condition_spec=spec)
    .add_subplot(PlotSpec(
        'LTIB_LFOF',   "alpha_imu",
        row=1, col=1,
        renderer=IndividualLinesRenderer(), events=events))
    .add_subplot(PlotSpec(
        'LTIB_LFOF', "alpha_ofm",
        row=1, col=1,
        renderer=IndividualLinesRenderer(), events=events))
    .build(title="Shoulder abduction - AReve vs Vicon vs Plug-in Gait")
)
fig.show()