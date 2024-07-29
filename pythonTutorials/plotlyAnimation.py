import plotly.graph_objects as go
import numpy as np

def animate_3d_plot():
    x = np.outer(np.linspace(-2, 2, 30), np.ones(30))
    y = x.copy().T
    z = np.zeros((30, 30))

    frames = []
    for t in np.linspace(0, 2*np.pi, 100):
        z = np.sin(x**2 + y**2 + t)
        frames.append(go.Frame(data=[go.Surface(z=z, x=x, y=y)]))

    fig = go.Figure(
        data=[go.Surface(z=z, x=x, y=y)],
        frames=frames
    )

    fig.update_layout(
        title='Animated 3D Surface Plot',
        scene=dict(zaxis=dict(range=[-1.2, 1.2])),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)])]
        )]
    )

    fig.show()

animate_3d_plot()