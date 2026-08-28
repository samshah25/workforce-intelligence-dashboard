import pandas as pd
import numpy as np
from datetime import datetime

TENURE_BUCKETS_ORDER = [
    "< 6 Months",
    "6 - 12 Months",
    "1 - 2 Years",
    "2 - 3 Years",
    "3 - 5 Years",
    "5+ Years"
]

def assign_tenure_bucket(months):
    if months < 6:
        return "< 6 Months"
    elif months < 12:
        return "6 - 12 Months"
    elif months < 24:
        return "1 - 2 Years"
    elif months < 36:
        return "2 - 3 Years"
    elif months < 60:
        return "3 - 5 Years"
    else:
        return "5+ Years"

def calculate_tenure_and_filter(
    df: pd.DataFrame,
    obs_date: pd.Timestamp = None,
    start_date: pd.Timestamp = None,
    end_date: pd.Timestamp = None,
    selected_emp_types: list = None,
    selected_branches: list = None,
    selected_teams: list = None,
    sda_city: str = "All"
) -> pd.DataFrame:
    """
    Calculates tenure and filters employees working during selected period [start_date, end_date].
    Compatible with both obs_date (legacy single target) and start_date/end_date (period).
    """
    if df.empty:
        return pd.DataFrame()

    df = df.copy()
    
    # Resolve dates gracefully
    if end_date is None and obs_date is not None:
        end_date = obs_date
    if start_date is None and end_date is not None:
        start_date = pd.Timestamp(datetime(end_date.year, end_date.month, 1))
        
    if start_date is None or end_date is None:
        return pd.DataFrame()
    
    # Parse dates
    df['doj_dt'] = pd.to_datetime(df['doj'], errors='coerce')
    df['dol_dt'] = pd.to_datetime(df['dol'], errors='coerce')
    
    # Filter: Employees who were working during period [start_date, end_date]
    active_in_period_mask = (df['doj_dt'] <= end_date) & (df['dol_dt'].isnull() | (df['dol_dt'] >= start_date))
    df_filtered = df[active_in_period_mask].copy()
    
    if df_filtered.empty:
        return pd.DataFrame()
        
    # Calculate tenure of active employees as of period end_date
    df_filtered['effective_end_date'] = end_date
    df_filtered['tenure_days'] = (df_filtered['effective_end_date'] - df_filtered['doj_dt']).dt.days.clip(lower=0)
    df_filtered['tenure_months'] = (df_filtered['tenure_days'] / 30.4375).round(1)
    df_filtered['tenure_years'] = (df_filtered['tenure_days'] / 365.25).round(2)
    
    # Status in Period: Exited during period vs Still Active at end of period
    exited_in_period_mask = df_filtered['dol_dt'].notnull() & (df_filtered['dol_dt'] >= start_date) & (df_filtered['dol_dt'] <= end_date)
    df_filtered['exited_in_period'] = exited_in_period_mask
    df_filtered['status_as_of_obs'] = df_filtered['exited_in_period'].apply(lambda x: 'Exited' if x else 'Active')
    
    df_filtered['tenure_bucket'] = df_filtered['tenure_months'].apply(assign_tenure_bucket)
    df_filtered['tenure_bucket'] = pd.Categorical(df_filtered['tenure_bucket'], categories=TENURE_BUCKETS_ORDER, ordered=True)
    
    # Apply EmpType Filter
    if selected_emp_types and "All" not in selected_emp_types:
        df_filtered = df_filtered[df_filtered['emp_type'].isin(selected_emp_types)]
        
    # Apply Branch Filter
    if selected_branches and "All Branches" not in selected_branches and "All" not in selected_branches:
        df_filtered = df_filtered[df_filtered['branch'].isin(selected_branches)]
        
    # Apply Team Type Filter
    if selected_teams and "All Teams" not in selected_teams and "All" not in selected_teams:
        df_filtered = df_filtered[df_filtered['team_type'].isin(selected_teams)]
        
    # Apply JDA City Filter if specified
    if sda_city and sda_city != "All":
        df_filtered = df_filtered[df_filtered['branch'] == sda_city]
        
    return df_filtered

def get_tenure_summary_by_bucket(df: pd.DataFrame, group_col: str = 'branch'):
    """
    Returns grouped counts by tenure bucket and specified group_col (e.g., branch or team_type).
    """
    if df.empty:
        return pd.DataFrame()
        
    pivot = df.pivot_table(
        index=group_col,
        columns='tenure_bucket',
        values='emp_code',
        aggfunc='count',
        fill_value=0,
        observed=False
    ).reset_index()
    
    return pivot
