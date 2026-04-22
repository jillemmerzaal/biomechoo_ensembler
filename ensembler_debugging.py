import os
# import statements
from ensembler import Ensembler
from plot_spec import PlotSpec
# line plot and event renderers
from renderers import IndividualLinesRenderer, MeanSDRenderer, EventOverlayRenderer
from renderers import ViolinRenderer, BlandAltmanRenderer, ScatterRenderer
# combiner renderers
from renderers import CompositeRenderer
from helpers import ConditionSpec, ConditionSource


#%%
# Set up variables, this time we use str_match to find participants and look for events
current_dir = os.getcwd()
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
fld = os.path.join(project_root, 'data', 'sample_study', 'normalized')

spec = ConditionSpec(source = ConditionSource.BETWEEN,
                     conditions = ['Straight', 'Turn'])
channels = ['RightAnklePower', 'RKneeAngles_x']
str_match = [r'\bHC\d{3}[A-Z]\b']
events = ['max','NRMSE']
rows = 1
cols = 3

lines_and_events = CompositeRenderer(IndividualLinesRenderer(), EventOverlayRenderer())     # within stuff

fig = (
    Ensembler(in_folder=fld,  channels=channels, n_rows=rows,  n_cols=cols, str_match=str_match, condition_spec=spec, events=events)
    .add_subplot(PlotSpec(channel='RightAnklePower', condition = 'Straight', companions = ['Turn'], row=1, col=1, renderer=lines_and_events, events=['NRMSE']))
    .add_subplot(PlotSpec(channel='RightAnklePower', condition = 'Straight', companions = ['Turn'], row=1, col=2, renderer=lines_and_events, events=['max']))
    .add_subplot(PlotSpec(channel='RightAnklePower', condition = 'Straight', companions = ['Turn'], row=1, col=3, renderer=MeanSDRenderer()))
    .build(title='Metrics Straight vs Turn')
)
fig.show()