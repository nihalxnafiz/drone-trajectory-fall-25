"""Utility to visualize photo plans.
"""

import typing as T

import plotly.graph_objects as go

from src.data_model import Waypoint


def plot_photo_plan(photo_plans: T.List[Waypoint]) -> go.Figure:
    """Plot the photo plan on a 2D grid.

    Args:
        photo_plans: List of waypoints for the photo plan.

    Returns:
        Plotly figure object.
    """
    # handle empty input
    if not photo_plans:
        fig = go.Figure()
        fig.update_layout(title="Empty photo plan", xaxis_title="X (m)", yaxis_title="Y (m)")
        return fig

    xs = [float(wp.x_m) for wp in photo_plans]
    ys = [float(wp.y_m) for wp in photo_plans]

    # Path with markers
    hover_text = [
        f"Idx {i}: x={wp.x_m:.2f} m, y={wp.y_m:.2f} m, z={wp.z_m:.2f} m, speed={wp.speed_m_s:.2f} m/s"
        for i, wp in enumerate(photo_plans)
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines+markers",
            marker=dict(size=8, color="blue"),
            line=dict(color="blue", width=1.5),
            name="flight path",
            hoverinfo="text",
            text=hover_text,
        )
    )

    # Numbered annotations and look-at arrows
    for i, wp in enumerate(photo_plans):
        fig.add_annotation(
            x=wp.x_m,
            y=wp.y_m,
            text=str(i),
            showarrow=False,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            font=dict(size=10),
            yshift=8,
        )

        # draw a dotted line/arrow to the look_at point when available
        if wp.look_at_x_m is not None and wp.look_at_y_m is not None:
            fig.add_trace(
                go.Scatter(
                    x=[wp.x_m, wp.look_at_x_m],
                    y=[wp.y_m, wp.look_at_y_m],
                    mode="lines",
                    line=dict(color="gray", width=1, dash="dot"),
                    showlegend=False,
                    hoverinfo="none",
                )
            )
            # arrow head
            fig.add_annotation(
                x=wp.look_at_x_m,
                y=wp.look_at_y_m,
                ax=wp.x_m,
                ay=wp.y_m,
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor="gray",
            )

    fig.update_layout(
        title="Photo plan (top-down)",
        xaxis_title="X (m)",
        yaxis_title="Y (m)",
        yaxis=dict(scaleanchor="x", scaleratio=1.0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=20, t=50, b=40),
    )

    return fig
