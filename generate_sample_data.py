import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_sample_dataset(num_records=800, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    branches = [
        "Ahmedabad", "Bangalore", "Chandigarh", "Chennai", "Coimbatore",
        "Delhi", "Hyderabad", "Jaipur", "Kolkata", "Mumbai", "Pune"
    ]
    
    emp_types = ["JDA", "ME", "TME"]
    emp_type_weights = [0.25, 0.35, 0.40]
    
    tme_team_types = [
        'B2B BDE', 'BLANK', 'Bounce', 'Corporate', 'DF', 'Hot Data',
        'Multiple team', 'Online', 'Revival (Expiry)', 'SHT', 'Super', 'Super Cat', 'trainee'
    ]
    
    first_names = [
        "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
        "Ananya", "Diya", "Sanya", "Aadhya", "Pari", "Saisha", "Kavya", "Navya", "Riya", "Anika",
        "Rahul", "Rohan", "Priya", "Sneha", "Amit", "Vikram", "Neha", "Pooja", "Suresh", "Rajesh"
    ]
    
    last_names = [
        "Sharma", "Verma", "Gupta", "Patel", "Mehta", "Singh", "Kumar", "Joshi", "Nair", "Reddy",
        "Rao", "Chawla", "Deshmukh", "Banerjee", "Chatterjee", "Roy", "Shah", "Kulkarni", "Aggarwal", "Malhotra"
    ]
    
    start_date = datetime(2018, 1, 1)
    end_date = datetime(2026, 6, 30)
    total_days = (end_date - start_date).days
    
    records = []
    
    for i in range(1, num_records + 1):
        emp_code = f"EMP{i:04d}"
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        emp_name = f"{fname} {lname}"
        
        branch = random.choice(branches)
        emp_type = np.random.choice(emp_types, p=emp_type_weights)
        
        if emp_type == "TME":
            team_type = random.choice(tme_team_types)
        elif emp_type == "ME":
            team_type = random.choice(["Field Sales", "Merchant Onboarding", "Key Accounts", "Corporate ME", "BLANK"])
        else: # JDA
            team_type = random.choice(["JDA Direct", "JDA Partner", "JDA Corporate", "BLANK"])
            
        # Join date
        random_days = random.randint(0, total_days)
        doj = start_date + timedelta(days=random_days)
        
        # Decide if employee has left
        is_exited = random.random() < 0.35 # 35% attrition rate historically
        
        dol = None
        if is_exited:
            # Tenure duration before exit (between 15 days and 1800 days)
            tenure_days = random.randint(15, 1800)
            dol_candidate = doj + timedelta(days=tenure_days)
            if dol_candidate <= datetime(2026, 8, 1):
                dol = dol_candidate
            else:
                dol = None # Still active if candidate exit date is in future
                
        doj_str = doj.strftime("%Y-%m-%d")
        dol_str = dol.strftime("%Y-%m-%d") if dol else ""
        
        designation_map = {
            "JDA": ["JDA Associate", "JDA Senior Executive", "JDA Lead"],
            "ME": ["ME Executive", "Senior ME", "ME Manager"],
            "TME": ["TME Tele-caller", "TME BDE", "TME Team Lead", "TME Trainee"]
        }
        designation = random.choice(designation_map[emp_type])
        
        records.append({
            "emp_code": emp_code,
            "emp_name": emp_name,
            "branch": branch,
            "emp_type": emp_type,
            "team_type": team_type,
            "doj": doj_str,
            "dol": dol_str,
            "designation": designation,
            "email": f"{fname.lower()}.{lname.lower()}{i}@company.com",
            "phone": f"+91 {random.randint(7000000000, 9999999999)}"
        })
        
    df = pd.DataFrame(records)
    
    out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "employee_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Sample dataset with {len(df)} records generated at {csv_path}")
    return df

if __name__ == "__main__":
    generate_sample_dataset()
