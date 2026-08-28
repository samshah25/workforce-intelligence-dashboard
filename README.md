# ⚡ Analytics Employee Headcount & Tenure Dashboard

An **Executive Workforce Intelligence & Tenure Analytics Platform** built with **Python**, **Streamlit**, **Pandas**, and **JavaScript DOM Mutation Handling**. 

This platform delivers real-time headcount tracking, tenure breakdown matrices, historical retention trends, and multi-dimensional drill-down analytics across **11 Pan-India Cities** and **13 Team Types**.

---

## 🧮 1. Complete Mathematical & Business Formulas Used

### A. Observation Period Filtering Rules
For any selected observation window defined by $[T_{\text{Start}}, T_{\text{End}}]$:

- **Active Headcount ($H_{\text{Active}}$)**:
  An employee is classified as **Active** if they joined on or before $T_{\text{End}}$ and had not exited before $T_{\text{End}}$:
  $$H_{\text{Active}} = \sum_{i=1}^{N} \mathbb{I}\left( \text{DOJ}_i \le T_{\text{End}} \ \land \ (\text{DOL}_i > T_{\text{End}} \ \lor \ \text{DOL}_i \text{ is Null}) \right)$$

- **Exited Count in Period ($E_{\text{Period}}$)**:
  An employee is classified as **Exited in Period** if their Date of Leaving ($\text{DOL}$) falls strictly within $[T_{\text{Start}}, T_{\text{End}}]$:
  $$E_{\text{Period}} = \sum_{i=1}^{N} \mathbb{I}\left( \text{DOL}_i \ge T_{\text{Start}} \ \land \ \text{DOL}_i \le T_{\text{End}} \right)$$

- **New Joiners Count in Period ($J_{\text{Period}}$)**:
  An employee is classified as a **New Joiner** if their Date of Joining ($\text{DOJ}$) falls strictly within $[T_{\text{Start}}, T_{\text{End}}]$:
  $$J_{\text{Period}} = \sum_{i=1}^{N} \mathbb{I}\left( \text{DOJ}_i \ge T_{\text{Start}} \ \land \ \text{DOJ}_i \le T_{\text{End}} \right)$$

---

### B. Tenure Duration Calculation
For each employee record $i$:

- **Effective End Date ($\text{Date}_{\text{End}}$)**:
  $$\text{Date}_{\text{End}, i} = \begin{cases} \text{DOL}_i, & \text{if Exited and } \text{DOL}_i \le T_{\text{End}} \\ T_{\text{End}}, & \text{otherwise} \end{cases}$$

- **Tenure in Days ($D_i$)**:
  $$D_i = \max\left(1, \ \text{Date}_{\text{End}, i} - \text{DOJ}_i\right)$$

- **Tenure in Months ($M_i$)**:
  $$M_i = \text{Round}\left(\frac{D_i}{30.4375}, 1\right)$$

- **Tenure in Years ($Y_i$)**:
  $$Y_i = \text{Round}\left(\frac{D_i}{365.25}, 2\right)$$

---

### C. Historical Comparison Metrics (MoM, QtQ, YoY)

- **Month-over-Month (MoM) % Change**:
  Compares active headcount at $[T_{\text{Start}}, T_{\text{End}}]$ against prior month $[T_{\text{Start}} - 1\text{m}, T_{\text{End}} - 1\text{m}]$:
  $$\text{MoM \%} = \left( \frac{H_{\text{Active, Current}} - H_{\text{Active, Prior Month}}}{H_{\text{Active, Prior Month}}} \right) \times 100$$

- **Quarter-over-Quarter (QtQ / QoQ) % Change**:
  Compares active headcount against prior financial quarter ($Q_{k-1}$):
  $$\text{QtQ \%} = \left( \frac{H_{\text{Active, Current}} - H_{\text{Active, Prior Quarter}}}{H_{\text{Active, Prior Quarter}}} \right) \times 100$$

- **Year-over-Year (YoY) % Change**:
  Compares active headcount against prior year $[T_{\text{Start}} - 1\text{yr}, T_{\text{End}} - 1\text{yr}]$:
  $$\text{YoY \%} = \left( \frac{H_{\text{Active, Current}} - H_{\text{Active, Prior Year}}}{H_{\text{Active, Prior Year}}} \right) \times 100$$

---

### D. Tenure Bucket Classification Matrix
Employees are categorized into 6 tenure brackets based on exact calculated tenure months ($M_i$):
$$\text{Tenure Bucket}(M_i) = \begin{cases} 
< 6 \text{ Months}, & M_i < 6 \\
6 - 12 \text{ Months}, & 6 \le M_i < 12 \\
1 - 2 \text{ Years}, & 12 \le M_i < 24 \\
2 - 3 \text{ Years}, & 24 \le M_i < 36 \\
3 - 5 \text{ Years}, & 36 \le M_i < 60 \\
5+ \text{ Years}, & M_i \ge 60
\end{cases}$$

