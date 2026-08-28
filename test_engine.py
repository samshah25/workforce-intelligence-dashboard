import pandas as pd
from tenure_engine import calculate_tenure_and_filter

df_raw = pd.read_csv("employee_data.csv")
print(f"Total raw records loaded: {len(df_raw)}")

# Test 1: Observation date May 31, 2026
obs_may = pd.Timestamp("2026-05-31")
df_may = calculate_tenure_and_filter(df_raw, obs_date=obs_may)
print(f"\n[Test 1 - Obs Date: 2026-05-31] Records as of May 31: {len(df_may)}")
print(f"Active count: {len(df_may[df_may['status_as_of_obs'] == 'Active'])}")
print(f"Exited count: {len(df_may[df_may['status_as_of_obs'] == 'Exited'])}")

# Check an employee who exited in April 2026
exited_april = df_may[(df_may['status_as_of_obs'] == 'Exited') & (df_may['dol'].str.startswith("2026-04"))]
if not exited_april.empty:
    sample_emp = exited_april.iloc[0]
    print("\nSample employee who exited in April 2026 when checking in May 2026:")
    print(f"  Emp Code: {sample_emp['emp_code']}")
    print(f"  DOJ: {sample_emp['doj']}")
    print(f"  DOL: {sample_emp['dol']}")
    print(f"  Effective End Date used: {sample_emp['effective_end_date']}")
    print(f"  Tenure Months: {sample_emp['tenure_months']} M")

# Test 2: EmpType = TME and Team Type = Corporate
df_tme_corp = calculate_tenure_and_filter(
    df_raw,
    obs_date=obs_may,
    selected_emp_types=["TME"],
    selected_teams=["Corporate"]
)
print(f"\n[Test 2 - TME + Corporate Team] Records: {len(df_tme_corp)}")

# Test 3: TME + ME Together
df_tme_me = calculate_tenure_and_filter(
    df_raw,
    obs_date=obs_may,
    selected_emp_types=["TME", "ME"]
)
print(f"\n[Test 3 - TME + ME Together] Records: {len(df_tme_me)}")

# Test 4: JDA City-wise filter (Mumbai)
df_jda_mumbai = calculate_tenure_and_filter(
    df_raw,
    obs_date=obs_may,
    selected_emp_types=["JDA"],
    sda_city="Mumbai"
)
print(f"\n[Test 4 - JDA + Mumbai City] Records: {len(df_jda_mumbai)}")
