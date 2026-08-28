import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import os
import io

from generate_sample_data import generate_sample_dataset
from tenure_engine import calculate_tenure_and_filter

st.set_page_config(
    page_title="Workforce Intelligence Executive Command",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Full Dark Navy Foundation Design System (Color Palette 3)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body {
        scroll-behavior: smooth !important;
    }

    .stApp {
        background-color: #060D1F;
        background-image: 
            radial-gradient(at 50% 0%, #091229 0%, transparent 75%),
            radial-gradient(at 0% 100%, rgba(16, 31, 64, 0.3) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(20, 39, 77, 0.25) 0px, transparent 50%);
        background-attachment: fixed;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #CAD5E8;
    }

    /* Executive Command Hero Header (#0A1530 Header Background) */
    .command-hero-header {
        background: linear-gradient(135deg, #0A1530 0%, #0D1A36 50%, #0A1530 100%);
        padding: 2.2rem 3rem;
        border-radius: 24px;
        color: #F4F7FC;
        margin-bottom: 2rem;
        box-shadow: 0 16px 40px rgba(6, 13, 31, 0.8), 0 0 30px rgba(16, 31, 64, 0.3);
        border: 1.5px solid rgba(26, 53, 100, 0.5);
    }
    .command-badge {
        display: inline-block;
        background: rgba(16, 31, 64, 0.5);
        color: #94A8D0;
        border: 1px solid #1A3564;
        font-weight: 800;
        font-size: 0.8rem;
        padding: 5px 14px;
        border-radius: 20px;
        backdrop-filter: blur(4px);
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    .command-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #F4F7FC;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    .command-subtitle {
        font-size: 1rem;
        color: #CAD5E8;
        margin-top: 6px;
        font-weight: 600;
    }

    /* 4-Category Dropdown Popover Header Trigger Styling (#101F40 Card, #14274D Hover) */
    div[data-testid="stPopover"] {
        width: 100% !important;
        margin-bottom: 1.5rem !important;
    }
    div[data-testid="stPopover"] button,
    button[data-testid="stPopoverButton"],
    button[data-testid="stBaseButton-secondary"] {
        background: #101F40 !important;
        background-color: #101F40 !important;
        border: 1.5px solid rgba(26, 53, 100, 0.5) !important;
        border-radius: 18px !important;
        box-shadow: 0 6px 18px rgba(6, 13, 31, 0.6), 0 0 15px rgba(16, 31, 64, 0.2) !important;
        padding: 0.9rem 1.2rem !important;
        width: 100% !important;
        color: #F4F7FC !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="stPopover"] button:hover,
    button[data-testid="stPopoverButton"]:hover {
        background: #14274D !important;
        background-color: #14274D !important;
        box-shadow: 0 10px 24px rgba(6, 13, 31, 0.8), 0 0 25px rgba(26, 53, 100, 0.4) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stPopover"] button *,
    button[data-testid="stPopoverButton"] *,
    button[data-testid="stPopoverButton"] p,
    button[data-testid="stPopoverButton"] span,
    button[data-testid="stPopoverButton"] div,
    button[data-testid="stPopoverButton"] svg {
        color: #F4F7FC !important;
        fill: #F4F7FC !important;
        font-weight: 800 !important;
        font-size: 1.12rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* Popover Top Accent Borders */
    div[data-testid="column"]:nth-child(1) div[data-testid="stPopover"] > button {
        border-top: 5px solid #1A3564 !important;
    }
    div[data-testid="column"]:nth-child(1) div[data-testid="stPopover"] > button:hover {
        background: #14274D !important;
    }

    div[data-testid="column"]:nth-child(2) div[data-testid="stPopover"] > button {
        border-top: 5px solid #2B4C8C !important;
    }
    div[data-testid="column"]:nth-child(2) div[data-testid="stPopover"] > button:hover {
        background: #14274D !important;
    }

    div[data-testid="column"]:nth-child(3) div[data-testid="stPopover"] > button {
        border-top: 5px solid #3B67B5 !important;
    }
    div[data-testid="column"]:nth-child(3) div[data-testid="stPopover"] > button:hover {
        background: #14274D !important;
    }

    div[data-testid="column"]:nth-child(4) div[data-testid="stPopover"] > button {
        border-top: 5px solid #1A3564 !important;
    }
    div[data-testid="column"]:nth-child(4) div[data-testid="stPopover"] > button:hover {
        background: #14274D !important;
    }

    /* Floating Popover Container Body Styling (#0D1A36 Background 3) */
    div[data-testid="stPopoverBody"] {
        background: #0D1A36 !important;
        backdrop-filter: blur(16px) !important;
        border: 1.5px solid rgba(26, 53, 100, 0.6) !important;
        border-radius: 20px !important;
        box-shadow: 0 16px 40px rgba(6, 13, 31, 0.8), 0 0 30px rgba(16, 31, 64, 0.3) !important;
        padding: 1.4rem !important;
    }

    /* High-Contrast Time Period Chip Badge */
    .period-chip {
        background: rgba(16, 31, 64, 0.6) !important;
        border: 1.5px solid #1A3564 !important;
        border-radius: 14px !important;
        color: #F4F7FC !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        padding: 10px 16px !important;
        margin-top: 14px !important;
        margin-bottom: 6px !important;
        display: block !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(6, 13, 31, 0.5), 0 0 15px rgba(26, 53, 100, 0.3) !important;
    }
    .period-chip, .period-chip * {
        color: #F4F7FC !important;
        font-weight: 800 !important;
    }

    /* Headings & Typography */
    h1, h2, h3, h4, h5, h6, .filter-section-title {
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        color: #F4F7FC !important;
        letter-spacing: -0.3px !important;
        margin-bottom: 10px !important;
    }
    p, span, label, div[data-testid="stMarkdownContainer"] p {
        color: #CAD5E8 !important;
    }
    div[data-testid="stCaptionContainer"] {
        color: #8397BC !important;
    }

    /* Selectbox Widget Labels */
    div[data-testid="stSelectbox"] label, label[data-testid="stWidgetLabel"] {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        color: #F4F7FC !important;
        margin-bottom: 6px !important;
    }

    /* Executive Selectbox Input Styling */
    div[data-testid="stSelectbox"] > div {
        background: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 12px rgba(6, 13, 31, 0.08) !important;
        transition: all 0.22s ease !important;
    }
    div[data-testid="stSelectbox"] > div:hover {
        border-color: #1A3564 !important;
        box-shadow: 0 6px 18px rgba(26, 53, 100, 0.3) !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #060D1F !important;
    }

    /* KPI Cards Styling (#101F40 Card Background, #14274D Hover) */
    .metric-card-exec {
        background: #101F40 !important;
        border-radius: 22px;
        padding: 1.4rem 1.1rem;
        text-align: center;
        box-shadow: 0 10px 28px rgba(6, 13, 31, 0.6), 0 0 20px rgba(16, 31, 64, 0.2);
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        border: 1.5px solid rgba(26, 53, 100, 0.45);
    }
    .metric-card-exec:hover {
        background: #14274D !important;
        transform: translateY(-6px);
        box-shadow: 0 16px 36px rgba(6, 13, 31, 0.8), 0 0 30px rgba(26, 53, 100, 0.4);
        border-color: #1A3564;
    }
    .metric-card-exec::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
    }

    /* 🟢 Headcount (Emerald Highlight) */
    .kpi-emerald {
        background: #101F40 !important;
        border-color: rgba(52, 211, 153, 0.4);
    }
    .kpi-emerald::before { background: linear-gradient(90deg, #10B981, #34D399); }
    .metric-val-emerald { font-size: 2.3rem; font-weight: 800; color: #34D399; line-height: 1.1; }
    .badge-bg-emerald { background: rgba(52, 211, 153, 0.2); color: #F4F7FC; border: 1px solid #34D399; }

    /* 🟧 Active JDA / QtQ % (Vivid Amber Gold) */
    .kpi-orange {
        background: #101F40 !important;
        border-color: rgba(255, 215, 0, 0.4);
    }
    .kpi-orange::before { background: linear-gradient(90deg, #F59E0B, #FFD700); }
    .metric-val-orange { font-size: 2.3rem; font-weight: 800; color: #FFD700; line-height: 1.1; }
    .badge-bg-orange { background: rgba(255, 215, 0, 0.2); color: #F4F7FC; border: 1px solid #FFD700; }

    /* 🟦 Active ME / YoY % (Royal Blue Accent) */
    .kpi-blue {
        background: #101F40 !important;
        border-color: rgba(96, 165, 250, 0.4);
    }
    .kpi-blue::before { background: linear-gradient(90deg, #2563EB, #60A5FA); }
    .metric-val-blue { font-size: 2.3rem; font-weight: 800; color: #60A5FA; line-height: 1.1; }
    .badge-bg-blue { background: rgba(96, 165, 250, 0.2); color: #F4F7FC; border: 1px solid #60A5FA; }

    /* 🔴 Active TME / Exited (Luminous Red) */
    .kpi-rose {
        background: #101F40 !important;
        border-color: rgba(248, 113, 113, 0.4);
    }
    .kpi-rose::before { background: linear-gradient(90deg, #EF4444, #F87171); }
    .metric-val-rose { font-size: 2.3rem; font-weight: 800; color: #F87171; line-height: 1.1; }
    .badge-bg-rose { background: rgba(248, 113, 113, 0.2); color: #F4F7FC; border: 1px solid #F87171; }

    /* 🌊 MoM % (Neon Cyan) */
    .kpi-cyan {
        background: #101F40 !important;
        border-color: rgba(0, 229, 255, 0.4);
    }
    .kpi-cyan::before { background: linear-gradient(90deg, #0284C7, #00E5FF); }
    .metric-val-cyan { font-size: 2.3rem; font-weight: 800; color: #00E5FF; line-height: 1.1; }
    .badge-bg-cyan { background: rgba(0, 229, 255, 0.2); color: #F4F7FC; border: 1px solid #00E5FF; }

    .metric-lbl-exec {
        font-size: 0.88rem;
        color: #CAD5E8;
        font-weight: 800;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .metric-badge-exec {
        display: inline-block;
        font-size: 0.8rem;
        font-weight: 800;
        padding: 5px 14px;
        border-radius: 14px;
        margin-top: 8px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.3);
    }

    /* Executive Tables Card Container (#0B1933 Table Background) */
    .custom-table-card {
        background: #0B1933 !important;
        backdrop-filter: blur(12px);
        border-radius: 22px;
        padding: 1.6rem;
        border: 1.5px solid rgba(26, 53, 100, 0.5);
        box-shadow: 0 12px 36px rgba(6, 13, 31, 0.8), 0 0 25px rgba(16, 31, 64, 0.25);
        margin-bottom: 2rem;
        overflow-x: auto;
    }
    .custom-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 16px;
        overflow: hidden;
        font-size: 1.02rem;
    }
    .custom-table th {
        background: linear-gradient(135deg, #0A1530 0%, #102142 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800;
        padding: 18px 22px;
        text-align: center;
        border-bottom: 3px solid #1A3564;
        font-size: 0.96rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .custom-table td {
        padding: 16px 22px;
        text-align: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 1.02rem;
    }
    .custom-table tr:nth-child(odd) td {
        background-color: #102142 !important; /* Table Row Normal */
    }
    .custom-table tr:nth-child(even) td {
        background-color: #14284D !important; /* Table Alt Row */
    }
    .custom-table tr:hover td {
        background-color: #1A3564 !important; /* Table Hover */
        color: #FFFFFF !important;
    }
    .custom-table tr.total-row td {
        background: linear-gradient(135deg, #1A3564 0%, #2B4C8C 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
    }

    /* Export & Download Footer Banner (#101F40 Card Background) */
    .export-footer {
        background: #101F40 !important;
        backdrop-filter: blur(12px);
        border: 1px solid #1A3564;
        border-top: 4px solid #2B4C8C;
        border-radius: 20px;
        padding: 1.8rem 2.4rem;
        margin-top: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 12px 30px rgba(6, 13, 31, 0.6), 0 0 25px rgba(16, 31, 64, 0.25);
    }
    .export-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #60A5FA;
        margin-bottom: 0.4rem;
    }

    /* Main Tab Navigation Bar (#0B1630 Background 2) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 18px !important;
        border-bottom: none !important;
        background: #0B1630 !important;
        backdrop-filter: blur(12px);
        padding: 14px 28px !important;
        border-radius: 22px !important;
        box-shadow: 0 8px 26px rgba(6, 13, 31, 0.6), 0 0 20px rgba(16, 31, 64, 0.2);
        border: 1.5px solid rgba(26, 53, 100, 0.4);
        margin-top: 2.2rem !important;
        margin-bottom: 2rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        color: #CAD5E8 !important;
        padding: 14px 38px !important;
        border-radius: 16px !important;
        transition: all 0.28s ease !important;
        border-bottom: none !important;
        white-space: nowrap !important;
        height: auto !important;
        min-height: 56px !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(26, 53, 100, 0.4) !important;
        color: #FFFFFF !important;
    }
    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        background: linear-gradient(135deg, #1A3564 0%, #2B4C8C 100%) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 22px rgba(6, 13, 31, 0.6), 0 0 20px rgba(26, 53, 100, 0.5) !important;
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab-highlight-container"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
        height: 0px !important;
        visibility: hidden !important;
    }
    .stTabs button::after {
        display: none !important;
    }

    /* Integrated Parent-Child Sub-View Segmented Control Bar (#0B1630) */
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 8px !important;
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        background: #0B1630 !important;
        padding: 6px 10px !important;
        border-radius: 18px !important;
        border: 1.5px solid rgba(26, 53, 100, 0.4) !important;
        margin-top: 12px !important;
        margin-bottom: 1.8rem !important;
        width: fit-content !important;
        box-shadow: inset 0 2px 4px rgba(6, 13, 31, 0.4), 0 0 15px rgba(16, 31, 64, 0.15) !important;
    }
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #CAD5E8 !important;
        background: transparent !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        box-shadow: none !important;
        transition: all 0.25s ease !important;
        margin-right: 0px !important;
        cursor: pointer !important;
    }
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label p,
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label span,
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        color: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
    }
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        color: #FFFFFF !important;
        background: rgba(26, 53, 100, 0.3) !important;
    }
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, #1A3564 0%, #2B4C8C 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 14px rgba(6, 13, 31, 0.6), 0 0 18px rgba(26, 53, 100, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Dataset
@st.cache_data
def load_data():
    csv_file = os.path.join(os.path.dirname(__file__), "employee_data.csv")
    if not os.path.exists(csv_file):
        df = generate_sample_dataset()
    else:
        df = pd.read_csv(csv_file)
    return df

raw_df = load_data()

# Hero Banner
st.markdown("""
<div class="command-hero-header">
    <div>
        <span class="command-badge">⚡ WORKFORCE INTELLIGENCE COMMAND</span><br>
        <span class="command-title">Analytics Employee Headcount & Tenure Dashboard</span>
        <div class="command-subtitle">Real-Time Executive Workforce Intelligence, Tenure Analytics & Drill-Down Matrix</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Bulletproof Expander State Persistence & Auto-Close Handler Script
import streamlit.components.v1 as components
components.html("""
<script>
    (function() {
        try {
            var targetDoc = window.parent.document || window.top.document;
            if (!targetDoc) return;

            var styleId = 'custom-smooth-scroll-style-p3';
            if (!targetDoc.getElementById(styleId)) {
                var style = targetDoc.createElement('style');
                style.id = styleId;
                style.innerHTML = 'html, body, div[data-testid="stAppViewContainer"], section.main { scroll-behavior: smooth !important; }';
                targetDoc.head.appendChild(style);
            }

            function getExpanderIdx(exp) {
                var all = Array.from(targetDoc.querySelectorAll('div[data-testid="stExpander"]'));
                return 'exp_idx_' + all.indexOf(exp);
            }

            function restoreOpenState() {
                var openIdx = sessionStorage.getItem('activeOpenExpanderIdx');
                if (openIdx !== null) {
                    var expanders = targetDoc.querySelectorAll('div[data-testid="stExpander"]');
                    expanders.forEach(function(exp) {
                        if (getExpanderIdx(exp) === openIdx) {
                            var d = exp.querySelector('details');
                            if (d && !d.hasAttribute('open')) {
                                d.setAttribute('open', '');
                            }
                        }
                    });
                }
            }

            if (!targetDoc._hasExpanderPersistListenerP3) {
                targetDoc._hasExpanderPersistListenerP3 = true;

                targetDoc.addEventListener('click', function(e) {
                    var opt = e.target.closest('li[role="option"]') || e.target.closest('div[role="option"]');
                    if (opt) {
                        var activePopover = targetDoc.querySelector('div[data-testid="stPopoverBody"]');
                        if (activePopover) {
                            var isTimeMode = activePopover.innerText && (activePopover.innerText.includes("Select Time Mode") || activePopover.innerText.includes("Monthly (MTD)"));
                            var optTxt = opt.innerText ? opt.innerText.trim() : "";
                            var isTodayOption = (optTxt === "Today" || optTxt.includes("Today"));
                            var isYearNumber = /^\\d{4}$/.test(optTxt);

                            if (!isTimeMode || isTodayOption || isYearNumber) {
                                setTimeout(function() {
                                    targetDoc.body.click();
                                }, 150);
                            }
                        }
                    }

                    var summary = e.target.closest('div[data-testid="stExpander"] summary');
                    var isInsideExpander = e.target.closest('div[data-testid="stExpander"]');
                    var isPopover = e.target.closest('div[data-baseweb="popover"]') || 
                                    e.target.closest('ul[role="listbox"]') || 
                                    e.target.closest('li[role="option"]') || 
                                    e.target.closest('[data-baseweb="select"]') || 
                                    e.target.closest('div[data-baseweb="calendar"]');

                    if (summary) {
                        var exp = summary.closest('div[data-testid="stExpander"]');
                        var details = exp ? exp.querySelector('details') : null;
                        setTimeout(function() {
                            if (details && details.hasAttribute('open')) {
                                sessionStorage.setItem('activeOpenExpanderIdx', getExpanderIdx(exp));
                            } else {
                                sessionStorage.removeItem('activeOpenExpanderIdx');
                            }
                        }, 50);
                    } else if (!isInsideExpander && !isPopover) {
                        sessionStorage.removeItem('activeOpenExpanderIdx');
                        var openExpanders = targetDoc.querySelectorAll('div[data-testid="stExpander"] details[open]');
                        openExpanders.forEach(function(d) { d.removeAttribute('open'); });
                    }

                    var btn = e.target.closest('button, label, [role="tab"], div[data-baseweb="tab"]');
                    if (btn) {
                        setTimeout(function() {
                            btn.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });
                        }, 100);
                    }
                }, true);

                var observer = new MutationObserver(restoreOpenState);
                observer.observe(targetDoc.body, { childList: true, subtree: true });
                setInterval(restoreOpenState, 50);
            }
        } catch(err) {
            console.error("Expander persistence notice:", err);
        }
    })();
</script>
""", height=0, width=0)

# Branch & Team Scope Lists
tme_all_teams = [
    'B2B BDE', 'BLANK', 'Bounce', 'Corporate', 'DF', 'Hot Data',
    'Multiple team', 'Online', 'Revival (Expiry)', 'SHT', 'Super', 'Super Cat', 'trainee'
]
branches_11_options = ["All 11 Cities", "Ahmedabad", "Bangalore", "Chandigarh", "Chennai", "Coimbatore", "Delhi", "Hyderabad", "Jaipur", "Kolkata", "Mumbai", "Pune"]
team_type_single_options = ["All Teams"] + tme_all_teams

if "last_active_expander" not in st.session_state:
    st.session_state["last_active_expander"] = None

def cb_time():
    st.session_state["last_active_expander"] = "time"

def cb_emp():
    st.session_state["last_active_expander"] = "emp"

def cb_city():
    st.session_state["last_active_expander"] = "city"

def cb_team():
    st.session_state["last_active_expander"] = "team"

time_filter_mode_peek = st.session_state.get("hdr_dd_time_mode", "Monthly (MTD)")
today = date.today()

if time_filter_mode_peek == "Monthly (MTD)":
    peek_year = st.session_state.get("hdr_dd_mo_year", 2026)
    month_names_peek = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    peek_month = st.session_state.get("hdr_dd_mo_month", "August")
    m_idx = month_names_peek.index(peek_month) + 1
    s_dt = pd.Timestamp(datetime(peek_year, m_idx, 1))
    if m_idx == 12:
        e_dt = pd.Timestamp(datetime(peek_year, 12, 31))
    else:
        e_dt = pd.Timestamp(datetime(peek_year, m_idx + 1, 1)) - pd.Timedelta(days=1)
    time_header_label = f"🗓️ Time Period ({peek_month[:3]} {peek_year})"

elif time_filter_mode_peek == "Quarterly":
    peek_year = st.session_state.get("hdr_dd_q_year", 2026)
    peek_q = st.session_state.get("hdr_dd_q_quarter", "Q3 (Jul-Sep)")
    sq_peek = peek_q.split(" ")[0]
    time_header_label = f"📊 Time Period ({sq_peek} {peek_year})"

elif time_filter_mode_peek == "Yearly":
    peek_year = st.session_state.get("hdr_dd_y_year", 2026)
    time_header_label = f"📆 Time Period ({peek_year})"

elif time_filter_mode_peek == "Today":
    time_header_label = f"📍 Time Period (Today {today.strftime('%d %b')})"

else:
    cal_r = st.session_state.get("hdr_dd_cal_range", (date(2026, 8, 1), date(2026, 8, 31)))
    if isinstance(cal_r, (tuple, list)) and len(cal_r) == 2:
        s_dt = pd.Timestamp(cal_r[0])
        e_dt = pd.Timestamp(cal_r[1])
        time_header_label = f"📅 Time Period ({s_dt.strftime('%d %b')} - {e_dt.strftime('%d %b')})"
    else:
        time_header_label = f"📍 Time Period (Today {today.strftime('%d %b')})"

peek_emp_type = st.session_state.get("hdr_dd_emp_type", "All EmpTypes")
emp_type_header_label = f"👤 Employee  ({peek_emp_type})"

peek_city = st.session_state.get("hdr_dd_city", "All 11 Cities")
city_header_label = f"🏢 Branch  ({peek_city})"

peek_team = st.session_state.get("hdr_dd_team", "All Teams")
team_header_label = f"👥 Team  ({peek_team})"

# ==============================================================================
# 4-CATEGORY TOP DROPDOWN FILTER HEADBAR
# ==============================================================================
filter_c1, filter_c2, filter_c3, filter_c4 = st.columns(4)

# 1. 🗓️ Time Period Category Dropdown
with filter_c1:
    with st.popover(time_header_label, use_container_width=True):
        time_filter_mode = st.selectbox(
            "Select Time Mode",
            ["Monthly (MTD)", "Quarterly", "Yearly", "Today", "Custom Calendar"],
            index=0,
            key="hdr_dd_time_mode"
        )
        
        today = date.today()
        if time_filter_mode == "Monthly (MTD)":
            sel_year = st.selectbox("Year", options=list(range(2028, 2017, -1)), index=2, key="hdr_dd_mo_year")
            month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            sel_month_name = st.selectbox("Month", options=month_names, index=7, key="hdr_dd_mo_month")
            
            sel_m_num = month_names.index(sel_month_name) + 1
            sel_y_num = sel_year
            start_date = pd.Timestamp(datetime(sel_y_num, sel_m_num, 1))
            if sel_m_num == 12:
                end_date = pd.Timestamp(datetime(sel_y_num, 12, 31))
            else:
                end_date = pd.Timestamp(datetime(sel_y_num, sel_m_num + 1, 1)) - pd.Timedelta(days=1)
            st.markdown(f'<div class="period-chip">📅 {start_date.strftime("%d %b %Y")} to {end_date.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)

        elif time_filter_mode == "Quarterly":
            sel_year = st.selectbox("Year", options=list(range(2028, 2017, -1)), index=2, key="hdr_dd_q_year")
            sel_q_name = st.selectbox("Quarter", options=["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"], index=2, key="hdr_dd_q_quarter")
            
            sq = sel_q_name.split(" ")[0]
            q_start_dates = {"Q1": datetime(sel_year, 1, 1), "Q2": datetime(sel_year, 4, 1), "Q3": datetime(sel_year, 7, 1), "Q4": datetime(sel_year, 10, 1)}
            q_end_dates = {"Q1": datetime(sel_year, 3, 31), "Q2": datetime(sel_year, 6, 30), "Q3": datetime(sel_year, 9, 30), "Q4": datetime(sel_year, 12, 31)}
            start_date = pd.Timestamp(q_start_dates[sq])
            end_date = pd.Timestamp(q_end_dates[sq])
            st.markdown(f'<div class="period-chip">📊 {start_date.strftime("%d %b %Y")} to {end_date.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)

        elif time_filter_mode == "Yearly":
            sel_year = st.selectbox("Year", options=list(range(2028, 2017, -1)), index=2, key="hdr_dd_y_year")
            start_date = pd.Timestamp(datetime(sel_year, 1, 1))
            end_date = pd.Timestamp(datetime(sel_year, 12, 31))
            st.markdown(f'<div class="period-chip">📆 01 Jan {sel_year} to 31 Dec {sel_year}</div>', unsafe_allow_html=True)

        elif time_filter_mode == "Today":
            start_date = pd.Timestamp(today)
            end_date = pd.Timestamp(today)
            st.markdown(f'<div class="period-chip">📍 Today ({start_date.strftime("%d %b %Y")})</div>', unsafe_allow_html=True)

        else: # Custom Calendar
            cal_range = st.date_input("Date Range", value=(date(2026, 8, 1), date(2026, 8, 31)), min_value=date(2018, 1, 1), max_value=date(2028, 12, 31), key="hdr_dd_cal_range")
            if isinstance(cal_range, (tuple, list)) and len(cal_range) == 2:
                start_date = pd.Timestamp(cal_range[0])
                end_date = pd.Timestamp(cal_range[1])
                st.markdown(f'<div class="period-chip">📅 {start_date.strftime("%d %b %Y")} to {end_date.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
            else:
                start_date = pd.Timestamp(today)
                end_date = pd.Timestamp(today)

# 2. 👤 Employee Scope Category Dropdown
with filter_c2:
    with st.popover(emp_type_header_label, use_container_width=True):
        emp_type_option = st.selectbox(
            "Select Employee Type",
            ["All EmpTypes", "JDA", "ME", "TME", "JDS"],
            index=0,
            key="hdr_dd_emp_type"
        )

# 3. 🏢 Branch Scope Category Dropdown
with filter_c3:
    with st.popover(city_header_label, use_container_width=True):
        selected_city_single = st.selectbox(
            "Select Branch/City",
            branches_11_options,
            index=0,
            key="hdr_dd_city"
        )

# 4. 👥 Team Scope Category Dropdown
with filter_c4:
    with st.popover(team_header_label, use_container_width=True):
        selected_team_single = st.selectbox(
            "Select Team Scope",
            team_type_single_options,
            index=0,
            key="hdr_dd_team"
        )

# Process EmpType, City, Team
if emp_type_option == "JDA":
    selected_emp_types = ["JDA"]
elif emp_type_option == "ME":
    selected_emp_types = ["ME"]
elif emp_type_option == "TME":
    selected_emp_types = ["TME"]
elif emp_type_option == "JDS":
    selected_emp_types = ["ME", "TME"]
else:
    selected_emp_types = ["All"]

if selected_city_single == "All 11 Cities":
    selected_branches = branches_11_options[1:]
else:
    selected_branches = [selected_city_single]
jda_city_selected = "All"

if selected_team_single == "All Teams":
    selected_teams = tme_all_teams
else:
    selected_teams = [selected_team_single]

# Execute Filter Engine
df_filtered = calculate_tenure_and_filter(
    raw_df,
    start_date=start_date,
    end_date=end_date,
    selected_emp_types=selected_emp_types,
    selected_branches=selected_branches,
    selected_teams=selected_teams,
    sda_city=jda_city_selected
)

# Main Metrics
total_count = len(df_filtered)
if total_count > 0:
    active_df = df_filtered[df_filtered['status_as_of_obs'] == 'Active']
    active_count = len(active_df)
    exited_count = len(df_filtered[df_filtered['status_as_of_obs'] == 'Exited'])
    
    active_jda_count = len(active_df[active_df['emp_type'] == 'JDA'])
    active_me_count = len(active_df[active_df['emp_type'] == 'ME'])
    active_tme_count = len(active_df[active_df['emp_type'] == 'TME'])
    
    avg_tenure_m = round(df_filtered['tenure_months'].mean(), 1)
    avg_tenure_y = round(df_filtered['tenure_years'].mean(), 2)
    median_tenure_m = round(df_filtered['tenure_months'].median(), 1)
    min_tenure_m = round(df_filtered['tenure_months'].min(), 1)
    max_tenure_m = round(df_filtered['tenure_months'].max(), 1)
else:
    active_count = 0
    exited_count = 0
    active_jda_count = 0
    active_me_count = 0
    active_tme_count = 0
    avg_tenure_m = 0.0
    avg_tenure_y = 0.0
    median_tenure_m = 0.0
    min_tenure_m = 0.0
    max_tenure_m = 0.0

# Calculate YoY %, MoM %, QtQ % for 5-card view
def compute_prior_active(df_raw, target_dt, emp_types, branches, teams):
    try:
        df_p = calculate_tenure_and_filter(
            df_raw,
            start_date=target_dt - pd.Timedelta(days=30),
            end_date=target_dt,
            selected_emp_types=emp_types,
            selected_branches=branches,
            selected_teams=teams,
            sda_city="All"
        )
        if not df_p.empty:
            return (df_p['status_as_of_obs'] == 'Active').sum()
    except Exception:
        pass
    return 0

mom_target = end_date - pd.DateOffset(months=1)
qtq_target = end_date - pd.DateOffset(months=3)
yoy_target = end_date - pd.DateOffset(years=1)

mom_count = compute_prior_active(raw_df, mom_target, selected_emp_types, selected_branches, selected_teams)
qtq_count = compute_prior_active(raw_df, qtq_target, selected_emp_types, selected_branches, selected_teams)
yoy_count = compute_prior_active(raw_df, yoy_target, selected_emp_types, selected_branches, selected_teams)

mom_str = f"{'+' if ((active_count - mom_count) / max(mom_count, 1) * 100) >= 0 else ''}{round(((active_count - mom_count) / max(mom_count, 1)) * 100, 1)}%" if mom_count > 0 else "+0.0%"
qtq_str = f"{'+' if ((active_count - qtq_count) / max(qtq_count, 1) * 100) >= 0 else ''}{round(((active_count - qtq_count) / max(qtq_count, 1)) * 100, 1)}%" if qtq_count > 0 else "+0.0%"
yoy_str = f"{'+' if ((active_count - yoy_count) / max(yoy_count, 1) * 100) >= 0 else ''}{round(((active_count - yoy_count) / max(yoy_count, 1)) * 100, 1)}%" if yoy_count > 0 else "+0.0%"

# ==============================================================================
# TOP EXECUTIVE KPI METRIC CARDS
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)

if emp_type_option == "All EmpTypes":
    # 4 CARDS VIEW: Headcount, Active JDA, Active ME, Active TME
    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f'''
    <div class="metric-card-exec kpi-emerald">
        <div class="metric-val-emerald">{active_count}</div>
        <div class="metric-lbl-exec">Headcount</div>
        <div class="metric-badge-exec badge-bg-emerald">🏢 Total Active</div>
    </div>
    ''', unsafe_allow_html=True)

    c2.markdown(f'''
    <div class="metric-card-exec kpi-orange">
        <div class="metric-val-orange">{active_jda_count}</div>
        <div class="metric-lbl-exec">Active JDA</div>
        <div class="metric-badge-exec badge-bg-orange">🟧 Active JDA</div>
    </div>
    ''', unsafe_allow_html=True)

    c3.markdown(f'''
    <div class="metric-card-exec kpi-blue">
        <div class="metric-val-blue">{active_me_count}</div>
        <div class="metric-lbl-exec">Active ME</div>
        <div class="metric-badge-exec badge-bg-blue">🟦 Active ME</div>
    </div>
    ''', unsafe_allow_html=True)

    c4.markdown(f'''
    <div class="metric-card-exec kpi-rose">
        <div class="metric-val-rose">{active_tme_count}</div>
        <div class="metric-lbl-exec">Active TME</div>
        <div class="metric-badge-exec badge-bg-rose">🔴 Active TME</div>
    </div>
    ''', unsafe_allow_html=True)

else:
    # 5 CARDS VIEW: Headcount, Exited in Period, YoY %, MoM %, QtQ %
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.markdown(f'''
    <div class="metric-card-exec kpi-emerald">
        <div class="metric-val-emerald">{active_count}</div>
        <div class="metric-lbl-exec">Headcount</div>
        <div class="metric-badge-exec badge-bg-emerald">🏢 Active ({emp_type_option})</div>
    </div>
    ''', unsafe_allow_html=True)

    c2.markdown(f'''
    <div class="metric-card-exec kpi-rose">
        <div class="metric-val-rose">{exited_count}</div>
        <div class="metric-lbl-exec">Exited in Period</div>
        <div class="metric-badge-exec badge-bg-rose">🔴 Exited Count</div>
    </div>
    ''', unsafe_allow_html=True)

    c3.markdown(f'''
    <div class="metric-card-exec kpi-blue">
        <div class="metric-val-blue">{yoy_str}</div>
        <div class="metric-lbl-exec">YoY % Change</div>
        <div class="metric-badge-exec badge-bg-blue">📈 Year-over-Year</div>
    </div>
    ''', unsafe_allow_html=True)

    c4.markdown(f'''
    <div class="metric-card-exec kpi-cyan">
        <div class="metric-val-cyan">{mom_str}</div>
        <div class="metric-lbl-exec">MoM % Change</div>
        <div class="metric-badge-exec badge-bg-cyan">📊 Month-over-Month</div>
    </div>
    ''', unsafe_allow_html=True)

    c5.markdown(f'''
    <div class="metric-card-exec kpi-orange">
        <div class="metric-val-orange">{qtq_str}</div>
        <div class="metric-lbl-exec">QtQ % Change</div>
        <div class="metric-badge-exec badge-bg-orange">🗓️ Quarter-over-Quarter</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Global Download Footer Function
def render_download_section(section_id="default"):
    st.markdown(f"""
    <div class="export-footer">
        <div class="export-title">📥 Download Filtered Employee Dataset</div>
        <div style="font-size: 0.92rem; color: #60A5FA; margin-bottom: 0.9rem; font-weight:600;">
            Export complete employee dataset matching your criteria for period <b>{start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')}</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if df_filtered.empty:
        st.info("No employee data available to download.")
        return

    raw_cols = [
        "emp_code", "emp_name", "branch", "emp_type", "team_type",
        "doj", "dol", "status_as_of_obs", "tenure_months", "tenure_years", "tenure_days",
        "designation", "email", "phone"
    ]
    export_cols = [c for c in raw_cols if c in df_filtered.columns]
    
    col_rename_map = {
        "emp_code": "Emp Code",
        "emp_name": "Employee Name",
        "branch": "Branch/City",
        "emp_type": "Emp Type",
        "team_type": "Team Type",
        "doj": "DOJ",
        "dol": "DOL",
        "status_as_of_obs": f"Status (in period {start_date.strftime('%b %Y')})",
        "tenure_months": "Exact Tenure (Months)",
        "tenure_years": "Exact Tenure (Years)",
        "tenure_days": "Exact Tenure (Days)",
        "designation": "Designation",
        "email": "Email",
        "phone": "Phone"
    }
    
    final_table = df_filtered[export_cols].rename(columns={k: v for k, v in col_rename_map.items() if k in export_cols})
    
    dl_col1, dl_col2, _ = st.columns([1.5, 1.5, 2])
    
    csv_bytes = final_table.to_csv(index=False).encode('utf-8')
    dl_col1.download_button(
        label="📄 Download CSV Data",
        data=csv_bytes,
        file_name=f"Employee_Tenure_{end_date.strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True,
        key=f"btn_dl_csv_{section_id}"
    )
    
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        final_table.to_excel(writer, index=False, sheet_name='Tenure Data')
    excel_data = excel_buffer.getvalue()
    
    dl_col2.download_button(
        label="📊 Download Excel (.xlsx) Data",
        data=excel_data,
        file_name=f"Employee_Tenure_{end_date.strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key=f"btn_dl_xlsx_{section_id}"
    )

# ==============================================================================
# MAIN DASHBOARD NAVIGATION
# ==============================================================================
st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)

main_tab1, main_tab2, main_tab3 = st.tabs([
    "🔢 Employee Headcount",
    "📈 Tenure Breakdown",
    "📋 Employee Drill-Down"
])

# ------------------------------------------------------------------------------
# TAB 1: EMPLOYEE HEADCOUNT SUMMARY
# ------------------------------------------------------------------------------
with main_tab1:
    if df_filtered.empty:
        st.warning("No records matching filter criteria.")
    else:
        s_mode = st.radio(
            "Select Headcount Summary Scope",
            options=["📊 Pan India / Branch Summary", "👥 Team Type Summary"],
            index=0,
            horizontal=True,
            key="headcount_summary_pill_toggle",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        is_pan_india = (selected_city_single == "All 11 Cities" or selected_branches == branches_11_options[1:])
        
        if s_mode == "📊 Pan India / Branch Summary":
            st.markdown(f"#### 📊 {'Pan India' if is_pan_india else selected_branches[0]} Headcount Summary")
            
            br_hc_df = df_filtered.groupby('branch').agg(
                Active_Count=('status_as_of_obs', lambda x: (x == 'Active').sum()),
                Exited_Count=('status_as_of_obs', lambda x: (x == 'Exited').sum())
            ).reset_index()
            br_hc_df['Total_Scope'] = br_hc_df['Active_Count'] + br_hc_df['Exited_Count']
            br_hc_df['Active_Pct'] = br_hc_df.apply(lambda r: f"{round(r['Active_Count']/r['Total_Scope']*100, 1)}%" if r['Total_Scope'] > 0 else "0.0%", axis=1)
            
            html_b = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            html_b.append('<th>Branch / City</th><th>Headcount</th><th>Exited in Period</th><th>Retention Share (%)</th>')
            html_b.append('</tr></thead><tbody>')
            for _, r in br_hc_df.iterrows():
                html_b.append('<tr>')
                html_b.append(f'<td style="font-weight:700; text-align:left; color:#FFD700;">{r["branch"]}</td>')
                html_b.append(f'<td style="color:#34D399; font-weight:800;">{r["Active_Count"]}</td>')
                html_b.append(f'<td style="color:#F87171; font-weight:700;">{r["Exited_Count"]}</td>')
                html_b.append(f'<td style="color:#60A5FA; font-weight:800;">{r["Active_Pct"]}</td>')
                html_b.append('</tr>')
            html_b.append('</tbody></table></div>')
            st.markdown("".join(html_b), unsafe_allow_html=True)

        else: # 👥 Team Type Summary
            st.markdown("#### 👥 Team Type Headcount Summary")
            team_hc_df = df_filtered.groupby('team_type').agg(
                Active_Count=('status_as_of_obs', lambda x: (x == 'Active').sum()),
                Exited_Count=('status_as_of_obs', lambda x: (x == 'Exited').sum())
            ).reset_index().sort_values(by='Active_Count', ascending=False)
            team_hc_df['Total_Scope'] = team_hc_df['Active_Count'] + team_hc_df['Exited_Count']
            team_hc_df['Active_Pct'] = team_hc_df.apply(lambda r: f"{round(r['Active_Count']/r['Total_Scope']*100, 1)}%" if r['Total_Scope'] > 0 else "0.0%", axis=1)
            
            html_t = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            html_t.append('<th>Team Type</th><th>Headcount</th><th>Exited in Period</th><th>Retention Share (%)</th>')
            html_t.append('</tr></thead><tbody>')
            for _, r in team_hc_df.iterrows():
                html_t.append('<tr>')
                html_t.append(f'<td style="font-weight:700; text-align:left; color:#FFD700;">{r["team_type"]}</td>')
                html_t.append(f'<td style="color:#34D399; font-weight:800;">{r["Active_Count"]}</td>')
                html_t.append(f'<td style="color:#F87171; font-weight:700;">{r["Exited_Count"]}</td>')
                html_t.append(f'<td style="color:#60A5FA; font-weight:800;">{r["Active_Pct"]}</td>')
                html_t.append('</tr>')
            html_t.append('</tbody></table></div>')
            st.markdown("".join(html_t), unsafe_allow_html=True)

    render_download_section("tab1_headcount_summary")

# ------------------------------------------------------------------------------
# TAB 2: TENURE BREAKDOWN & MATRICES
# ------------------------------------------------------------------------------
with main_tab2:
    if df_filtered.empty:
        st.warning("No data matching selected filter criteria.")
    else:
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

        bucket_order = ["< 6 Months", "6 - 12 Months", "1 - 2 Years", "2 - 3 Years", "3 - 5 Years", "5+ Years"]
        df_filtered['tenure_bucket'] = df_filtered['tenure_months'].apply(assign_tenure_bucket)

        v_mode = st.radio(
            "Select Tenure View",
            options=["⏳ Overall Tenure Buckets", "🏢 Branch-Wise Tenure Matrix Table", "👥 Team-Wise Tenure Matrix Table"],
            index=0,
            horizontal=True,
            key="tenure_view_pill_toggle",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)

        if v_mode == "⏳ Overall Tenure Buckets":
            st.markdown(f"#### ⏳ Headcount & Exited in Period by Tenure Buckets ({start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')})")
            
            tb_df = df_filtered.groupby('tenure_bucket').agg(
                Total_Headcount=('emp_code', 'count'),
                Active_Count=('status_as_of_obs', lambda x: (x == 'Active').sum()),
                Exited_Count=('status_as_of_obs', lambda x: (x == 'Exited').sum())
            ).reindex(bucket_order).fillna(0).reset_index()
            
            tb_df['Active_Pct'] = tb_df.apply(
                lambda r: f"{round(r['Active_Count']/r['Total_Headcount']*100, 1)}%" if r['Total_Headcount'] > 0 else "0.0%", axis=1
            )
            
            html_tb = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            html_tb.append('<th>Tenure Bucket</th><th>Headcount</th><th>Exited in Period</th><th>Retention Share (%)</th>')
            html_tb.append('</tr></thead><tbody>')
            for _, r in tb_df.iterrows():
                html_tb.append('<tr>')
                html_tb.append(f'<td style="font-weight:700; text-align:left; color:#FFD700;">{r["tenure_bucket"]}</td>')
                html_tb.append(f'<td style="color:#34D399; font-weight:800;">{int(r["Active_Count"])}</td>')
                html_tb.append(f'<td style="color:#F87171; font-weight:700;">{int(r["Exited_Count"])}</td>')
                html_tb.append(f'<td style="color:#60A5FA; font-weight:800;">{r["Active_Pct"]}</td>')
                html_tb.append('</tr>')
            html_tb.append('</tbody></table></div>')
            st.markdown("".join(html_tb), unsafe_allow_html=True)

        elif v_mode == "🏢 Branch-Wise Tenure Matrix Table":
            st.markdown("#### 🏢 Branch-Wise Headcount Bucket Matrix Table")
            b_pivot = pd.crosstab(df_filtered['branch'], df_filtered['tenure_bucket']).reindex(columns=bucket_order, fill_value=0).reset_index()
            b_pivot['Headcount'] = b_pivot[bucket_order].sum(axis=1)
            
            html_bp = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            html_bp.append('<th>Branch / City</th>')
            for bo in bucket_order:
                html_bp.append(f'<th>{bo}</th>')
            html_bp.append('<th>Headcount</th></tr></thead><tbody>')
            
            for _, r in b_pivot.iterrows():
                html_bp.append('<tr>')
                html_bp.append(f'<td style="font-weight:700; text-align:left; color:#FFD700;">{r["branch"]}</td>')
                for bo in bucket_order:
                    html_bp.append(f'<td>{r[bo]}</td>')
                html_bp.append(f'<td style="font-weight:800; color:#60A5FA;">{r["Headcount"]}</td>')
                html_bp.append('</tr>')
            html_bp.append('</tbody></table></div>')
            st.markdown("".join(html_bp), unsafe_allow_html=True)

        else: # 👥 Team-Wise Tenure Matrix
            st.markdown("#### 👥 Team Type Wise Headcount Bucket Matrix Table")
            t_pivot = pd.crosstab(df_filtered['team_type'], df_filtered['tenure_bucket']).reindex(columns=bucket_order, fill_value=0).reset_index()
            t_pivot['Headcount'] = t_pivot[bucket_order].sum(axis=1)
            
            html_tp = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            html_tp.append('<th>Team Type</th>')
            for bo in bucket_order:
                html_tp.append(f'<th>{bo}</th>')
            html_tp.append('<th>Headcount</th></tr></thead><tbody>')
            
            for _, r in t_pivot.iterrows():
                html_tp.append('<tr>')
                html_tp.append(f'<td style="font-weight:700; text-align:left; color:#FFD700;">{r["team_type"]}</td>')
                for bo in bucket_order:
                    html_tp.append(f'<td>{r[bo]}</td>')
                html_tp.append(f'<td style="font-weight:800; color:#60A5FA;">{r["Headcount"]}</td>')
                html_tp.append('</tr>')
            html_tp.append('</tbody></table></div>')
            st.markdown("".join(html_tp), unsafe_allow_html=True)

    render_download_section("tab2_tenure_breakdown")

# ------------------------------------------------------------------------------
# TAB 3: EMPLOYEE DRILL-DOWN & DATA MATRICES
# ------------------------------------------------------------------------------
with main_tab3:
    d_mode = st.radio(
        "Select Drill-Down View",
        options=["🔍 Searchable Employee List", "🏢 Branch List", "👥 Team List", "🚪 Exited Employees"],
        index=0,
        horizontal=True,
        key="drilldown_view_pill_toggle",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if d_mode == "🔍 Searchable Employee List":
        search_q = st.text_input("Search Active Employees", placeholder="🔍 Search Active Employees by Name or Emp Code...", key="drill_search_box", label_visibility="collapsed")
        
        display_df = df_filtered[df_filtered['status_as_of_obs'] == 'Active'].copy()
        if search_q:
            mask = (
                display_df['emp_name'].str.contains(search_q, case=False, na=False) |
                display_df['emp_code'].str.contains(search_q, case=False, na=False)
            )
            display_df = display_df[mask]
            
        if display_df.empty:
            st.info("No matching active employee records found.")
        else:
            html5 = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            html5.append('<th>Emp Code</th><th>Employee Name</th><th>Branch</th><th>Type</th><th>Team Type</th><th>DOJ</th><th>DOL</th><th>Exact Months</th><th>Exact Years</th><th>Exact Days</th><th>Designation</th>')
            html5.append('</tr></thead><tbody>')
            
            for _, r in display_df.head(100).iterrows():
                dol_str = r['dol'] if pd.notnull(r['dol']) and str(r['dol']).strip() != "" else "-"
                
                html5.append('<tr>')
                html5.append(f'<td style="font-weight:700; color:#FFD700;">{r["emp_code"]}</td>')
                html5.append(f'<td style="text-align:left; font-weight:700; color:#FFFFFF;">{r["emp_name"]}</td>')
                html5.append(f'<td style="color:#60A5FA;">{r["branch"]}</td>')
                html5.append(f'<td><b style="color:#34D399;">{r["emp_type"]}</b></td>')
                html5.append(f'<td>{r["team_type"]}</td>')
                html5.append(f'<td>{r["doj"]}</td>')
                html5.append(f'<td>{dol_str}</td>')
                html5.append(f'<td style="font-weight:800; color:#34D399;">{r["tenure_months"]} M</td>')
                html5.append(f'<td>{r["tenure_years"]} Yrs</td>')
                html5.append(f'<td>{r["tenure_days"]} Days</td>')
                html5.append(f'<td style="font-size:0.9rem; color:#CAD5E8;">{r["designation"]}</td>')
                html5.append('</tr>')
                
            html5.append('</tbody></table></div>')
            st.markdown("".join(html5), unsafe_allow_html=True)
            st.caption(f"Displaying top **100** of **{len(display_df)}** matching active employee records.")

    elif d_mode == "🏢 Branch List":
        st.markdown("#### 🏢 Branch-Wise Table")
        if df_filtered.empty:
            st.warning("No records matching filter criteria.")
        else:
            branch_stats = df_filtered.groupby('branch').agg(
                Active_Count=('status_as_of_obs', lambda x: (x == 'Active').sum()),
                Exited_Count=('status_as_of_obs', lambda x: (x == 'Exited').sum()),
                Avg_Tenure_Months=('tenure_months', lambda x: round(x.mean(), 1)),
                Avg_Tenure_Years=('tenure_years', lambda x: round(x.mean(), 2)),
                Median_Tenure_Months=('tenure_months', lambda x: round(x.median(), 1)),
                Min_Tenure_Months=('tenure_months', lambda x: round(x.min(), 1)),
                Max_Tenure_Months=('tenure_months', lambda x: round(x.max(), 1))
            ).reset_index().rename(columns={
                'branch': 'Branch / City',
                'Active_Count': 'Headcount',
                'Exited_Count': 'Exited in Period',
                'Avg_Tenure_Months': 'Exact Avg Tenure (Months)',
                'Avg_Tenure_Years': 'Exact Avg Tenure (Years)',
                'Median_Tenure_Months': 'Exact Median (Months)',
                'Min_Tenure_Months': 'Exact Min (Months)',
                'Max_Tenure_Months': 'Exact Max (Months)'
            })
            
            tot_b_row = {
                'Branch / City': 'TOTAL (Selected Cities)',
                'Headcount': active_count,
                'Exited in Period': exited_count,
                'Exact Avg Tenure (Months)': avg_tenure_m,
                'Exact Avg Tenure (Years)': avg_tenure_y,
                'Exact Median (Months)': median_tenure_m,
                'Exact Min (Months)': min_tenure_m,
                'Exact Max (Months)': max_tenure_m
            }
            full_b_df = pd.concat([branch_stats, pd.DataFrame([tot_b_row])], ignore_index=True)
            
            html3 = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            html3.append('<th>Branch / City</th><th>Headcount</th><th>Exited in Period</th><th>Exact Avg (Months)</th><th>Exact Avg (Years)</th><th>Median (M)</th><th>Min (M)</th><th>Max (M)</th>')
            html3.append('</tr></thead><tbody>')
            
            for _, r in full_b_df.iterrows():
                is_tot = str(r['Branch / City']).startswith("TOTAL")
                tr_cls = 'class="total-row"' if is_tot else ''
                
                html3.append(f'<tr {tr_cls}>')
                html3.append(f'<td style="text-align:left; font-weight:700; color:#FFD700;">{r["Branch / City"]}</td>')
                html3.append(f'<td style="color:#34D399; font-weight:800;">{r["Headcount"]}</td>')
                html3.append(f'<td style="color:#F87171; font-weight:700;">{r["Exited in Period"]}</td>')
                html3.append(f'<td style="font-weight:800; color:#60A5FA;">{r["Exact Avg Tenure (Months)"]} M</td>')
                html3.append(f'<td>{r["Exact Avg Tenure (Years)"]} Yrs</td>')
                html3.append(f'<td>{r["Exact Median (Months)"]} M</td>')
                html3.append(f'<td>{r["Exact Min (Months)"]} M</td>')
                html3.append(f'<td>{r["Exact Max (Months)"]} M</td>')
                html3.append('</tr>')
                
            html3.append('</tbody></table></div>')
            st.markdown("".join(html3), unsafe_allow_html=True)

    elif d_mode == "👥 Team List":
        st.markdown("#### 👥 Team-Wise Table")
        if df_filtered.empty:
            st.warning("No records matching filter criteria.")
        else:
            team_stats = df_filtered.groupby('team_type').agg(
                Active_Count=('status_as_of_obs', lambda x: (x == 'Active').sum()),
                Exited_Count=('status_as_of_obs', lambda x: (x == 'Exited').sum()),
                Avg_Tenure_Months=('tenure_months', lambda x: round(x.mean(), 1)),
                Avg_Tenure_Years=('tenure_years', lambda x: round(x.mean(), 2)),
                Median_Tenure_Months=('tenure_months', lambda x: round(x.median(), 1)),
                Min_Tenure_Months=('tenure_months', lambda x: round(x.min(), 1)),
                Max_Tenure_Months=('tenure_months', lambda x: round(x.max(), 1))
            ).reset_index().rename(columns={
                'team_type': 'Team Type',
                'Active_Count': 'Headcount',
                'Exited_Count': 'Exited in Period',
                'Avg_Tenure_Months': 'Exact Avg Tenure (Months)',
                'Avg_Tenure_Years': 'Exact Avg Tenure (Years)',
                'Median_Tenure_Months': 'Exact Median (Months)',
                'Min_Tenure_Months': 'Exact Min (Months)',
                'Max_Tenure_Months': 'Exact Max (Months)'
            })
            
            tot_t_row = {
                'Team Type': 'TOTAL (Selected Teams)',
                'Headcount': active_count,
                'Exited in Period': exited_count,
                'Exact Avg Tenure (Months)': avg_tenure_m,
                'Exact Avg Tenure (Years)': avg_tenure_y,
                'Exact Median (Months)': median_tenure_m,
                'Exact Min (Months)': min_tenure_m,
                'Exact Max (Months)': max_tenure_m
            }
            full_t_df = pd.concat([team_stats, pd.DataFrame([tot_t_row])], ignore_index=True)
            
            html4 = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            html4.append('<th>Team Type</th><th>Headcount</th><th>Exited in Period</th><th>Exact Avg (Months)</th><th>Exact Avg (Years)</th><th>Median (M)</th><th>Min (M)</th><th>Max (M)</th>')
            html4.append('</tr></thead><tbody>')
            
            for _, r in full_t_df.iterrows():
                is_tot = str(r['Team Type']).startswith("TOTAL")
                tr_cls = 'class="total-row"' if is_tot else ''
                
                html4.append(f'<tr {tr_cls}>')
                html4.append(f'<td style="text-align:left; font-weight:700; color:#FFD700;">{r["Team Type"]}</td>')
                html4.append(f'<td style="color:#34D399; font-weight:800;">{r["Headcount"]}</td>')
                html4.append(f'<td style="color:#F87171; font-weight:700;">{r["Exited in Period"]}</td>')
                html4.append(f'<td style="font-weight:800; color:#60A5FA;">{r["Exact Avg Tenure (Months)"]} M</td>')
                html4.append(f'<td>{r["Exact Avg Tenure (Years)"]} Yrs</td>')
                html4.append(f'<td>{r["Exact Median (Months)"]} M</td>')
                html4.append(f'<td>{r["Exact Min (Months)"]} M</td>')
                html4.append(f'<td>{r["Exact Max (Months)"]} M</td>')
                html4.append('</tr>')
                
            html4.append('</tbody></table></div>')
            st.markdown("".join(html4), unsafe_allow_html=True)

    else:
        st.markdown(f"#### 🔴 Employees Who Left (Exited) in Selected Period ({start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')})")
        exited_df = df_filtered[df_filtered['status_as_of_obs'] == 'Exited'].copy()
        
        if exited_df.empty:
            st.info("No employees exited during the selected period.")
        else:
            st.write(f"Total **{len(exited_df)}** employee(s) exited during this period:")
            
            html_ex = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            html_ex.append('<th>Emp Code</th><th>Employee Name</th><th>Branch</th><th>Type</th><th>Team Type</th><th>DOJ</th><th>DOL (Exit Date)</th><th>Exact Months</th><th>Exact Years</th><th>Designation</th><th>Email</th><th>Phone</th>')
            html_ex.append('</tr></thead><tbody>')
            
            for _, r in exited_df.iterrows():
                dol_str = r['dol'] if pd.notnull(r['dol']) and str(r['dol']).strip() != "" else "-"
                
                html_ex.append('<tr>')
                html_ex.append(f'<td style="font-weight:700; color:#F87171;">{r["emp_code"]}</td>')
                html_ex.append(f'<td style="text-align:left; font-weight:700; color:#FFFFFF;">{r["emp_name"]}</td>')
                html_ex.append(f'<td>{r["branch"]}</td>')
                html_ex.append(f'<td><b>{r["emp_type"]}</b></td>')
                html_ex.append(f'<td>{r["team_type"]}</td>')
                html_ex.append(f'<td>{r["doj"]}</td>')
                html_ex.append(f'<td style="color:#F87171; font-weight:800;">{dol_str}</td>')
                html_ex.append(f'<td style="font-weight:800; color:#60A5FA;">{r["tenure_months"]} M</td>')
                html_ex.append(f'<td>{r["tenure_years"]} Yrs</td>')
                html_ex.append(f'<td style="font-size:0.9rem; color:#CAD5E8;">{r["designation"]}</td>')
                html_ex.append(f'<td style="font-size:0.88rem;">{r["email"]}</td>')
                html_ex.append(f'<td style="font-size:0.88rem;">{r["phone"]}</td>')
                html_ex.append('</tr>')
                
            html_ex.append('</tbody></table></div>')
            st.markdown("".join(html_ex), unsafe_allow_html=True)
            
            raw_ex_cols = ["emp_code", "emp_name", "branch", "emp_type", "team_type", "doj", "dol", "tenure_months", "tenure_years", "tenure_days", "designation", "email", "phone"]
            ex_export_cols = [c for c in raw_ex_cols if c in exited_df.columns]
            ex_rename = {
                "emp_code": "Emp Code", "emp_name": "Employee Name", "branch": "Branch/City", "emp_type": "Emp Type",
                "team_type": "Team Type", "doj": "DOJ", "dol": "Date of Leaving (DOL)", "tenure_months": "Tenure (Months)",
                "tenure_years": "Tenure (Years)", "tenure_days": "Tenure (Days)", "designation": "Designation",
                "email": "Email", "phone": "Phone"
            }
            ex_final_table = exited_df[ex_export_cols].rename(columns={k: v for k, v in ex_rename.items() if k in ex_export_cols})
            
            ex_dl1, ex_dl2, _ = st.columns([2, 2, 2])
            ex_csv_bytes = ex_final_table.to_csv(index=False).encode('utf-8')
            ex_dl1.download_button(
                label="📄 Download Exited Employees CSV",
                data=ex_csv_bytes,
                file_name=f"Exited_Employees_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                key="btn_dl_exited_csv"
            )
            
            ex_excel_buffer = io.BytesIO()
            with pd.ExcelWriter(ex_excel_buffer, engine='openpyxl') as writer:
                ex_final_table.to_excel(writer, index=False, sheet_name='Exited Employees')
            ex_excel_data = ex_excel_buffer.getvalue()
            
            ex_dl2.download_button(
                label="📊 Download Exited Employees Excel (.xlsx)",
                data=ex_excel_data,
                file_name=f"Exited_Employees_{end_date.strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="btn_dl_exited_xlsx"
            )

    render_download_section("tab3_drilldown_matrices")
