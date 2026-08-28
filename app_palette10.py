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
    page_title="Workforce Intelligence Executive Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Palette 10: Executive Analytics Soft Velvet Purple Theme System (#F5F3F8, #50377C -> #63458C)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body {
        scroll-behavior: smooth !important;
    }

    .stApp {
        background-color: #F5F3F8 !important;
        background-image: 
            radial-gradient(at 50% 0%, #EFEAF5 0%, transparent 75%),
            radial-gradient(at 0% 100%, #F5F3F8 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(234, 226, 243, 0.6) 0px, transparent 50%);
        background-attachment: fixed;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #2D263B !important;
    }

    /* Executive Command Hero Header (#50377C -> #63458C Rich Purple Gradient) */
    .command-hero-header {
        position: relative;
        background: linear-gradient(135deg, #50377C 0%, #63458C 100%) !important;
        padding: 2.2rem 3.0rem;
        border-radius: 12px;
        color: #FFFFFF !important;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 16px rgba(80, 55, 124, 0.15);
        border: 1px solid #63458C;
        overflow: hidden;
    }
    .command-hero-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3.5px;
        background: linear-gradient(90deg, #63458C 0%, #835CAE 40%, #2E9B72 80%, #50377C 100%);
    }
    .command-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.16);
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.3);
        font-weight: 800;
        font-size: 0.95rem;
        padding: 5px 14px;
        border-radius: 8px;
        backdrop-filter: blur(4px);
        letter-spacing: 0.8px;
    }
    .header-tag-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.12);
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.25);
        font-weight: 800;
        font-size: 0.9rem;
        padding: 4px 12px;
        border-radius: 8px;
        backdrop-filter: blur(4px);
        letter-spacing: 0.6px;
    }
    .header-accent-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 10px;
        padding: 1.1rem 1.4rem;
        box-shadow: 0 4px 14px rgba(40, 20, 70, 0.15);
    }
    .command-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: #FFFFFF !important;
        letter-spacing: -0.8px;
        line-height: 1.1;
        margin-top: 4px;
    }
    .command-subtitle {
        font-size: 1.15rem;
        color: #F5F1FA !important;
        margin-top: 6px;
        font-weight: 650;
    }

    /* Popover Trigger Buttons (#FFFFFF with subtle border) */
    div[data-testid="stPopover"] {
        width: 100% !important;
        margin-bottom: 1.2rem !important;
    }
    div[data-testid="stPopover"] button,
    button[data-testid="stPopoverButton"],
    button[data-testid="stBaseButton-secondary"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E2D9EC !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(80, 55, 124, 0.05) !important;
        padding: 0.85rem 1.1rem !important;
        width: 100% !important;
        color: #2D263B !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stPopover"] button:hover,
    button[data-testid="stPopoverButton"]:hover {
        background: #F8F5FC !important;
        background-color: #F8F5FC !important;
        border-color: #563D7C !important;
        box-shadow: 0 4px 12px rgba(86, 61, 124, 0.1) !important;
    }
    div[data-testid="stPopover"] button *,
    button[data-testid="stPopoverButton"] *,
    button[data-testid="stPopoverButton"] p,
    button[data-testid="stPopoverButton"] span,
    button[data-testid="stPopoverButton"] div,
    button[data-testid="stPopoverButton"] svg {
        color: #2D263B !important;
        fill: #2D263B !important;
        font-weight: 850 !important;
        font-size: 1.2rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* Popover Body Content Overlay Cards */
    div[data-testid="stPopoverBody"] {
        background: #FFFFFF !important;
        border: 1px solid #E2D9EC !important;
        border-radius: 12px !important;
        box-shadow: 0 12px 32px rgba(80, 55, 124, 0.16) !important;
        padding: 1.2rem !important;
    }

    /* Top Executive KPI Metric Cards (Clean White with Subtle Tinted Accents) */
    .metric-card-exec {
        background: #FFFFFF !important;
        border-radius: 10px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 2px 8px rgba(80, 55, 124, 0.06);
        border: 1px solid #E8E2F0;
        position: relative;
        overflow: hidden;
        transition: all 0.25s ease;
    }
    .metric-card-exec:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(80, 55, 124, 0.1);
        border-color: #563D7C;
    }

    .kpi-emerald { border-top: 4px solid #2E9B72 !important; background: linear-gradient(180deg, #F4FAF7 0%, #FFFFFF 100%) !important; }
    .kpi-orange { border-top: 4px solid #D68A24 !important; background: linear-gradient(180deg, #FAF7F2 0%, #FFFFFF 100%) !important; }
    .kpi-blue { border-top: 4px solid #563D7C !important; background: linear-gradient(180deg, #F8F5FB 0%, #FFFFFF 100%) !important; }
    .kpi-rose { border-top: 4px solid #D95757 !important; background: linear-gradient(180deg, #FAF4F4 0%, #FFFFFF 100%) !important; }
    .kpi-cyan { border-top: 4px solid #63458C !important; background: linear-gradient(180deg, #F7F4FA 0%, #FFFFFF 100%) !important; }

    .metric-val-emerald { font-size: 2.7rem; font-weight: 850; color: #2E9B72; line-height: 1.0; }
    .metric-val-orange { font-size: 2.7rem; font-weight: 850; color: #D68A24; line-height: 1.0; }
    .metric-val-blue { font-size: 2.7rem; font-weight: 850; color: #563D7C; line-height: 1.0; }
    .metric-val-rose { font-size: 2.7rem; font-weight: 850; color: #D95757; line-height: 1.0; }
    .metric-val-cyan { font-size: 2.7rem; font-weight: 850; color: #63458C; line-height: 1.0; }

    .metric-lbl-exec {
        font-size: 1.05rem;
        font-weight: 750;
        color: #50377C;
        margin-top: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-badge-exec {
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 800;
        padding: 3px 10px;
        border-radius: 6px;
        margin-top: 8px;
    }
    .badge-bg-emerald { background: #E6F5F0; color: #2E9B72; border: 1px solid #B8E4D5; }
    .badge-bg-orange { background: #FDF4E7; color: #D68A24; border: 1px solid #F6DFBA; }
    .badge-bg-blue { background: #EFEAF5; color: #563D7C; border: 1px solid #D9CDE8; }
    .badge-bg-rose { background: #FDEEEE; color: #D95757; border: 1px solid #F7C6C6; }
    .badge-bg-cyan { background: #F1ECF7; color: #63458C; border: 1px solid #D9CEE8; }

    /* Custom Soft Purple Table Cards */
    .custom-table-card {
        background: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 0 !important;
        box-shadow: 0 2px 8px rgba(80, 55, 124, 0.06) !important;
        border: 1px solid #E8E2F0 !important;
        overflow: hidden !important;
        margin-top: 1rem !important;
        margin-bottom: 1.5rem !important;
    }
    .custom-table {
        width: 100% !important;
        border-collapse: collapse !important;
        text-align: center !important;
    }
    .custom-table th {
        background-color: #50377C !important;
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        padding: 12px 18px !important;
        border-bottom: 1px solid #63458C !important;
    }
    .custom-table td {
        padding: 11px 18px !important;
        font-size: 1.0rem !important;
        color: #2D263B !important;
        border-bottom: 1px solid #E8E2F0 !important;
    }
    .custom-table tbody tr:nth-child(even) {
        background-color: #F9F7FC !important;
    }
    .custom-table tbody tr:hover {
        background-color: #F0EBF7 !important;
    }
    .custom-table tr.total-row {
        background-color: #EDE7F5 !important;
        font-weight: 850 !important;
        border-top: 2px solid #563D7C !important;
    }
    .custom-table tr.total-row td {
        color: #50377C !important;
        font-size: 1.05rem !important;
    }

    /* Smooth Dynamic Sub-Tab Bar Container Centering */
    .stTabs [role="tabpanel"],
    .stTabs div[data-testid="stTabContent"] {
        position: relative !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin-top: 0 !important;
        margin-bottom: 1.2rem !important;
        box-shadow: none !important;
        width: fit-content !important;
        max-width: 100% !important;
        transition: margin-left 0.25s ease !important;
    }

    div[data-testid="stRadio"] {
        margin-left: 0px;
        transition: margin-left 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* PRIMARY NAVIGATION TABS (One Clear Primary Tab Bar) */
    .stTabs button,
    .stTabs button[role="tab"],
    .stTabs [data-baseweb="tab"],
    .stTabs [data-testid="stTab"],
    div[data-testid="stTabs"] button,
    div[data-testid="stTabs"] button[role="tab"],
    div[data-testid="stTabs"] [data-baseweb="tab"],
    div[data-testid="stTabs"] [data-testid="stTab"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E2D9EC !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        min-height: 54px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        cursor: pointer !important;
        box-shadow: 0 2px 8px rgba(80, 55, 124, 0.05) !important;
        transition: all 0.2s ease !important;
    }

    .stTabs button *,
    .stTabs button p,
    .stTabs button span,
    .stTabs button div,
    .stTabs [data-baseweb="tab"] *,
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span,
    .stTabs [data-baseweb="tab"] div,
    div[data-testid="stTabs"] button *,
    div[data-testid="stTabs"] button p,
    div[data-testid="stTabs"] button span,
    div[data-testid="stTabs"] button div,
    div[data-testid="stTabs"] [data-baseweb="tab"] *,
    div[data-testid="stTabs"] [data-baseweb="tab"] p,
    div[data-testid="stTabs"] [data-baseweb="tab"] span,
    div[data-testid="stTabs"] [data-baseweb="tab"] div {
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        color: #50377C !important;
        background: transparent !important;
        white-space: nowrap !important;
        line-height: 1.2 !important;
    }

    .stTabs button:hover,
    .stTabs button:hover *,
    div[data-testid="stTabs"] button:hover,
    div[data-testid="stTabs"] button:hover * {
        background: #F8F5FC !important;
        background-color: #F8F5FC !important;
        color: #563D7C !important;
        border-color: #563D7C !important;
    }

    /* ACTIVE PRIMARY NAVIGATION TAB (#563D7C Primary Velvet Violet Background) */
    .stTabs button[aria-selected="true"],
    .stTabs [data-baseweb="tab"][aria-selected="true"],
    .stTabs [data-testid="stTab"][aria-selected="true"],
    div[data-testid="stTabs"] button[aria-selected="true"],
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
    div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"],
    div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] {
        background: #563D7C !important;
        background-color: #563D7C !important;
        border: 1px solid #563D7C !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 14px rgba(86, 61, 124, 0.22) !important;
    }

    .stTabs button[aria-selected="true"] *,
    .stTabs button[aria-selected="true"] p,
    .stTabs button[aria-selected="true"] span,
    .stTabs button[aria-selected="true"] div,
    .stTabs [aria-selected="true"] *,
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span,
    .stTabs [aria-selected="true"] div,
    div[data-testid="stTabs"] button[aria-selected="true"] *,
    div[data-testid="stTabs"] button[aria-selected="true"] p,
    div[data-testid="stTabs"] button[aria-selected="true"] span,
    div[data-testid="stTabs"] button[aria-selected="true"] div,
    div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] *,
    div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] p,
    div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] span,
    div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] div {
        color: #FFFFFF !important;
        background: transparent !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
    }

    div[data-baseweb="tab-highlight-container"],
    div[data-baseweb="tab-border"],
    div[data-testid="stTabs"] [data-baseweb="tab-highlight-container"],
    div[data-testid="stTabs"] [data-baseweb="tab-border"],
    .stTabs [data-baseweb="tab-highlight-container"],
    .stTabs [data-baseweb="tab-border"],
    .stTabs [role="tablist"],
    .stTabs [data-baseweb="tab-list"],
    div[data-testid="stTabs"] [role="tablist"],
    div[data-testid="stTabs"] [data-baseweb="tab-list"],
    div[role="tablist"] {
        border-bottom: none !important;
        border-bottom-color: transparent !important;
        border-bottom-width: 0px !important;
    }
    div[data-baseweb="tab-border"],
    div[data-baseweb="tab-highlight-container"] {
        display: none !important;
        height: 0px !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    div[data-testid="stTabs"] button::after,
    .stTabs button::after,
    .stTabs [role="tablist"]::after,
    .stTabs [data-baseweb="tab-list"]::after {
        display: none !important;
        content: none !important;
    }

    /* SECONDARY SEGMENTED CONTROL BAR (One Light Secondary Control Bar) */
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 4px !important;
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        background: #EFEAF5 !important;
        padding: 3.5px 4.5px !important;
        border-radius: 10px !important;
        border: 1px solid #E2D9EC !important;
        margin-top: 4px !important;
        margin-bottom: 4px !important;
        width: fit-content !important;
        box-shadow: 0 2px 6px rgba(80, 55, 124, 0.05) !important;
    }

    /* Inactive Child Option Labels (#50377C Dark Purple Text) */
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label {
        font-size: 0.98rem !important;
        font-weight: 750 !important;
        color: #50377C !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 7.5px !important;
        padding: 5px 14px !important;
        opacity: 0.9 !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        margin-right: 0px !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        display: inline-block !important;
        text-align: center !important;
    }
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label p,
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label span,
    .stTabs div[data-testid="stRadio"] label div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        color: #50377C !important;
        font-size: 0.98rem !important;
        font-weight: 750 !important;
        white-space: nowrap !important;
        display: inline !important;
    }
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        opacity: 1.0 !important;
        background: rgba(86, 61, 124, 0.08) !important;
        border-radius: 7.5px !important;
    }

    /* ACTIVE SELECTED CHILD OPTION (#563D7C Primary Purple Pill with Crisp White Text) */
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background: #563D7C !important;
        background-color: #563D7C !important;
        color: #FFFFFF !important;
        font-weight: 850 !important;
        opacity: 1.0 !important;
        border-radius: 7.5px !important;
        padding: 5px 14px !important;
        border: 1px solid #563D7C !important;
        box-shadow: 0 2px 6px rgba(86, 61, 124, 0.2) !important;
        transform: none !important;
    }
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p,
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) span,
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) div {
        color: #FFFFFF !important;
        background: transparent !important;
        font-size: 0.98rem !important;
        font-weight: 850 !important;
    }

    /* Download Footer Banner */
    .export-footer {
        background: #FFFFFF !important;
        border-radius: 10px;
        padding: 1.4rem;
        box-shadow: 0 2px 8px rgba(80, 55, 124, 0.06);
        border: 1px solid #E8E2F0;
        margin-top: 2rem;
    }
    .export-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #50377C;
        margin-bottom: 0.4rem;
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
<div class="command-hero-header" style="padding: 2.2rem 3.0rem; border-radius: 12px; background: linear-gradient(135deg, #50377C 0%, #63458C 100%) !important; box-shadow: 0 4px 16px rgba(80, 55, 124, 0.15); border: 1px solid #63458C;">
    <div style="text-align: left; position: relative; z-index: 2;">
        <div class="command-title" style="margin: 0; font-size: 3.1rem; font-weight: 900; letter-spacing: -0.8px; line-height: 1.15; color: #FFFFFF;">
            Employee Headcount & Tenure Dashboard
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Expander State Persistence & Auto-Close Handler Script
import streamlit.components.v1 as components
components.html("""
<script>
    (function() {
        try {
            var targetDoc = window.parent.document || window.top.document;
            if (!targetDoc) return;

            try {
                var navEntries = performance.getEntriesByType('navigation');
                var isReload = (navEntries.length > 0 && navEntries[0].type === 'reload');
                if (isReload || !targetDoc._hasInitPageTop) {
                    targetDoc._hasInitPageTop = true;
                    sessionStorage.removeItem("openPopoverTag");
                    sessionStorage.removeItem("timeStepCount");
                }
            } catch(err) {}

            function keepPageAtTop() {
                try {
                    var mainContainer = targetDoc.querySelector('div[data-testid="stAppViewContainer"], section.main');
                    if (mainContainer) {
                        mainContainer.scrollTop = 0;
                    }
                    if (targetDoc.defaultView) {
                        targetDoc.defaultView.scrollTo(0, 0);
                    }
                } catch(e) {}
            }

            function alignChildFilterToActiveTab() {
                try {
                    var activeTabBtn = targetDoc.querySelector('div[data-testid="stTabs"] button[aria-selected="true"], div[data-testid="stTabs"] [aria-selected="true"]');
                    var activeTabPanel = targetDoc.querySelector('div[data-testid="stTabContent"]:not([hidden]), div[role="tabpanel"]:not([hidden])');
                    
                    if (activeTabBtn && activeTabPanel) {
                        var childRadioBar = activeTabPanel.querySelector('div[data-testid="stRadio"]');
                        if (childRadioBar) {
                            var tabRect = activeTabBtn.getBoundingClientRect();
                            var panelRect = activeTabPanel.getBoundingClientRect();
                            var tabCenterLeft = (tabRect.left + (tabRect.width / 2)) - panelRect.left;
                            var radioWidth = childRadioBar.getBoundingClientRect().width;
                            var targetMarginLeft = tabCenterLeft - (radioWidth / 2);
                            
                            if (targetMarginLeft < 0) targetMarginLeft = 0;
                            var maxMarginLeft = panelRect.width - radioWidth;
                            if (maxMarginLeft > 0 && targetMarginLeft > maxMarginLeft) targetMarginLeft = maxMarginLeft;
                            
                            childRadioBar.style.setProperty('margin-left', Math.round(targetMarginLeft) + 'px', 'important');
                        }
                    }
                } catch(err) {}
            }

            setInterval(alignChildFilterToActiveTab, 120);

            function restoreOpenState() {
                try {
                    var activeIdx = sessionStorage.getItem("active_subtab_idx");
                    if (activeIdx !== null) {
                        var activeTabPanel = targetDoc.querySelector('div[data-testid="stTabContent"]:not([hidden]), div[role="tabpanel"]:not([hidden])');
                        if (activeTabPanel) {
                            var radioLabels = activeTabPanel.querySelectorAll('div[data-testid="stRadio"] label');
                            var targetLabel = radioLabels[parseInt(activeIdx)];
                            if (targetLabel) {
                                var input = targetLabel.querySelector('input');
                                if (input && !input.checked) {
                                    targetLabel.click();
                                }
                            }
                        }
                    }
                } catch(err) {}
            }

            if (!targetDoc._hasGlobalClickListener) {
                targetDoc._hasGlobalClickListener = true;

                targetDoc.addEventListener('click', function(e) {
                    var popoverBody = e.target.closest('div[data-testid="stPopoverBody"]');
                    var isInsideSelectDropdown = e.target.closest('ul[role="listbox"]') || 
                                                 e.target.closest('div[role="listbox"]') ||
                                                 e.target.closest('div[data-baseweb="menu"]') ||
                                                 e.target.closest('div[data-baseweb="calendar"]') ||
                                                 e.target.closest('div[data-baseweb="datepicker"]') ||
                                                 e.target.closest('div[data-baseweb="popover"]');

                    var radioLabel = e.target.closest('div[data-testid="stRadio"] label');
                    if (radioLabel) {
                        var radioContainer = radioLabel.closest('div[role="radiogroup"]');
                        if (radioContainer) {
                            var labels = Array.from(radioContainer.querySelectorAll('label'));
                            var clickedIdx = labels.indexOf(radioLabel);
                            if (clickedIdx !== -1) {
                                sessionStorage.setItem("active_subtab_idx", clickedIdx.toString());
                            }
                        }

                        setTimeout(function() {
                            var tableCard = targetDoc.querySelector('.custom-table-card, table.custom-table');
                            var mainContainer = targetDoc.querySelector('div[data-testid="stAppViewContainer"], section.main');
                            if (tableCard) {
                                var rect = tableCard.getBoundingClientRect();
                                var containerRect = mainContainer ? mainContainer.getBoundingClientRect() : { top: 0 };
                                var currentScroll = mainContainer ? mainContainer.scrollTop : (targetDoc.defaultView.pageYOffset || 0);
                                var targetTop = currentScroll + (rect.top - containerRect.top) - 15;
                                
                                if (mainContainer) {
                                    mainContainer.scrollTo({ top: Math.max(0, targetTop), behavior: 'smooth' });
                                }
                                if (targetDoc.defaultView) {
                                    targetDoc.defaultView.scrollTo({ top: Math.max(0, targetTop), behavior: 'smooth' });
                                }
                            }
                        }, 100);
                    }

                    var tabBtn = e.target.closest('div[data-testid="stTabs"] button');
                    if (tabBtn) {
                        sessionStorage.removeItem("active_subtab_idx");
                    }

                    if (popoverBody) {
                        var optTxt = e.target.innerText || e.target.textContent || "";
                        optTxt = optTxt.trim();

                        var isTimeModeOption = (
                            optTxt.includes("Monthly (MTD)") || optTxt.includes("Quarterly") ||
                            optTxt.includes("Yearly") || optTxt.includes("Today") || optTxt.includes("Custom Calendar")
                        );

                        var isYearNumber = /^\d{4}$/.test(optTxt);
                        var isMonthName = ["January","February","March","April","May","June","July","August","September","October","November","December"].some(m => optTxt.includes(m));
                        var isQuarterName = ["Q1","Q2","Q3","Q4"].some(q => optTxt.includes(q));
                        var isToday = optTxt.includes("Today");

                        var isCustomCalendarOption = optTxt.includes("Custom Calendar");
                        var isCustomCalendarActive = popoverBody.innerText && popoverBody.innerText.includes("Custom Date Range");

                        if (!isInsideSelectDropdown) {
                            if (isCustomCalendarOption || isCustomCalendarActive) {
                                sessionStorage.setItem("openPopoverTag", "time");
                            } else if (isTimeModeOption || isYearNumber || isMonthName || isQuarterName || isToday) {
                                var stepCount = parseInt(sessionStorage.getItem("timeStepCount") || "0");
                                stepCount++;
                                sessionStorage.setItem("timeStepCount", stepCount.toString());

                                var isYearModeActive = popoverBody.innerText && popoverBody.innerText.includes("Select Year");
                                var isFinished = !isCustomCalendarActive && !isCustomCalendarOption && (
                                    isToday || (isYearModeActive && isYearNum) || isMonthName || isQuarterName
                                );

                                if (isFinished) {
                                    sessionStorage.removeItem("openPopoverTag");
                                    sessionStorage.removeItem("timeStepCount");
                                    targetDoc._preventPopoverReopen = true;
                                    setTimeout(function() {
                                        targetDoc.body.click();
                                        setTimeout(function() {
                                            targetDoc._preventPopoverReopen = false;
                                        }, 600);
                                    }, 80);
                                } else {
                                    sessionStorage.setItem("openPopoverTag", "time");
                                }
                            }
                        }
                    }
                }, true);

                try {
                    var mainContainer = targetDoc.querySelector('div[data-testid="stAppViewContainer"], section.main');
                    if (mainContainer) { mainContainer.scrollTop = 0; }
                    targetDoc.defaultView.scrollTo(0, 0);
                } catch(err) {}

                function restorePopoverOpenState() {
                    if (targetDoc._preventPopoverReopen) return;
                    var openTag = sessionStorage.getItem("openPopoverTag");
                    var isCustomCal = sessionStorage.getItem("isCustomCalendarMode") === "true";
                    if ((openTag === "time" || isCustomCal) && !targetDoc._isReopeningPopover) {
                        var popoverBtns = targetDoc.querySelectorAll('button[data-testid="stPopoverButton"]');
                        if (popoverBtns.length > 0) {
                            var timeBtn = popoverBtns[0];
                            var currentOpenBody = targetDoc.querySelector('div[data-testid="stPopoverBody"]');
                            if (!currentOpenBody) {
                                targetDoc._isReopeningPopover = true;
                                setTimeout(function() {
                                    timeBtn.click();
                                    setTimeout(function() {
                                        targetDoc._isReopeningPopover = false;
                                    }, 400);
                                }, 150);
                            }
                        }
                    }
                }

                var observer = new MutationObserver(function() {
                    keepPageAtTop();
                    restoreOpenState();
                    restorePopoverOpenState();
                    alignChildFilterToActiveTab();
                });
                observer.observe(targetDoc.body, { childList: true, subtree: true });
            }
        } catch(err) {
            console.error("Expander persistence notice:", err);
        }
    })();
</script>
""", height=0, width=0)

# Branch & Team Scope Lists
tme_all_teams = sorted([str(t) for t in raw_df['team_type'].dropna().unique() if str(t).strip() != ""])
branches_11_options = ["All 11 Cities", "Ahmedabad", "Bangalore", "Chandigarh", "Chennai", "Coimbatore", "Delhi", "Hyderabad", "Jaipur", "Kolkata", "Mumbai", "Pune"]
team_type_single_options = ["All Teams"] + tme_all_teams

if "last_active_expander" not in st.session_state:
    st.session_state["last_active_expander"] = None

def cb_time(): st.session_state["last_active_expander"] = "time"
def cb_emp(): st.session_state["last_active_expander"] = "emp"
def cb_city(): st.session_state["last_active_expander"] = "city"
def cb_team(): st.session_state["last_active_expander"] = "team"

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

# 4-Category Dropdown Popover Header Bar
filter_c1, filter_c2, filter_c3, filter_c4 = st.columns(4)

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
            month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            
            sel_month = st.selectbox("Select Month", month_names, index=7, key="hdr_dd_mo_month")
            sel_year = st.selectbox("Select Year", list(range(2018, 2029)), index=8, key="hdr_dd_mo_year")
            
            m_idx = month_names.index(sel_month) + 1
            start_date = pd.Timestamp(datetime(sel_year, m_idx, 1))
            if m_idx == 12:
                end_date = pd.Timestamp(datetime(sel_year, 12, 31))
            else:
                end_date = pd.Timestamp(datetime(sel_year, m_idx + 1, 1)) - pd.Timedelta(days=1)

        elif time_filter_mode == "Quarterly":
            sel_q_year = st.selectbox("Select Year", list(range(2018, 2029)), index=8, key="hdr_dd_q_year")
            q_options = ["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]
            sel_quarter = st.selectbox("Select Quarter", q_options, index=2, key="hdr_dd_q_quarter")
            
            if "Q1" in sel_quarter:
                start_date = pd.Timestamp(datetime(sel_q_year, 1, 1))
                end_date = pd.Timestamp(datetime(sel_q_year, 3, 31))
            elif "Q2" in sel_quarter:
                start_date = pd.Timestamp(datetime(sel_q_year, 4, 1))
                end_date = pd.Timestamp(datetime(sel_q_year, 6, 30))
            elif "Q3" in sel_quarter:
                start_date = pd.Timestamp(datetime(sel_q_year, 7, 1))
                end_date = pd.Timestamp(datetime(sel_q_year, 9, 30))
            else:
                start_date = pd.Timestamp(datetime(sel_q_year, 10, 1))
                end_date = pd.Timestamp(datetime(sel_q_year, 12, 31))

        elif time_filter_mode == "Yearly":
            sel_y_year = st.selectbox("Select Year", list(range(2018, 2029)), index=8, key="hdr_dd_y_year")
            start_date = pd.Timestamp(datetime(sel_y_year, 1, 1))
            end_date = pd.Timestamp(datetime(sel_y_year, 12, 31))

        elif time_filter_mode == "Today":
            start_date = pd.Timestamp(today)
            end_date = pd.Timestamp(today)

        else: # Custom Calendar
            default_start = date(2026, 8, 1)
            default_end = date(2026, 8, 31)
            
            cal_range = st.date_input(
                "Select Custom Date Range",
                value=(default_start, default_end),
                min_value=date(2018, 1, 1),
                max_value=date(2028, 12, 31),
                key="hdr_dd_cal_range"
            )
            
            if isinstance(cal_range, (tuple, list)) and len(cal_range) == 2:
                start_date = pd.Timestamp(cal_range[0])
                end_date = pd.Timestamp(cal_range[1])
            else:
                start_date = pd.Timestamp(default_start)
                end_date = pd.Timestamp(default_end)

with filter_c2:
    with st.popover(emp_type_header_label, use_container_width=True):
        emp_type_option = st.selectbox(
            "Select Employee Type",
            ["All EmpTypes", "JDA", "ME", "TME"],
            index=0,
            key="hdr_dd_emp_type"
        )

with filter_c3:
    with st.popover(city_header_label, use_container_width=True):
        selected_city_single = st.selectbox(
            "Select Branch / City",
            branches_11_options,
            index=0,
            key="hdr_dd_city"
        )

with filter_c4:
    with st.popover(team_header_label, use_container_width=True):
        selected_team_single = st.selectbox(
            "Select Team Type",
            team_type_single_options,
            index=0,
            key="hdr_dd_team"
        )

# Construct Filter Arrays
selected_emp_types = [emp_type_option] if emp_type_option != "All EmpTypes" else ["JDA", "ME", "TME"]
selected_branches = [selected_city_single] if selected_city_single != "All 11 Cities" else branches_11_options[1:]
selected_teams = [selected_team_single] if selected_team_single != "All Teams" else tme_all_teams

# Filter Data via Engine
df_filtered = calculate_tenure_and_filter(
    raw_df,
    start_date=start_date,
    end_date=end_date,
    selected_emp_types=selected_emp_types,
    selected_branches=selected_branches,
    selected_teams=selected_teams,
    sda_city="All"
)

active_count = len(df_filtered)
exited_count = (df_filtered['status_as_of_obs'] == 'Exited').sum()
active_jda_count = ((df_filtered['status_as_of_obs'] == 'Active') & (df_filtered['emp_type'] == 'JDA')).sum()
active_me_count = ((df_filtered['status_as_of_obs'] == 'Active') & (df_filtered['emp_type'] == 'ME')).sum()
active_tme_count = ((df_filtered['status_as_of_obs'] == 'Active') & (df_filtered['emp_type'] == 'TME')).sum()

# Helper for comparison metrics
def compute_period_active(df_raw, p_start_date, p_end_date, emp_types, branches, teams):
    try:
        df_p = calculate_tenure_and_filter(
            df_raw,
            start_date=p_start_date,
            end_date=p_end_date,
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

mom_start = start_date - pd.DateOffset(months=1)
mom_end = end_date - pd.DateOffset(months=1)

def get_previous_quarter_dates(ref_date):
    m = ref_date.month
    y = ref_date.year
    if m in [4, 5, 6]:
        return pd.Timestamp(datetime(y, 1, 1)), pd.Timestamp(datetime(y, 3, 31))
    elif m in [7, 8, 9]:
        return pd.Timestamp(datetime(y, 4, 1)), pd.Timestamp(datetime(y, 6, 30))
    elif m in [10, 11, 12]:
        return pd.Timestamp(datetime(y, 7, 1)), pd.Timestamp(datetime(y, 9, 30))
    else:
        return pd.Timestamp(datetime(y - 1, 10, 1)), pd.Timestamp(datetime(y - 1, 12, 31))

qtq_start, qtq_end = get_previous_quarter_dates(end_date)
yoy_start = start_date - pd.DateOffset(years=1)
yoy_end = end_date - pd.DateOffset(years=1)

mom_count = compute_period_active(raw_df, mom_start, mom_end, selected_emp_types, selected_branches, selected_teams)
qtq_count = compute_period_active(raw_df, qtq_start, qtq_end, selected_emp_types, selected_branches, selected_teams)
yoy_count = compute_period_active(raw_df, yoy_start, yoy_end, selected_emp_types, selected_branches, selected_teams)

if mom_count > 0:
    mom_diff = active_count - mom_count
    mom_pct = round((mom_diff / mom_count) * 100, 1)
    mom_str = f"{'+' if mom_pct >= 0 else ''}{mom_pct}%"
else:
    mom_str = "+0.0%"

if qtq_count > 0:
    qtq_diff = active_count - qtq_count
    qtq_pct = round((qtq_diff / qtq_count) * 100, 1)
    qtq_str = f"{'+' if qtq_pct >= 0 else ''}{qtq_pct}%"
else:
    qtq_str = "+0.0%"

if yoy_count > 0:
    yoy_diff = active_count - yoy_count
    yoy_pct = round((yoy_diff / yoy_count) * 100, 1)
    yoy_str = f"{'+' if yoy_pct >= 0 else ''}{yoy_pct}%"
else:
    yoy_str = "+0.0%"

if not df_filtered.empty:
    new_joiners_count = ((pd.to_datetime(df_filtered['doj']) >= start_date) & (pd.to_datetime(df_filtered['doj']) <= end_date)).sum()
else:
    new_joiners_count = 0

# Executive KPI Cards Block
st.markdown("<br>", unsafe_allow_html=True)
time_mode_current = st.session_state.get("hdr_dd_time_mode", "Monthly (MTD)")

if time_mode_current == "Yearly":
    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f'''
    <div class="metric-card-exec kpi-emerald">
        <div class="metric-val-emerald">{active_count}</div>
        <div class="metric-lbl-exec">Headcount</div>
        <div class="metric-badge-exec badge-bg-emerald">🏢 Active ({emp_type_option})</div>
    </div>
    ''', unsafe_allow_html=True)

    c2.markdown(f'''
    <div class="metric-card-exec kpi-orange">
        <div class="metric-val-orange">{new_joiners_count}</div>
        <div class="metric-lbl-exec">New Joiners</div>
        <div class="metric-badge-exec badge-bg-orange">✨ New Joiners in Year</div>
    </div>
    ''', unsafe_allow_html=True)

    c3.markdown(f'''
    <div class="metric-card-exec kpi-rose">
        <div class="metric-val-rose">{exited_count}</div>
        <div class="metric-lbl-exec">Exited in Year</div>
        <div class="metric-badge-exec badge-bg-rose">🔴 Exited Count</div>
    </div>
    ''', unsafe_allow_html=True)

    c4.markdown(f'''
    <div class="metric-card-exec kpi-blue">
        <div class="metric-val-blue">{yoy_str}</div>
        <div class="metric-lbl-exec">YoY % Change</div>
        <div class="metric-badge-exec badge-bg-blue">📈 Year-over-Year</div>
    </div>
    ''', unsafe_allow_html=True)

elif time_mode_current == "Quarterly":
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.markdown(f'''
    <div class="metric-card-exec kpi-emerald">
        <div class="metric-val-emerald">{active_count}</div>
        <div class="metric-lbl-exec">Headcount</div>
        <div class="metric-badge-exec badge-bg-emerald">🏢 Active ({emp_type_option})</div>
    </div>
    ''', unsafe_allow_html=True)

    c2.markdown(f'''
    <div class="metric-card-exec kpi-orange">
        <div class="metric-val-orange">{new_joiners_count}</div>
        <div class="metric-lbl-exec">New Joiners</div>
        <div class="metric-badge-exec badge-bg-orange">✨ New Joiners in Quarter</div>
    </div>
    ''', unsafe_allow_html=True)

    c3.markdown(f'''
    <div class="metric-card-exec kpi-rose">
        <div class="metric-val-rose">{exited_count}</div>
        <div class="metric-lbl-exec">Exited in Quarter</div>
        <div class="metric-badge-exec badge-bg-rose">🔴 Exited Count</div>
    </div>
    ''', unsafe_allow_html=True)

    c4.markdown(f'''
    <div class="metric-card-exec kpi-cyan">
        <div class="metric-val-cyan">{qtq_str}</div>
        <div class="metric-lbl-exec">QtQ % Change</div>
        <div class="metric-badge-exec badge-bg-cyan">🗓️ Quarter-over-Quarter</div>
    </div>
    ''', unsafe_allow_html=True)

    c5.markdown(f'''
    <div class="metric-card-exec kpi-blue">
        <div class="metric-val-blue">{yoy_str}</div>
        <div class="metric-lbl-exec">YoY % Change</div>
        <div class="metric-badge-exec badge-bg-blue">📈 Year-over-Year</div>
    </div>
    ''', unsafe_allow_html=True)

else:
    if time_mode_current == "Today":
        c1, c2, c3, c4 = st.columns(4)

        c1.markdown(f'''
        <div class="metric-card-exec kpi-emerald">
            <div class="metric-val-emerald">{active_count}</div>
            <div class="metric-lbl-exec">Headcount</div>
            <div class="metric-badge-exec badge-bg-emerald">📍 Active Today ({emp_type_option})</div>
        </div>
        ''', unsafe_allow_html=True)

        c2.markdown(f'''
        <div class="metric-card-exec kpi-cyan">
            <div class="metric-val-cyan">{mom_str}</div>
            <div class="metric-lbl-exec">MoM % Change</div>
            <div class="metric-badge-exec badge-bg-cyan">📊 Month-over-Month</div>
        </div>
        ''', unsafe_allow_html=True)

        c3.markdown(f'''
        <div class="metric-card-exec kpi-blue">
            <div class="metric-val-blue">{qtq_str}</div>
            <div class="metric-lbl-exec">QtQ % Change</div>
            <div class="metric-badge-exec badge-bg-blue">🗓️ Quarter-over-Quarter</div>
        </div>
        ''', unsafe_allow_html=True)

        c4.markdown(f'''
        <div class="metric-card-exec kpi-orange">
            <div class="metric-val-orange">{yoy_str}</div>
            <div class="metric-lbl-exec">YoY % Change</div>
            <div class="metric-badge-exec badge-bg-orange">📈 Year-over-Year</div>
        </div>
        ''', unsafe_allow_html=True)

    elif emp_type_option == "All EmpTypes":
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
            <div class="metric-badge-exec badge-bg-orange">🟩 Active JDA</div>
        </div>
        ''', unsafe_allow_html=True)

        c3.markdown(f'''
        <div class="metric-card-exec kpi-blue">
            <div class="metric-val-blue">{active_me_count}</div>
            <div class="metric-lbl-exec">Active ME</div>
            <div class="metric-badge-exec badge-bg-blue">🟨 Active ME</div>
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
            <div class="metric-lbl-exec">Exited in Month</div>
            <div class="metric-badge-exec badge-bg-rose">🔴 Exited Count</div>
        </div>
        ''', unsafe_allow_html=True)

        c3.markdown(f'''
        <div class="metric-card-exec kpi-cyan">
            <div class="metric-val-cyan">{mom_str}</div>
            <div class="metric-lbl-exec">MoM % Change</div>
            <div class="metric-badge-exec badge-bg-cyan">📊 Month-over-Month</div>
        </div>
        ''', unsafe_allow_html=True)

        c4.markdown(f'''
        <div class="metric-card-exec kpi-orange">
            <div class="metric-val-orange">{new_joiners_count}</div>
            <div class="metric-lbl-exec">New Joiners</div>
            <div class="metric-badge-exec badge-bg-orange">✨ New Joiners in Month</div>
        </div>
        ''', unsafe_allow_html=True)

        c5.markdown(f'''
        <div class="metric-card-exec kpi-blue">
            <div class="metric-val-blue">{yoy_str}</div>
            <div class="metric-lbl-exec">YoY % Change</div>
            <div class="metric-badge-exec badge-bg-blue">📈 Year-over-Year</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Global Download Footer Function
def render_download_section(section_id="default"):
    st.markdown(f"""
    <div class="export-footer">
        <div class="export-title">📥 Download Filtered Employee Dataset</div>
        <div style="font-size: 0.92rem; color: #50377C; margin-bottom: 0.9rem; font-weight:600;">
            Export complete employee dataset matching your criteria for period <b>{start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')}</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    excel_buf = io.BytesIO()
    with pd.ExcelWriter(excel_buf, engine='openpyxl') as writer:
        df_filtered.to_excel(writer, index=False, sheet_name='Filtered_Employees')
    excel_data = excel_buf.getvalue()

    st.download_button(
        label="📥 Download Filtered Dataset (.xlsx)",
        data=excel_data,
        file_name=f"Workforce_Analytics_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"btn_dl_xlsx_{section_id}"
    )

# Dashboard Main Tabs
st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)

main_tab1, main_tab2, main_tab3 = st.tabs([
    "🔢 Employee Headcount",
    "📈 Tenure Breakdown",
    "📋 Employee Drill-Down"
])

# TAB 1: EMPLOYEE HEADCOUNT SUMMARY
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
        is_today = (time_mode_current == "Today")

        if s_mode == "📊 Pan India / Branch Summary":
            st.markdown(f"#### 📊 {'Pan India' if is_pan_india else selected_branches[0]} Headcount Summary")
            
            br_hc_df = df_filtered.groupby('branch').agg(
                Active_Count=('emp_code', 'count'),
                Exited_Count=('status_as_of_obs', lambda x: (x == 'Exited').sum()),
                New_Joiners_Count=('doj', lambda x: ((pd.to_datetime(x) >= start_date) & (pd.to_datetime(x) <= end_date)).sum())
            ).reset_index()

            tot_branch_row = {
                'branch': 'TOTAL (Pan India)',
                'Active_Count': br_hc_df['Active_Count'].sum(),
                'Exited_Count': br_hc_df['Exited_Count'].sum(),
                'New_Joiners_Count': br_hc_df['New_Joiners_Count'].sum()
            }
            br_hc_df_full = pd.concat([br_hc_df, pd.DataFrame([tot_branch_row])], ignore_index=True)
            
            html_b = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            if is_today:
                html_b.append('<th>Branch / City</th><th>Headcount</th>')
            else:
                html_b.append('<th>Branch / City</th><th>Headcount</th><th>Exited in Period</th><th>New Joiners in Period</th>')
            html_b.append('</tr></thead><tbody>')
            
            for _, r in br_hc_df_full.iterrows():
                is_tot = str(r['branch']).startswith("TOTAL")
                tr_cls = 'class="total-row"' if is_tot else ''
                html_b.append(f'<tr {tr_cls}>')
                html_b.append(f'<td style="font-weight:700; text-align:left; color:#50377C;">{r["branch"]}</td>')
                html_b.append(f'<td style="color:#2E9B72; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html_b.append(f'<td style="color:#D95757; font-weight:700;">{r["Exited_Count"]}</td>')
                    html_b.append(f'<td style="color:#D68A24; font-weight:800;">{r["New_Joiners_Count"]}</td>')
                html_b.append('</tr>')
            html_b.append('</tbody></table></div>')
            st.markdown("".join(html_b), unsafe_allow_html=True)

        else: # 👥 Team Type Summary
            st.markdown("#### 👥 Team Type Headcount Summary")
            team_hc_df = df_filtered.groupby('team_type').agg(
                Active_Count=('emp_code', 'count'),
                Exited_Count=('status_as_of_obs', lambda x: (x == 'Exited').sum()),
                New_Joiners_Count=('doj', lambda x: ((pd.to_datetime(x) >= start_date) & (pd.to_datetime(x) <= end_date)).sum())
            ).reset_index().sort_values(by='Active_Count', ascending=False)

            tot_team_row = {
                'team_type': 'TOTAL (All Teams)',
                'Active_Count': team_hc_df['Active_Count'].sum(),
                'Exited_Count': team_hc_df['Exited_Count'].sum(),
                'New_Joiners_Count': team_hc_df['New_Joiners_Count'].sum()
            }
            team_hc_df_full = pd.concat([team_hc_df, pd.DataFrame([tot_team_row])], ignore_index=True)
            
            html_t = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            if is_today:
                html_t.append('<th>Team Type</th><th>Headcount</th>')
            else:
                html_t.append('<th>Team Type</th><th>Headcount</th><th>Exited in Period</th><th>New Joiners in Period</th>')
            html_t.append('</tr></thead><tbody>')
            
            for _, r in team_hc_df_full.iterrows():
                is_tot = str(r['team_type']).startswith("TOTAL")
                tr_cls = 'class="total-row"' if is_tot else ''
                html_t.append(f'<tr {tr_cls}>')
                html_t.append(f'<td style="font-weight:700; text-align:left; color:#50377C;">{r["team_type"]}</td>')
                html_t.append(f'<td style="color:#2E9B72; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html_t.append(f'<td style="color:#D95757; font-weight:700;">{r["Exited_Count"]}</td>')
                    html_t.append(f'<td style="color:#D68A24; font-weight:800;">{r["New_Joiners_Count"]}</td>')
                html_t.append('</tr>')
            html_t.append('</tbody></table></div>')
            st.markdown("".join(html_t), unsafe_allow_html=True)

    render_download_section("tab1_headcount_summary")

# TAB 2: TENURE BREAKDOWN ANALYSIS
with main_tab2:
    if df_filtered.empty:
        st.warning("No records matching filter criteria.")
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
            options=["⏳ Overall Tenure", "🏢 Branch-Wise Tenure", "👥 Team-Wise Tenure"],
            index=0,
            horizontal=True,
            key="tenure_view_pill_toggle",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)

        if "Overall Tenure" in v_mode:
            st.markdown(f"#### ⏳ Headcount Wise Tenure ({start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')})")
            
            tb_df = df_filtered.groupby('tenure_bucket').agg(
                Total_Headcount=('emp_code', 'count'),
                Exited_Count=('status_as_of_obs', lambda x: (x == 'Exited').sum())
            ).reindex(bucket_order).fillna(0).reset_index()

            tot_tb_row = {
                'tenure_bucket': 'TOTAL (All Tenure Buckets)',
                'Total_Headcount': tb_df['Total_Headcount'].sum(),
                'Exited_Count': tb_df['Exited_Count'].sum()
            }
            tb_df_full = pd.concat([tb_df, pd.DataFrame([tot_tb_row])], ignore_index=True)
            
            html_tb = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            if is_today:
                html_tb.append('<th>Tenure Bucket</th><th>Headcount</th>')
            else:
                html_tb.append('<th>Tenure Bucket</th><th>Headcount</th><th>Exited in Period</th>')
            html_tb.append('</tr></thead><tbody>')
            
            for _, r in tb_df_full.iterrows():
                is_tot = str(r['tenure_bucket']).startswith("TOTAL")
                tr_cls = 'class="total-row"' if is_tot else ''
                html_tb.append(f'<tr {tr_cls}>')
                html_tb.append(f'<td style="font-weight:700; text-align:left; color:#50377C;">{r["tenure_bucket"]}</td>')
                html_tb.append(f'<td style="color:#2E9B72; font-weight:800;">{int(r["Total_Headcount"])}</td>')
                if not is_today:
                    html_tb.append(f'<td style="color:#D95757; font-weight:700;">{int(r["Exited_Count"])}</td>')
                html_tb.append('</tr>')
            html_tb.append('</tbody></table></div>')
            st.markdown("".join(html_tb), unsafe_allow_html=True)

        elif "Branch" in v_mode:
            st.markdown("#### 🏢 Branch-Wise Tenure")
            b_pivot = pd.crosstab(df_filtered['branch'], df_filtered['tenure_bucket']).reindex(columns=bucket_order, fill_value=0).reset_index()

            tot_b_pivot = {'branch': 'TOTAL (All Cities)'}
            for bo in bucket_order:
                tot_b_pivot[bo] = b_pivot[bo].sum()
            b_pivot_full = pd.concat([b_pivot, pd.DataFrame([tot_b_pivot])], ignore_index=True)
            
            html_bp = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            html_bp.append('<th>Branch / City</th>')
            for bo in bucket_order:
                html_bp.append(f'<th>{bo}</th>')
            html_bp.append('</tr></thead><tbody>')
            
            for _, r in b_pivot_full.iterrows():
                is_tot = str(r['branch']).startswith("TOTAL")
                tr_cls = 'class="total-row"' if is_tot else ''
                html_bp.append(f'<tr {tr_cls}>')
                html_bp.append(f'<td style="font-weight:700; text-align:left; color:#50377C;">{r["branch"]}</td>')
                for bo in bucket_order:
                    html_bp.append(f'<td>{int(r[bo])}</td>')
                html_bp.append('</tr>')
            html_bp.append('</tbody></table></div>')
            st.markdown("".join(html_bp), unsafe_allow_html=True)

        else: # 👥 Team-Wise Tenure Matrix
            st.markdown("#### 👥 Team Type Wise Tenure")
            t_pivot = pd.crosstab(df_filtered['team_type'], df_filtered['tenure_bucket']).reindex(columns=bucket_order, fill_value=0).reset_index()

            tot_t_pivot = {'team_type': 'TOTAL (All Teams)'}
            for bo in bucket_order:
                tot_t_pivot[bo] = t_pivot[bo].sum()
            t_pivot_full = pd.concat([t_pivot, pd.DataFrame([tot_t_pivot])], ignore_index=True)
            
            html_tp = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            html_tp.append('<th>Team Type</th>')
            for bo in bucket_order:
                html_tp.append(f'<th>{bo}</th>')
            html_tp.append('</tr></thead><tbody>')
            
            for _, r in t_pivot_full.iterrows():
                is_tot = str(r['team_type']).startswith("TOTAL")
                tr_cls = 'class="total-row"' if is_tot else ''
                html_tp.append(f'<tr {tr_cls}>')
                html_tp.append(f'<td style="font-weight:700; text-align:left; color:#50377C;">{r["team_type"]}</td>')
                for bo in bucket_order:
                    html_tp.append(f'<td>{int(r[bo])}</td>')
                html_tp.append('</tr>')
            html_tp.append('</tbody></table></div>')
            st.markdown("".join(html_tp), unsafe_allow_html=True)

    render_download_section("tab2_tenure_breakdown")

# TAB 3: EMPLOYEE DRILL-DOWN & DATA MATRICES
with main_tab3:
    drill_options = ["🔍 Searchable Employee List", "🏢 Branch List", "👥 Team List"]
    if time_mode_current != "Today":
        drill_options.append("🚪 Exited Employees")

    d_mode = st.radio(
        "Select Drill-Down View",
        options=drill_options,
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
            html5.append('<th>Emp Code</th><th>Employee Name</th><th>Branch</th><th>Type</th><th>Team Type</th><th>DOJ</th><th>DOL</th><th>Designation</th>')
            html5.append('</tr></thead><tbody>')
            
            for _, r in display_df.head(100).iterrows():
                dol_str = r['dol'] if pd.notnull(r['dol']) and str(r['dol']).strip() != "" else "-"
                
                html5.append('<tr>')
                html5.append(f'<td style="font-weight:700; color:#50377C;">{r["emp_code"]}</td>')
                html5.append(f'<td style="text-align:left; font-weight:700; color:#2D263B;">{r["emp_name"]}</td>')
                html5.append(f'<td style="color:#50377C;">{r["branch"]}</td>')
                html5.append(f'<td><b>{r["emp_type"]}</b></td>')
                html5.append(f'<td>{r["team_type"]}</td>')
                html5.append(f'<td>{r["doj"]}</td>')
                html5.append(f'<td>{dol_str}</td>')
                html5.append(f'<td style="font-size:0.9rem; color:#6E6380;">{r["designation"]}</td>')
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
                Active_Count=('emp_code', 'count'),
                Exited_Count=('status_as_of_obs', lambda x: (x == 'Exited').sum())
            ).reset_index()
            
            tot_b_row = {
                'branch': 'TOTAL (Selected Cities)',
                'Active_Count': branch_stats['Active_Count'].sum(),
                'Exited_Count': branch_stats['Exited_Count'].sum()
            }
            full_b_df = pd.concat([branch_stats, pd.DataFrame([tot_b_row])], ignore_index=True)
            
            html3 = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            if is_today:
                html3.append('<th>Branch / City</th><th>Headcount</th>')
            else:
                html3.append('<th>Branch / City</th><th>Headcount</th><th>Exited in Period</th>')
            html3.append('</tr></thead><tbody>')
            
            for _, r in full_b_df.iterrows():
                is_tot = str(r['branch']).startswith("TOTAL")
                tr_cls = 'class="total-row"' if is_tot else ''
                html3.append(f'<tr {tr_cls}>')
                html3.append(f'<td style="text-align:left; font-weight:700; color:#50377C;">{r["branch"]}</td>')
                html3.append(f'<td style="color:#2E9B72; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html3.append(f'<td style="color:#D95757; font-weight:700;">{r["Exited_Count"]}</td>')
                html3.append('</tr>')
                
            html3.append('</tbody></table></div>')
            st.markdown("".join(html3), unsafe_allow_html=True)

    elif d_mode == "👥 Team List":
        st.markdown("#### 👥 Team-Wise Table")
        if df_filtered.empty:
            st.warning("No records matching filter criteria.")
        else:
            team_stats = df_filtered.groupby('team_type').agg(
                Active_Count=('emp_code', 'count'),
                Exited_Count=('status_as_of_obs', lambda x: (x == 'Exited').sum())
            ).reset_index().sort_values(by='Active_Count', ascending=False)
            
            tot_t_row = {
                'team_type': 'TOTAL (Selected Teams)',
                'Active_Count': team_stats['Active_Count'].sum(),
                'Exited_Count': team_stats['Exited_Count'].sum()
            }
            full_t_df = pd.concat([team_stats, pd.DataFrame([tot_t_row])], ignore_index=True)
            
            html4 = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
            if is_today:
                html4.append('<th>Team Type</th><th>Headcount</th>')
            else:
                html4.append('<th>Team Type</th><th>Headcount</th><th>Exited in Period</th>')
            html4.append('</tr></thead><tbody>')
            
            for _, r in full_t_df.iterrows():
                is_tot = str(r['team_type']).startswith("TOTAL")
                tr_cls = 'class="total-row"' if is_tot else ''
                
                html4.append(f'<tr {tr_cls}>')
                html4.append(f'<td style="text-align:left; font-weight:700; color:#50377C;">{r["team_type"]}</td>')
                html4.append(f'<td style="color:#2E9B72; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html4.append(f'<td style="color:#D95757; font-weight:700;">{r["Exited_Count"]}</td>')
                html4.append('</tr>')
                
            html4.append('</tbody></table></div>')
            st.markdown("".join(html4), unsafe_allow_html=True)

    else:
        st.markdown(f"#### 🔴 Employees Who Left (Exited) in Selected Period ({start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')})")
        if is_today:
            st.info("No exited employees recorded for Today selection.")
        else:
            exited_df = df_filtered[df_filtered['status_as_of_obs'] == 'Exited'].copy()
            if exited_df.empty:
                st.info("No exited employees found matching criteria.")
            else:
                html_ex = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
                html_ex.append('<th>Emp Code</th><th>Employee Name</th><th>Branch</th><th>Type</th><th>Team Type</th><th>DOJ</th><th>DOL (Exit Date)</th><th>Designation</th><th>Email</th><th>Phone</th>')
                html_ex.append('</tr></thead><tbody>')
                
                for _, r in exited_df.iterrows():
                    html_ex.append('<tr>')
                    html_ex.append(f'<td style="font-weight:700; color:#50377C;">{r["emp_code"]}</td>')
                    html_ex.append(f'<td style="text-align:left; font-weight:700; color:#2D263B;">{r["emp_name"]}</td>')
                    html_ex.append(f'<td>{r["branch"]}</td>')
                    html_ex.append(f'<td><b>{r["emp_type"]}</b></td>')
                    html_ex.append(f'<td>{r["team_type"]}</td>')
                    html_ex.append(f'<td>{r["doj"]}</td>')
                    html_ex.append(f'<td style="color:#D95757; font-weight:800;">{r["dol"]}</td>')
                    html_ex.append(f'<td style="font-size:0.9rem; color:#6E6380;">{r["designation"]}</td>')
                    html_ex.append(f'<td style="font-size:0.85rem; color:#6E6380;">{r["email"]}</td>')
                    html_ex.append(f'<td style="font-size:0.85rem; color:#6E6380;">{r["phone"]}</td>')
                    html_ex.append('</tr>')
                    
                html_ex.append('</tbody></table></div>')
                st.markdown("".join(html_ex), unsafe_allow_html=True)
                st.caption(f"Showing total **{len(exited_df)}** exited employee records.")

    render_download_section("tab3_drilldown")
