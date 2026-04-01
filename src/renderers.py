from abc import ABC, abstractmethod
from src.data_store import DataStore
import plotly.graph_objs as go
import numpy as np

from src.style_content import StyleContext
from src.helpers import compute_ensemble

#### Plot options to add
# Scatter plot/correlation plots --> regression line option?
# Violinplots
# MeanSD
# RainCloud?

class Renderer(ABC):
    """
    Knows how to add traces for ONE (channel, condition) into a subplot
    Receives the DataStore and shared style context - Nothing else.
    """

    @abstractmethod
    def render(self,
               fig: go.Figure,
               store: DataStore,
               style: "StyleContext",
               channel: str,
               condition: str,
               row: int,
               col: int
    ) -> None: ...


class IndividualLinesRenderer(Renderer):
    def render(self, fig, store, style, channel, condition, row, col):
        arrays = store.get_lines(channel, condition)
        subjects = store.get_subject_ids(channel, condition)
        x_norm  = np.linspace(0, 100, max((len(a) for a in arrays), default=1))

        for arr, subj in zip(arrays, subjects):
            color = style.subject_color(subj)
            dash = style.condition_dash(condition)
            show_leg = style.should_show_legend("subj", subj)

            fig.add_trace(go.Scatter(
                x=x_norm, y=arr,
                mode="lines",
                name=subj,
                legendgroup=subj,
                line=dict(color=color, dash=dash, width=1.2),
                opacity=0.45,
                showlegend=show_leg,
                hovertemplate=f"<b>{subj}</b><br>%{{x:.1f}}% | %{{y:.2f}}<extra></extra>",
            ), row = row, col = col)


class MeanSDRenderer(Renderer):
    def render(self, fig, store, style, channel, condition, row, col):
        arrays = store.get_lines(channel, condition)
        if not arrays:
            return

        n = len(arrays[0])
        x = np.linspace(0, 100, n)
        mean, upper, lower = compute_ensemble(arrays)

        # Standard deviation ribbon lower limit
        fig.add_trace(go.Scatter(
            x=x,
            y=lower,
            fillcolor="rgba(0,0,0,0.10)",
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False,
        ), row=row, col=col)

        # Standard deviation ribbon upper limit
        fig.add_trace(go.Scatter(
            x=x,
            y=upper,
            fill="tonexty",
            fillcolor="rgba(0,0,0,0.10)",
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False,
        ), row=row, col=col)

        # mean line
        dash = style.condition_dash(condition)
        show_leg = style.should_show_legend("mean", condition)
        fig.add_trace(go.Scatter(
            x=x, y=mean,
            name = f"Mean_{condition}",
            legendgroup=f"Mean_{condition}",
            line=dict(color="black", width=3, dash=dash),
            hovertemplate=f"<b>Mean – {condition}</b><br>%{{x:.1f}}% | %{{y:.2f}}<extra></extra>",
        ), row = row, col = col)