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
               col: int,
               events: list,
    ) -> None: ...


class IndividualLinesRenderer(Renderer):
    def render(self, fig, store, style, channel, condition, row, col, events):
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
    def render(self, fig, store, style, channel, condition, row, col, events):
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
            showlegend=show_leg,
        ), row = row, col = col)


class EventOverlayRenderer(Renderer):
    def render(self, fig, store, style, channel, condition, row, col, events):
        if not events:
            return

        subjects = store.get_subject_ids(channel, condition)
        for event_name in events:
            evs = store.get_events(channel, condition, event_name)  # list[ZooEvent]
            for ev,subj in zip(evs, subjects):
                color = style.subject_color(subj)
                show_leg = style.should_show_legend("event", f"{subj}_{event_name}")
                fig.add_trace(go.Scatter(
                    x=[ev.x], y=[ev.y],
                    mode="markers",
                    name=f"{subj} – {event_name}",
                    legendgroup=subj,
                    marker=dict(color=color, size=8),
                    showlegend=show_leg,
                    hovertemplate=(
                        f"<b>{subj} – {event_name}</b><br>"
                        f"x: %{{x:.1f}} | y: %{{y:.2f}}<extra></extra>"
                    ),
                ), row = row, col = col)

class ViolinRenderer(Renderer):
    def __init__(self, show_points: bool = True, bandwidth: float | None = None):
        self.show_points = show_points
        self.bandwidth = bandwidth
    def render(self, fig, store, style, channel, condition, row, col, events):
        if not events:
            return

        for event_name in events:
            values   = store.get_event_values(channel, condition, event_name)  # y-only
            if not values:
                continue

            color = style.condition_color(condition)
            show_leg = style.should_show_legend("violin", f"{condition}_{event_name}")
            fig.add_trace(go.Violin(
                x=condition,
                y=values,
                name=f"{condition} – {event_name}",
                legendgroup=f"{condition}_{event_name}",
                line_color=color,
                fillcolor=color,
                opacity=0.6,
                box_visible=True,
                meanline_visible=True,
                points="all" if self.show_points else False,
                bandwidth=self.bandwidth,
                showlegend=show_leg,
            ), row = row, col = col)

#==================================================
#All future renders be placed right above this line
#==================================================

# Compose renderers freely
class CompositeRenderer(Renderer):
    """Run multiple renderers on the same subplot"""
    def __init__(self, *renderers: Renderer):
        self._renderers = renderers

    def render(self, fig, store, style, channel, condition, row, col, events):
        for r in self._renderers:
            r.render(fig, store, style, channel, condition, row, col, events)

