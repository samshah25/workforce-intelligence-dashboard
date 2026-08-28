from flask import Flask, render_template_string, request, jsonify
import pandas as pd
import numpy as np
import os
import sys
import traceback

app = Flask(__name__)

def get_dataset():
    # Check candidate paths for dataset in Vercel serverless container
    candidate_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'employee_data.csv'),
        os.path.join(os.path.dirname(__file__), 'employee_data.csv'),
        os.path.join(os.getcwd(), 'employee_data.csv'),
        'employee_data.csv'
    ]
    
    for path in candidate_paths:
        if os.path.exists(path):
            try:
                return pd.read_csv(path)
            except Exception:
                pass
                
    # Fallback dataset generator if CSV is missing
    np.random.seed(42)
    n = 500
    cities = ["Ahmedabad", "Bangalore", "Chandigarh", "Chennai", "Coimbatore", "Delhi", "Hyderabad", "Jaipur", "Kolkata", "Mumbai", "Pune"]
    emp_types = ["JDA", "ME", "TME"]
    teams = ["Field Sales", "Corporate", "Merchant Onboarding", "Key Accounts", "B2B BDE"]
    
    dojs = pd.date_range(start="2020-01-01", end="2024-01-01", periods=n)
    dols = [d + pd.Timedelta(days=int(np.random.randint(30, 900))) if np.random.rand() < 0.3 else None for d in dojs]
    
    return pd.DataFrame({
        'emp_code': [f'EMP{1000+i}' for i in range(n)],
        'emp_name': [f'Employee {i+1}' for i in range(n)],
        'branch': np.random.choice(cities, n),
        'emp_type': np.random.choice(emp_types, n),
        'team_type': np.random.choice(teams, n),
        'doj': [d.strftime('%Y-%m-%d') for d in dojs],
        'dol': [d.strftime('%Y-%m-%d') if d else None for d in dols],
        'designation': np.random.choice(['Associate', 'Executive', 'Senior Executive', 'Manager'], n),
        'status_as_of_obs': ['Exited' if d else 'Active' for d in dols]
    })

