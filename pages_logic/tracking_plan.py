import streamlit as st


def render_tracking_plan(data):
    st.header('Tracking Plan')
    applications = data['applications']
    events = data['events']

    visitor_count = int(events[events['event_type'] == 'visitor']['visitor_id'].nunique())
    apply_clicks = int(events[events['event_type'] == 'apply_click'].shape[0])
    applications_submitted = int(applications.shape[0])
    shortlisted = int(applications[applications['status'] == 'Shortlisted'].shape[0])
    hired = int(applications[applications['status'] == 'Hired'].shape[0])

    interview_rate = (shortlisted / applications_submitted * 100) if applications_submitted else 0.0
    hiring_rate = (hired / applications_submitted * 100) if applications_submitted else 0.0
    overall_conversion_rate = (hired / visitor_count * 100) if visitor_count else 0.0

    plan_df = [
        ['Visitor Count', visitor_count, 'Unique visitors recorded in the flow.'],
        ['Apply Clicks', apply_clicks, 'Total clicks on the apply CTA.'],
        ['Applications Submitted', applications_submitted, 'Applications successfully submitted.'],
        ['Interview / Shortlist Rate', f"{interview_rate:.1f}%", 'Shortlisted applications as % of submissions.'],
        ['Hiring Rate', f"{hiring_rate:.1f}%", 'Hired applications as % of submissions.'],
        ['Overall Conversion Rate', f"{overall_conversion_rate:.1f}%", 'Hires as % of unique visitors.'],
    ]

    st.table({'Metric': [row[0] for row in plan_df], 'Value': [row[1] for row in plan_df], 'Description': [row[2] for row in plan_df]})
    st.markdown(
        '### Business metric definitions\n'
        '- Visitor Count: Unique visitor sessions entering the funnel.\n'
        '- Apply Clicks: Interest signal from visitors.\n'
        '- Applications Submitted: Completed application forms.\n'
        '- Interview / Shortlist Rate: Application quality indicator.\n'
        '- Hiring Rate: Final conversion to hire.\n'
        '- Overall Conversion Rate: Top-of-funnel to hire efficiency.\n'
    )