---

## 🛠️ 2. Comprehensive Implementation & Engineering Log

### Phase 1: High-Contrast Executive Color Theme & Typography Scaling
- Built **Royal Imperial Purple Theme (`#5E2D91`)** on active port **`8590`** (`app_palette8.py`).
- Scaled up site-wide typography:
  - KPI Values: **`2.95rem`** (Bold `900`).
  - KPI Sub-Badges & Labels: **`1.25rem`** (Bold `850`).
  - Custom Table Headers (`<th>`): **`1.2rem`**; Cells (`<td>`): **`1.18rem`**.
  - Hero Header Title: **`2.75rem`** (Bold `900`, Left-Aligned).

---

### Phase 2: Dynamic Period & EmpType-Aware KPI Metric Card Matrix
Implemented dynamic KPI card layouts based on Time Period mode and Employee Type selection:

1. **`Yearly` Mode (Any EmpType)**:
   - 4 Cards: `Headcount` | `New Joiners in Year` | `Exited in Year` | `YoY % Change`.
2. **`Quarterly` Mode (Any EmpType)**:
   - 5 Cards: `Headcount` | `New Joiners in Quarter` | `Exited in Quarter` | `QtQ % Change` | `YoY % Change`.
3. **`Monthly (MTD)` / `Custom Calendar` Mode**:
   - `All EmpTypes`: 4 Cards (`Headcount` | `Active JDA` | `Active ME` | `Active TME`).
   - Specific EmpType (`JDA`, `ME`, `TME`, `JDS`): 5 Cards (`Headcount` | `Exited in Period` | `MoM %` | `QtQ %` | `YoY %`).
4. **`Today` Mode**:
   - `All EmpTypes`: 4 Cards (`Headcount` | `Active JDA` | `Active ME` | `Active TME`).
   - Specific EmpType (`JDA`, `ME`, `TME`, `JDS`): 4 Cards (`Headcount` | `MoM %` | `QtQ %` | `YoY %` -> Exited card removed!).

---

### Phase 3: Popover Rerun Persistence, Step Auto-Closing & Anti-Flicker Architecture
To override Streamlit's default behavior of closing `st.popover` on widget interaction, we built a JavaScript event listener inside `components.html`:

- **Selection Step Count Auto-Close Rules**:
  - **`Monthly (MTD)`**: Auto-closes on **3rd selection** (`Monthly` ➔ `Year` ➔ `Month`).
  - **`Quarterly`**: Auto-closes on **3rd selection** (`Quarterly` ➔ `Year` ➔ `Quarter`).
  - **`Yearly`**: Auto-closes on **2nd selection** (`Yearly` ➔ `Year`).
  - **`Today`**: Auto-closes on **1st selection**.
  - **`👤 Employee` / `🏢 Branch` / `👥 Team`**: Auto-close on **1st selection**.
- **Anti-Flicker & Single-Execution Lock (`_preventPopoverReopen`)**:
  - Removed 50ms `setInterval` polling loop.
  - Installed a 600ms closing lock flag during final selection completion (`isFinished = true`) to prevent Streamlit rerun loops from re-opening the popover.
- **Page Refresh Reset**:
  - Utilized `performance.getEntriesByType('navigation')[0].type === 'reload'` to ensure all top popovers load completely **closed on browser refresh (`F5`)**.

---

### Phase 4: Page Scroll Lock & Layout Clean-Up
- **Top Scroll Anchor**: Enforced `mainContainer.scrollTop = 0` on page refresh and filter updates while preserving user manual scrolling (`sessionStorage.getItem("user_scrolled_down")`).
- **Clean Head Bar Header**: Removed all top badges, tag pills, system status cards, and subtitles, creating a sleek **left-aligned title banner**.
- **Table Statistics Streamlining**: Removed `Exact Average Months`, `Exact Average Years`, `Median Months`, `Min Months`, `Max Months`, and `Retention Share (%)` across all data tables for a clean executive layout.

---

### Phase 5: Excel Sample Dataset Generation
- Generated a full 800-record sample dataset exported to Excel:
  - File: [`Workforce_Intelligence_Sample_Data.xlsx`](file:///C:/Users/hp/.gemini/antigravity/scratch/tenure_dashboard/Workforce_Intelligence_Sample_Data.xlsx)
  - Columns: `emp_code`, `emp_name`, `branch`, `emp_type`, `team_type`, `doj`, `dol`, `designation`, `email`, `phone`.

---

## 🚀 3. Quick Start & Execution

### Launch Dashboard (Port 8590):
```bash
python -m streamlit run app_palette8.py --server.port 8590 --server.headless true
```

### Access URL:
- **`http://localhost:8590`**