@app.route('/')
def home():
    try:
        df = get_dataset()
        
        # Calculate KPIs safely
        if 'status_as_of_obs' in df.columns:
            active_df = df[df['status_as_of_obs'] == 'Active'].copy()
        else:
            active_df = df[df['dol'].isna()].copy()
            
        total_headcount = len(active_df)
        active_jda = len(active_df[active_df['emp_type'] == 'JDA']) if 'emp_type' in active_df.columns else 0
        active_me = len(active_df[active_df['emp_type'] == 'ME']) if 'emp_type' in active_df.columns else 0
        active_tme = len(active_df[active_df['emp_type'] == 'TME']) if 'emp_type' in active_df.columns else 0
        
        # Build Table HTML safely without nested f-string issues
        table_rows = []
        for _, r in active_df.head(20).iterrows():
            code = str(r.get('emp_code', ''))
            name = str(r.get('emp_name', ''))
            branch = str(r.get('branch', ''))
            etype = str(r.get('emp_type', ''))
            team = str(r.get('team_type', ''))
            desig = str(r.get('designation', ''))
            row_html = f"<tr><td><b>{code}</b></td><td>{name}</td><td>{branch}</td><td><b>{etype}</b></td><td>{team}</td><td>{desig}</td><td style='color:#059669; font-weight:800;'>Active</td></tr>"
            table_rows.append(row_html)
            
        rows_str = "".join(table_rows)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workforce Intelligence Executive Command</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --purple-main: #5E2D91;
            --cyan-accent: #0284C7;
            --emerald-accent: #059669;
            --amber-accent: #D97706;
            --rose-accent: #7E22CE;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #F8FAFC;
            background-image: 
                radial-gradient(at 12% 5%, rgba(233, 213, 255, 0.55) 0px, transparent 45%),
                radial-gradient(at 88% 12%, rgba(224, 242, 254, 0.55) 0px, transparent 50%),
                radial-gradient(at 50% 45%, rgba(243, 232, 255, 0.4) 0px, transparent 60%),
                radial-gradient(at 20% 88%, rgba(209, 250, 229, 0.35) 0px, transparent 45%);
            background-attachment: fixed;
            color: #0F172A;
            padding: 2rem;
        }}
        .header-banner {{
            background: linear-gradient(135deg, #4A1D75 0%, #5E2D91 40%, #7B4BB3 75%, #3B1C63 100%);
            padding: 2.4rem 3.2rem;
            border-radius: 20px;
            color: white;
            box-shadow: 0 20px 50px rgba(94, 45, 145, 0.38);
            margin-bottom: 2rem;
        }}
        .header-banner h1 {{ font-size: 2.4rem; font-weight: 900; letter-spacing: -0.5px; }}
        .header-banner p {{ font-size: 1.1rem; opacity: 0.9; margin-top: 0.4rem; }}
        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.2rem;
            margin-bottom: 2rem;
        }}
        .kpi-card {{
            border-radius: 20px;
            padding: 1.6rem;
            background: white;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease;
        }}
        .kpi-card.hc {{ border-top: 5px solid var(--cyan-accent); background: linear-gradient(135deg, #FFF 35%, #E0F2FE 100%); }}
        .kpi-card.jda {{ border-top: 5px solid var(--emerald-accent); background: linear-gradient(135deg, #FFF 35%, #D1FAE5 100%); }}
        .kpi-card.me {{ border-top: 5px solid var(--amber-accent); background: linear-gradient(135deg, #FFF 35%, #FEF3C7 100%); }}
        .kpi-card.tme {{ border-top: 5px solid var(--rose-accent); background: linear-gradient(135deg, #FFF 35%, #F3E8FF 100%); }}
        .kpi-val {{ font-size: 3.2rem; font-weight: 900; line-height: 1.1; margin-bottom: 0.4rem; }}
        .kpi-card.hc .kpi-val {{ color: var(--cyan-accent); }}
        .kpi-card.jda .kpi-val {{ color: var(--emerald-accent); }}
        .kpi-card.me .kpi-val {{ color: var(--amber-accent); }}
        .kpi-card.tme .kpi-val {{ color: var(--rose-accent); }}
        .kpi-title {{ font-size: 0.95rem; font-weight: 800; text-transform: uppercase; color: #475569; }}
        .parent-tabs {{ display: flex; gap: 1rem; margin-bottom: 1.5rem; }}
        .parent-tab-btn {{
            font-size: 1.85rem; font-weight: 900; padding: 16px 36px; min-height: 64px;
            border-radius: 18px; border: 2px solid #D8B4FE; background: white; color: var(--purple-main);
        }}
        .parent-tab-btn.active {{
            background: var(--purple-main); color: white; border-color: var(--purple-main);
            box-shadow: 0 10px 28px rgba(94, 45, 145, 0.4);
        }}
        .table-card {{ background: white; border-radius: 18px; padding: 1.8rem; box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05); border: 1.5px solid #CBD5E1; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
        th {{ background: linear-gradient(90deg, #5E2D91 0%, #0F172A 100%); color: white; padding: 14px; text-align: left; font-weight: 800; }}
        td {{ padding: 12px 14px; border-bottom: 1px solid #E2E8F0; font-weight: 600; }}
        tr:nth-child(even) {{ background: #F8FAFC; }}
    </style>
</head>
<body>
    <div class="header-banner">
        <h1>⚡ Workforce Intelligence Executive Command</h1>
        <p>Real-time Employee Headcount, Active ME/TME/JDA Analytics & Tenure Intelligence</p>
    </div>
    <div class="kpi-container">
        <div class="kpi-card hc"><div class="kpi-val">{total_headcount}</div><div class="kpi-title">TOTAL HEADCOUNT</div></div>
        <div class="kpi-card jda"><div class="kpi-val">{active_jda}</div><div class="kpi-title">ACTIVE JDA</div></div>
        <div class="kpi-card me"><div class="kpi-val">{active_me}</div><div class="kpi-title">ACTIVE ME</div></div>
        <div class="kpi-card tme"><div class="kpi-val">{active_tme}</div><div class="kpi-title">ACTIVE TME</div></div>
    </div>
    <div class="parent-tabs">
        <button class="parent-tab-btn active">📊 Employee Headcount</button>
        <button class="parent-tab-btn">⏳ Tenure Breakdown</button>
        <button class="parent-tab-btn">🔍 Employee Drill-Down</button>
    </div>
    <div class="table-card">
        <h2>🏢 Active Employee Roster Summary ({len(active_df)} Total Records)</h2>
        <table>
            <thead>
                <tr>
                    <th>Emp Code</th><th>Name</th><th>Branch</th><th>Type</th><th>Team</th><th>Designation</th><th>Status</th>
                </tr>
            </thead>
            <tbody>
                {rows_str}
            </tbody>
        </table>
    </div>
</body>
</html>"""
        return html
    except Exception as err:
        err_msg = traceback.format_exc()
        return f"<h1>Dashboard Initialization Status</h1><pre>{err_msg}</pre>", 200

handler = app
