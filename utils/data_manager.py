import random
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'


def safe_divide(numerator, denominator, scale=1.0):
    if denominator is None or denominator == 0 or (isinstance(denominator, float) and np.isnan(denominator)):
        return 0.0
    return float(numerator) * scale / float(denominator)


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _generate_companies():
    names = [
        'DataScope', 'Insightica', 'MetricWave', 'Trendlytics', 'Vizionary',
        'AnalyzeHub', 'SignalCraft', 'PulseData', 'Chartful', 'QueryGrid',
    ]
    industries = [
        'Healthcare', 'Finance', 'Retail', 'Technology', 'Education',
        'Logistics', 'Advertising', 'Consulting', 'Telecom', 'Energy',
    ]
    locations = [
        'New York, NY', 'San Francisco, CA', 'Austin, TX', 'Chicago, IL',
        'Boston, MA', 'Seattle, WA', 'Denver, CO', 'Atlanta, GA', 'Miami, FL', 'Los Angeles, CA',
    ]
    return pd.DataFrame([
        {
            'company_id': i + 1,
            'name': names[i],
            'industry': industries[i],
            'size': random.choice(['11-50', '51-200', '201-500', '501-1000']),
            'location': locations[i],
        }
        for i in range(len(names))
    ])


def _generate_jobs(companies):
    titles = [
        'Senior Data Analyst', 'Business Intelligence Analyst', 'Data Analytics Consultant',
        'Marketing Analytics Specialist', 'Revenue Operations Analyst', 'Customer Insights Analyst',
        'Operations Data Analyst', 'Financial Data Analyst', 'Product Analytics Manager', 'Reporting Analyst',
        'Growth Analytics Analyst', 'Pricing Data Analyst', 'Supply Chain Analyst', 'Data Visualization Specialist',
        'Strategy Analytics Analyst', 'Risk Analytics Analyst', 'Research Data Analyst', 'Quality Analytics Analyst',
        'Sales Performance Analyst', 'Retention Analytics Analyst',
    ]
    departments = ['Analytics', 'Business Intelligence', 'Operations', 'Marketing', 'Finance', 'Product']
    start_date = datetime.now() - timedelta(days=90)
    job_records = []
    for index, title in enumerate(titles, start=1):
        company_id = int(companies.sample(1, random_state=index).iloc[0]['company_id'])
        posted_date = start_date + timedelta(days=random.randint(0, 60))
        job_records.append({
            'job_id': index,
            'company_id': company_id,
            'title': title,
            'department': random.choice(departments),
            'posted_date': posted_date.strftime('%Y-%m-%d'),
            'employment_type': random.choice(['Full-time', 'Contract', 'Part-time']),
            'salary_range': random.choice(['$70k-$90k', '$90k-$110k', '$110k-$130k']),
        })
    return pd.DataFrame(job_records)


def _generate_candidates():
    first_names = ['Avery', 'Blake', 'Camila', 'Dylan', 'Elliot', 'Finley', 'Hayden', 'Jordan', 'Kai', 'Morgan',
                   'Noah', 'Peyton', 'Quinn', 'Riley', 'Sawyer', 'Taylor', 'Vivian', 'Wesley', 'Zoe', 'Levi']
    last_names = ['Adams', 'Brooks', 'Carter', 'Diaz', 'Evans', 'Foster', 'Garcia', 'Hughes', 'Ibrahim', 'Jackson',
                  'Kim', 'Lopez', 'Morris', 'Nguyen', 'Owens', 'Parker', 'Reed', 'Shelton', 'Turner', 'Wright']
    skills = ['Python', 'SQL', 'Tableau', 'Power BI', 'R', 'Looker', 'Excel', 'Statistics', 'Machine Learning', 'Data Modeling']
    locations = ['Remote', 'New York, NY', 'Chicago, IL', 'Austin, TX', 'Seattle, WA', 'Boston, MA', 'Dallas, TX']
    return pd.DataFrame([
        {
            'candidate_id': i,
            'full_name': f"{random.choice(first_names)} {random.choice(last_names)}",
            'experience_years': random.randint(1, 12),
            'skill_primary': random.choice(skills),
            'location': random.choice(locations),
            'profile_score': random.randint(60, 98),
        }
        for i in range(1, 51)
    ])


