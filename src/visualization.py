from typing import List, Optional
import plotly.graph_objects as go
from src.data_model import Waypoint

def plot_photo_plan(plan: List[Waypoint], title: Optional[str] = None) -> go.Figure:
    """
    Visualize a photo plan (lawnmower order).
    - draws lines connecting waypoints in order
    - draws numbered markers for waypoints
    - draws optional arrows for look_at points if present
    Returns a Plotly Figure.
    """
    if title is None:
        title = "Photo plan"
    xs = [wp.x_m for wp in plan]
    ys = [wp.y_m for wp in plan]
    texts = [f"Idx {i}<br>z={wp.z_m:.2f} m<br>speed={wp.speed_m_s:.2f} m/s" for i, wp in enumerate(plan)]

    fig = go.Figure()

    # path line
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            line=dict(color="royalblue"),
            name="path",
            hoverinfo="none",
        )
    )

    # waypoint markers
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            marker=dict(size=8, color="red"),
            text=[str(i) for i in range(len(plan))],
            textposition="top center",
            hovertext=texts,
            hoverinfo="text",
            name="waypoints",
        )
    )

    # optional look_at arrows
    for i, wp in enumerate(plan):
        if wp.look_at_x_m is not None and wp.look_at_y_m is not None:
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
                arrowhead=3,
                arrowsize=1.0,
                arrowwidth=1.0,
                arrowcolor="gray",
                opacity=0.7,
            )

    fig.update_layout(
        title=title,
        xaxis_title="X (m)",
        yaxis_title="Y (m)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        width=800,
        height=800,
    )

    # square aspect
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    return fig