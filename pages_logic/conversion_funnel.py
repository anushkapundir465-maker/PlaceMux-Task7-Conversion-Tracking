import plotly.graph_objects as go
import streamlit as st


def render_conversion_funnel(data):
    st.header('Conversion Funnel')
    events = data['events']

    if events.empty:
        st.warning('No funnel data is available for this filter selection.')
        return

    steps = [
        ('Visitors', 'visitor'),
        ('Viewed Jobs', 'job_view'),
        ('Started Application', 'apply_click'),
        ('Completed Application', 'submit_application'),
        ('Shortlisted', 'shortlisted'),
        ('Hired', 'hired'),
    ]

    labels = []
    values = []
    for label, event_type in steps:
        values.append(int(events[events['event_type'] == event_type]['visitor_id'].nunique()))
        labels.append(label)

    fig = go.Figure(
        go.Funnel(
            y=labels,
            x=values,
            textinfo='value+percent initial',
            marker={'color': ['#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#e41a1c', '#999999']},
        )
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title='Users',
        yaxis_title='Conversion Stage',
        hovermode='closest',
    )
    st.plotly_chart(fig, use_container_width=True)