def _generate_applications(jobs, candidates):
    statuses = ['Submitted', 'Rejected', 'Shortlisted', 'Hired']
    sources = ['Web', 'Mobile', 'Referral', 'Email']
    start_date = datetime.now() - timedelta(days=90)
    records = []
    app_id = 1
    for _ in range(100):
        candidate = candidates.sample(1).iloc[0]
        job = jobs.sample(1).iloc[0]
        status = random.choices(statuses, weights=[50, 20, 20, 10], k=1)[0]
        application_date = start_date + timedelta(days=random.randint(0, 90))
        records.append({
            'application_id': app_id,
            'candidate_id': int(candidate['candidate_id']),
            'job_id': int(job['job_id']),
            'company_id': int(job['company_id']),
            'application_date': application_date.strftime('%Y-%m-%d'),
            'status': status,
            'source': random.choice(sources),
            'applied_from': random.choice(['Landing Page', 'Job Board', 'Company Site']),
        })
        app_id += 1
    return pd.DataFrame(records)


def _generate_events(jobs, candidates):
    event_types = ['visitor', 'job_view', 'apply_click', 'submit_application', 'shortlisted', 'hired']
    records = []
    start_date = datetime.now() - timedelta(days=90)
    for index in range(1, 101):
        visitor_id = random.randint(1000, 1099)
        job = jobs.sample(1).iloc[0]
        candidate = candidates.sample(1).iloc[0]
        event_type = random.choices(event_types, weights=[20, 25, 20, 20, 10, 5], k=1)[0]
        event_time = start_date + timedelta(days=random.randint(0, 90), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        records.append({
            'event_id': index,
            'visitor_id': visitor_id,
            'session_id': f'session-{visitor_id}-{random.randint(1, 9)}',
            'event_type': event_type,
            'job_id': int(job['job_id']),
            'company_id': int(job['company_id']),
            'candidate_id': int(candidate['candidate_id']),
            'event_time': event_time.strftime('%Y-%m-%d %H:%M:%S'),
            'page_url': f"/jobs/{job['job_id']}/{job['title'].replace(' ', '-').lower()}",
        })
    return pd.DataFrame(records)


def _generate_conversions(jobs, candidates):
    conversion_types = ['Visitor', 'Job View', 'Apply Click', 'Application Submitted', 'Shortlisted', 'Hired']
    records = []
    start_date = datetime.now() - timedelta(days=90)
    for index in range(1, 101):
        job = jobs.sample(1).iloc[0]
        candidate = candidates.sample(1).iloc[0]
        conversion_type = random.choices(conversion_types, weights=[20, 25, 20, 20, 10, 5], k=1)[0]
        event_time = start_date + timedelta(days=random.randint(0, 90), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        records.append({
            'conversion_id': index,
            'job_id': int(job['job_id']),
            'company_id': int(job['company_id']),
            'candidate_id': int(candidate['candidate_id']),
            'conversion_type': conversion_type,
            'event_time': event_time.strftime('%Y-%m-%d %H:%M:%S'),
            'revenue_estimate': random.choice([0, 100, 250, 500, 750]),
        })
    return pd.DataFrame(records)


def _load_csv(path, parse_dates=None):
    if not path.exists() or path.stat().st_size == 0:
        return None
    try:
        return pd.read_csv(path, parse_dates=parse_dates) if parse_dates else pd.read_csv(path)
    except Exception:
        return None


def _write_csv(path, df):
    df.to_csv(path, index=False)


def load_all_data():
    ensure_data_dir()
    warnings = []

    companies = _load_csv(DATA_DIR / 'companies.csv')
    if companies is None or companies.empty:
        companies = _generate_companies()
        _write_csv(DATA_DIR / 'companies.csv', companies)
        warnings.append('Created sample companies.csv because the file was missing or empty.')

    jobs = _load_csv(DATA_DIR / 'jobs.csv')
    if jobs is None or jobs.empty:
        jobs = _generate_jobs(companies)
        _write_csv(DATA_DIR / 'jobs.csv', jobs)
        warnings.append('Created sample jobs.csv because the file was missing or empty.')

    candidates = _load_csv(DATA_DIR / 'candidates.csv')
    if candidates is None or candidates.empty:
        candidates = _generate_candidates()
        _write_csv(DATA_DIR / 'candidates.csv', candidates)
        warnings.append('Created sample candidates.csv because the file was missing or empty.')

    applications = _load_csv(DATA_DIR / 'applications.csv', parse_dates=['application_date'])
    if applications is None or applications.empty:
        applications = _generate_applications(jobs, candidates)
        applications['application_date'] = pd.to_datetime(applications['application_date'], errors='coerce')
        _write_csv(DATA_DIR / 'applications.csv', applications)
        warnings.append('Created sample applications.csv because the file was missing or empty.')

    conversions = _load_csv(DATA_DIR / 'conversions.csv', parse_dates=['event_time'])
    if conversions is None or conversions.empty:
        conversions = _generate_conversions(jobs, candidates)
        conversions['event_time'] = pd.to_datetime(conversions['event_time'], errors='coerce')
        _write_csv(DATA_DIR / 'conversions.csv', conversions)
        warnings.append('Created sample conversions.csv because the file was missing or empty.')

    events = _load_csv(DATA_DIR / 'events.csv', parse_dates=['event_time'])
    if events is None or events.empty:
        events = _generate_events(jobs, candidates)
        events['event_time'] = pd.to_datetime(events['event_time'], errors='coerce')
        _write_csv(DATA_DIR / 'events.csv', events)
        warnings.append('Created sample events.csv because the file was missing or empty.')

    applications = applications.drop_duplicates(subset=['candidate_id', 'job_id', 'application_date'], keep='first')
    if len(applications) < 100:
        warnings.append('Duplicate application rows were removed to preserve data quality.')

    return ({
        'companies': companies,
        'jobs': jobs,
        'candidates': candidates,
        'applications': applications,
        'conversions': conversions,
        'events': events,
    }, warnings)


def apply_filters(data, company=None, job=None, date_range=None, search_term=None):
    applications = data['applications'].copy()
    events = data['events'].copy()
    conversions = data['conversions'].copy()
    jobs = data['jobs'].copy()
    companies = data['companies'].copy()
    candidates = data['candidates'].copy()

    merged_applications = applications.merge(
        jobs[['job_id', 'title']], on='job_id', how='left'
    ).merge(
        companies[['company_id', 'name']], on='company_id', how='left'
    ).merge(
        candidates[['candidate_id', 'full_name']], on='candidate_id', how='left'
    )
    merged_applications.rename(
        columns={'name': 'company_name', 'title': 'job_title', 'full_name': 'candidate_name'},
        inplace=True,
    )

    if company:
        company_ids = companies[companies['name'].str.contains(company, case=False, na=False)]['company_id'].unique()
        merged_applications = merged_applications[merged_applications['company_id'].isin(company_ids)]
        events = events[events['company_id'].isin(company_ids)]
        conversions = conversions[conversions['company_id'].isin(company_ids)]

    if job:
        job_ids = jobs[jobs['title'].str.contains(job, case=False, na=False)]['job_id'].unique()
        merged_applications = merged_applications[merged_applications['job_id'].isin(job_ids)]
        events = events[events['job_id'].isin(job_ids)]
        conversions = conversions[conversions['job_id'].isin(job_ids)]

    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        merged_applications = merged_applications[merged_applications['application_date'].between(start_date, end_date)]
        events = events[events['event_time'].between(start_date, end_date + pd.Timedelta(days=1), inclusive='left')]
        conversions = conversions[conversions['event_time'].between(start_date, end_date + pd.Timedelta(days=1), inclusive='left')]

    if search_term:
        mask = (
            merged_applications['job_title'].astype(str).str.contains(search_term, case=False, na=False)
            | merged_applications['company_name'].astype(str).str.contains(search_term, case=False, na=False)
            | merged_applications['candidate_name'].astype(str).str.contains(search_term, case=False, na=False)
        )
        merged_applications = merged_applications[mask]
        events = events[
            events['event_type'].astype(str).str.contains(search_term, case=False, na=False)
            | events['page_url'].astype(str).str.contains(search_term, case=False, na=False)
        ]
        conversions = conversions[conversions['conversion_type'].astype(str).str.contains(search_term, case=False, na=False)]

    return {
        'companies': companies,
        'jobs': jobs,
        'candidates': candidates,
        'applications': merged_applications,
        'events': events,
        'conversions': conversions,
    }
