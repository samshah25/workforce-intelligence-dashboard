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

# Royal Imperial Purple Enterprise Color System (Color Palette 8)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body {
        scroll-behavior: smooth !important;
    }

    .stApp {
        background-color: #FAF8FC !important;
        background-image: 
            radial-gradient(at 50% 0%, #F3EEFA 0%, transparent 75%),
            radial-gradient(at 0% 100%, #FAF8FC 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(237, 228, 247, 0.5) 0px, transparent 50%);
        background-attachment: fixed;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #2D2D2D !important;
    }

    /* Executive Command Hero Header (#5E2D91 Solid Purple with Rich Geometric Hexagon Grid Pattern) */
    .command-hero-header {
        position: relative;
        background-color: #5E2D91 !important;
        background-image: 
            radial-gradient(circle at 12% 50%, rgba(155, 89, 182, 0.35) 0%, transparent 55%),
            radial-gradient(circle at 88% 30%, rgba(75, 34, 120, 0.45) 0%, transparent 50%),
            radial-gradient(circle at 50% 100%, rgba(123, 75, 179, 0.25) 0%, transparent 65%),
            url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%239b59b6' fill-opacity='0.08'%3E%3Cpolygon points='40,0 80,20 80,60 40,80 0,60 0,20'/%3E%3Cpath d='M40 0v80M0 20l80 40M0 60l80-40' stroke='%23ffffff' stroke-opacity='0.04' stroke-width='1'/%3E%3C/g%3E%3C/svg%3E") !important;
        padding: 2.4rem 3.2rem;
        border-radius: 26px;
        color: #FFFFFF !important;
        margin-bottom: 2rem;
        box-shadow: 0 20px 48px rgba(94, 45, 145, 0.28), inset 0 1px 1px rgba(255, 255, 255, 0.3);
        border: 1.5px solid #7B4BB3;
        overflow: hidden;
    }
    .command-hero-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #7B4BB3 0%, #9B59B6 35%, #34D399 70%, #7B4BB3 100%);
    }    .command-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        color: #FFFFFF !important;
        border: 1px solid #EDE4F7;
        font-weight: 850;
        font-size: 1.0rem;
        padding: 6px 16px;
        border-radius: 20px;
        backdrop-filter: blur(4px);
        letter-spacing: 1px;
    }
    .header-tag-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.14);
        color: #FFFFFF !important;
        border: 1px solid rgba(237, 228, 247, 0.4);
        font-weight: 850;
        font-size: 0.92rem;
        padding: 5px 14px;
        border-radius: 16px;
        backdrop-filter: blur(4px);
        letter-spacing: 0.8px;
    }
    .header-accent-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 18px;
        padding: 1.2rem 1.6rem;
        box-shadow: 0 8px 24px rgba(45, 15, 75, 0.25);
    }
    .command-title {
        font-size: 3.1rem;
        font-weight: 900;
        color: #FFFFFF !important;
        letter-spacing: -1px;
        line-height: 1.1;
        margin-top: 6px;
    }
    .command-subtitle {
        font-size: 1.25rem;
        color: #F3EEFA !important;
        margin-top: 8px;
        font-weight: 700;
    }

    /* 4-Category Dropdown Popover Header Trigger Styling */
    div[data-testid="stPopover"] {
        width: 100% !important;
        margin-bottom: 1.5rem !important;
    }
    div[data-testid="stPopover"] button,
    button[data-testid="stPopoverButton"],
    button[data-testid="stBaseButton-secondary"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #E5DDF0 !important;
        border-radius: 18px !important;
        box-shadow: 0 6px 18px rgba(45, 45, 45, 0.04) !important;
        padding: 0.9rem 1.2rem !important;
        width: 100% !important;
        color: #2D2D2D !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="stPopover"] button:hover,
    button[data-testid="stPopoverButton"]:hover {
        background: #EDE4F7 !important;
        background-color: #EDE4F7 !important;
        border-color: #7B4BB3 !important;
        box-shadow: 0 10px 24px rgba(94, 45, 145, 0.15) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stPopover"] button *,
    button[data-testid="stPopoverButton"] *,
    button[data-testid="stPopoverButton"] p,
    button[data-testid="stPopoverButton"] span,
    button[data-testid="stPopoverButton"] div,
    button[data-testid="stPopoverButton"] svg {
        color: #2D2D2D !important;
        fill: #2D2D2D !important;
        font-weight: 850 !important;
        font-size: 1.3rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* Popover Top Accent Borders */
    div[data-testid="column"]:nth-child(1) div[data-testid="stPopover"] > button {
        border-top: 5px solid #5E2D91 !important;
    }
    div[data-testid="column"]:nth-child(2) div[data-testid="stPopover"] > button {
        border-top: 5px solid #7B4BB3 !important;
    }
    div[data-testid="column"]:nth-child(3) div[data-testid="stPopover"] > button {
        border-top: 5px solid #9B59B6 !important;
    }
    div[data-testid="column"]:nth-child(4) div[data-testid="stPopover"] > button {
        border-top: 5px solid #5E2D91 !important;
    }

    /* Floating Popover Container Body Styling (#FFFFFF) */
    div[data-testid="stPopoverBody"] {
        background: #FFFFFF !important;
        backdrop-filter: blur(16px) !important;
        border: 1.5px solid #E5DDF0 !important;
        border-radius: 20px !important;
        box-shadow: 0 16px 40px rgba(94, 45, 145, 0.12) !important;
        padding: 1.4rem !important;
    }

    /* High-Contrast Time Period Chip Badge */
    .period-chip {
        background: #EDE4F7 !important;
        border: 1.5px solid #E5DDF0 !important;
        border-radius: 14px !important;
        color: #5E2D91 !important;
        font-weight: 850 !important;
        font-size: 1.2rem !important;
        padding: 12px 18px !important;
        margin-top: 14px !important;
        margin-bottom: 6px !important;
        display: block !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(94, 45, 145, 0.08) !important;
    }
    .period-chip, .period-chip * {
        color: #5E2D91 !important;
        font-weight: 850 !important;
    }

    /* Headings & Typography */
    h1, h2, h3, h4, h5, h6, .filter-section-title {
        font-size: 1.7rem !important;
        font-weight: 850 !important;
        color: #2D2D2D !important;
        letter-spacing: -0.3px !important;
        margin-bottom: 12px !important;
    }
    p, span, label, div[data-testid="stMarkdownContainer"] p {
        color: #2D2D2D;
        font-size: 1.15rem;
    }
    div[data-testid="stCaptionContainer"] {
        color: #8A8F98 !important;
        font-size: 1.05rem !important;
    }

    /* Selectbox Widget Labels */
    div[data-testid="stSelectbox"] label, label[data-testid="stWidgetLabel"] {
        font-size: 1.4rem !important;
        font-weight: 850 !important;
        color: #2D2D2D !important;
        margin-bottom: 6px !important;
    }

    /* Executive Selectbox Direct Card Styling (Whole Solid #FFFFFF White Card Like Popover) */
    div[data-testid="stSelectbox"] label,
    label[data-testid="stWidgetLabel"] {
        display: none !important;
    }
    div[data-testid="stSelectbox"] {
        margin-bottom: 1.5rem !important;
        width: 100% !important;
    }
    div[data-testid="stSelectbox"] > div {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #E5DDF0 !important;
        border-radius: 18px !important;
        box-shadow: 0 6px 18px rgba(45, 45, 45, 0.04) !important;
        padding: 0.8rem 1.2rem !important;
        min-height: 52px !important;
        height: 52px !important;
        width: 100% !important;
        color: #2D2D2D !important;
        transition: all 0.25s ease !important;
        display: flex !important;
        align-items: center !important;
    }
    /* STRIP ALL INNER BASEWEB GREY BOXES AND INNER BORDERS */
    div[data-testid="stSelectbox"] [data-baseweb="select"],
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
    }
    div[data-testid="stSelectbox"] > div:hover {
        background: #EDE4F7 !important;
        background-color: #EDE4F7 !important;
        border-color: #7B4BB3 !important;
        box-shadow: 0 10px 24px rgba(94, 45, 145, 0.15) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stSelectbox"] [data-baseweb="select"] *,
    div[data-testid="stSelectbox"] [data-baseweb="select"] p,
    div[data-testid="stSelectbox"] [data-baseweb="select"] span,
    div[data-testid="stSelectbox"] [data-baseweb="select"] div,
    div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
        font-size: 1.3rem !important;
        font-weight: 850 !important;
        color: #2D2D2D !important;
        fill: #2D2D2D !important;
        background: transparent !important;
    }

    /* Selectbox Top Accent Borders */
    div[data-testid="column"]:nth-child(2) div[data-testid="stSelectbox"] > div {
        border-top: 5px solid #5E2D91 !important;
    }
    div[data-testid="column"]:nth-child(3) div[data-testid="stSelectbox"] > div {
        border-top: 5px solid #7B4BB3 !important;
    }
    div[data-testid="column"]:nth-child(4) div[data-testid="stSelectbox"] > div {
        border-top: 5px solid #9B59B6 !important;
    }

    /* KPI Cards Styling (Scaled Up Inside Cards Typography) */
    .metric-card-exec {
        background-color: #FFFFFF !important;
        background-image: radial-gradient(circle at 90% 10%, rgba(237, 228, 247, 0.35) 0%, transparent 60%),
                          url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%235e2d91' fill-opacity='0.025'%3E%3Cpolygon points='0,0 20,0 10,10'/%3E%3C/g%3E%3C/svg%3E") !important;
        border-radius: 22px;
        padding: 1.6rem 1.3rem;
        text-align: center;
        box-shadow: 0 10px 28px rgba(45, 45, 45, 0.05);
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        border: 1.5px solid #E5E7EB;
    }
    .metric-card-exec:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 36px rgba(94, 45, 145, 0.14);
        border-color: #E5DDF0;
    }
    .metric-card-exec::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
    }

    /* 🟣 Headcount = Purple #5E2D91 / Bg #EDE4F7 */
    .kpi-emerald {
        background: #FFFFFF !important;
        border-color: #E5DDF0;
    }
    .kpi-emerald::before { background: linear-gradient(90deg, #5E2D91, #7B4BB3); }
    .metric-val-emerald { font-size: 2.95rem; font-weight: 900; color: #5E2D91; line-height: 1.1; }
    .badge-bg-emerald { background: #EDE4F7; color: #5E2D91; border: 1px solid #DCCFE8; }

    /* 🟢 Active DA = Green #28A745 / Bg #E8F8EF */
    .kpi-orange {
        background: #FFFFFF !important;
        border-color: #E5E7EB;
    }
    .kpi-orange::before { background: linear-gradient(90deg, #28A745, #34D399); }
    .metric-val-orange { font-size: 2.95rem; font-weight: 900; color: #28A745; line-height: 1.1; }
    .badge-bg-orange { background: #E8F8EF; color: #28A745; border: 1px solid #B8ECC8; }

    /* 🟠 Active ME = Orange #F39C12 / Bg #FFF3DC */
    .kpi-blue {
        background: #FFFFFF !important;
        border-color: #E5E7EB;
    }
    .kpi-blue::before { background: linear-gradient(90deg, #F39C12, #F59E0B); }
    .metric-val-blue { font-size: 2.95rem; font-weight: 900; color: #F39C12; line-height: 1.1; }
    .badge-bg-blue { background: #FFF3DC; color: #F39C12; border: 1px solid #FDE3B5; }

    /* 🔴 Active THE / Exited = Red #E74C3C / Bg #FDE6E6 */
    .kpi-rose {
        background: #FFFFFF !important;
        border-color: #E5E7EB;
    }
    .kpi-rose::before { background: linear-gradient(90deg, #E74C3C, #EF4444); }
    .metric-val-rose { font-size: 2.95rem; font-weight: 900; color: #E74C3C; line-height: 1.1; }
    .badge-bg-rose { background: #FDE6E6; color: #E74C3C; border: 1px solid #F9BFC0; }

    /* 🟣 MoM / YoY = Purple Accent #7B4BB3 */
    .kpi-cyan {
        background: #FFFFFF !important;
        border-color: #E5DDF0;
    }
    .kpi-cyan::before { background: linear-gradient(90deg, #7B4BB3, #9B59B6); }
    .metric-val-cyan { font-size: 2.95rem; font-weight: 900; color: #5E2D91; line-height: 1.1; }
    .badge-bg-cyan { background: #EDE4F7; color: #5E2D91; border: 1px solid #DCCFE8; }

    .metric-lbl-exec {
        font-size: 1.25rem;
        color: #4B5563;
        font-weight: 850;
        margin-top: 10px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .metric-badge-exec {
        display: inline-block;
        font-size: 1.05rem;
        font-weight: 850;
        padding: 6px 16px;
        border-radius: 16px;
        margin-top: 10px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.03);
    }

    /* Tenure Table (#5E2D91 Header, #FFFFFF Normal, #F8F5FB Alternate, #F3EEFA Hover, #E5DDF0 Borders) */
    .custom-table-card {
        background: #FFFFFF !important;
        backdrop-filter: blur(12px);
        border-radius: 22px;
        padding: 1.8rem;
        border: 1.5px solid #E5DDF0;
        box-shadow: 0 10px 30px rgba(45, 45, 45, 0.05);
        margin-bottom: 2rem;
        overflow-x: auto;
    }
    .custom-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 16px;
        overflow: hidden;
        font-size: 1.18rem;
    }
    .custom-table th {
        background: linear-gradient(135deg, #5E2D91 0%, #4B2278 100%) !important;
        color: #FFFFFF !important;
        font-weight: 850;
        padding: 20px 24px;
        text-align: center;
        border-bottom: 3px solid #7B4BB3;
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .custom-table td {
        padding: 18px 24px;
        text-align: center;
        border-bottom: 1px solid #E5DDF0;
        color: #2D2D2D !important;
        font-weight: 750;
        font-size: 1.18rem;
    }
    .custom-table tr:nth-child(odd) td {
        background-color: #FFFFFF !important;
    }
    .custom-table tr:nth-child(even) td {
        background-color: #F8F5FB !important;
    }
    .custom-table tr:hover td {
        background-color: #F3EEFA !important;
        color: #2D2D2D !important;
    }
    .custom-table tr.total-row td {
        background: linear-gradient(135deg, #5E2D91 0%, #7B4BB3 100%) !important;
        color: #FFFFFF !important;
        font-weight: 850 !important;
        font-size: 1.25rem !important;
    }

    /* Export & Download Section (#FAF7FC Bg with Geometric Grid, #E1D5EA Border, #5E2D91 Icons/Headings) */
    .export-footer {
        background-color: #FAF7FC !important;
        background-image: radial-gradient(circle at 95% 50%, rgba(237, 228, 247, 0.4) 0%, transparent 50%),
                          url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 0l20 20-20 20L0 20z' fill='%235e2d91' fill-opacity='0.02'/%3E%3C/svg%3E") !important;
        backdrop-filter: blur(12px);
        border: 1.5px solid #E1D5EA;
        border-top: 4px solid #5E2D91;
        border-radius: 20px;
        padding: 2.0rem 2.6rem;
        margin-top: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(45, 45, 45, 0.05);
    }
    .export-title {
        font-size: 1.5rem;
        font-weight: 850;
        color: #5E2D91;  color: #5E2D91;
        margin-bottom: 0.4rem;
    }

    /* Streamlit Download Buttons inside Export Section */
    div[data-testid="stDownloadButton"] button {
        background: #FFFFFF !important;
        color: #5E2D91 !important;
        border: 1.5px solid #DCCFE8 !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 12px rgba(94, 45, 145, 0.06) !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: #EDE4F7 !important;
        color: #4B2278 !important;
        border-color: #7B4BB3 !important;
    }

    /* Reset main tab container - do NOT wrap tables in a card */
    div[data-testid="stTabs"] {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }

    div[data-testid="stTabContent"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Clean Floating Parent Tab Header Track (No Outer White Background Card) */
    .stTabs [role="tablist"],
    .stTabs [data-baseweb="tab-list"],
    div[data-testid="stTabs"] [role="tablist"],
    div[data-testid="stTabs"] [data-baseweb="tab-list"],
    div[role="tablist"] {
        gap: 12px !important;
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.4rem !important;
        box-shadow: none !important;
        width: fit-content !important;
        max-width: 100% !important;
    }

    /* Clean Floating Child Filter Container (No Outer White Background Card - Tight Gap Below Parent Tab) */
    .stTabs div[data-testid="stTabContent"] > div:first-child,
    .stTabs div[data-testid="stRadio"] {
        background: transparent !important;
        background-color: transparent !important;
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

    /* Child Filter Segmented Bar Container (Dynamic centering transition) */
    div[data-testid="stRadio"] {
        margin-left: 0px;
        transition: margin-left 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* ALL Parent Tab Buttons (Both Active & Inactive) - Scaled 1.45rem Executive Size */
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
        border: 1.5px solid #A7F3D0 !important;
        border-radius: 16px !important;
        padding: 14px 32px !important;
        min-height: 58px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        cursor: pointer !important;
        box-shadow: 0 4px 14px rgba(4, 120, 87, 0.05) !important;
        transition: all 0.25s ease !important;
    }

    /* ALL NESTED TEXT ELEMENTS IN PARENT TABS */
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
        font-size: 1.45rem !important;
        font-weight: 850 !important;
        color: #047857 !important;
        background: transparent !important;
        white-space: nowrap !important;
        line-height: 1.2 !important;
    }

    /* Parent Tab Hover State (#ECFDF5 Bg, #065F46 Text) */
    .stTabs button:hover,
    .stTabs button:hover *,
    div[data-testid="stTabs"] button:hover,
    div[data-testid="stTabs"] button:hover * {
        background: #ECFDF5 !important;
        background-color: #ECFDF5 !important;
        color: #065F46 !important;
        border-color: #059669 !important;
    }

    /* ACTIVE PARENT TAB BUTTON (#047857 Solid Emerald Background) */
    .stTabs button[aria-selected="true"],
    .stTabs [data-baseweb="tab"][aria-selected="true"],
    .stTabs [data-testid="stTab"][aria-selected="true"],
    div[data-testid="stTabs"] button[aria-selected="true"],
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
    div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"],
    div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] {
        background: #047857 !important;
        background-color: #047857 !important;
        border: 1.5px solid #047857 !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 24px rgba(4, 120, 87, 0.35) !important;
    }

    /* ACTIVE PARENT TAB INNER TEXT (CRISP WHITE #FFFFFF) */
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
        font-size: 1.45rem !important;
        font-weight: 850 !important;
    }

    /* Completely Remove Streamlit Tab List Gray Bottom Border Line & Underlines */
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

    /* Child Filter Segmented Control Bar (Emerald Slate Theme - Refined & Precision Micro-Scaled) */
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 4px !important;
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        background: #047857 !important;
        padding: 3.5px 4.5px !important;
        border-radius: 11px !important;
        border: 1px solid #065F46 !important;
        margin-top: 4px !important;
        margin-bottom: 4px !important;
        width: fit-content !important;
        box-shadow: 0 2.5px 9px rgba(4, 120, 87, 0.19) !important;
    }

    /* Unselected Child Filter Options (0.98rem Precision Scale) */
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label {
        font-size: 0.98rem !important;
        font-weight: 750 !important;
        color: rgba(255, 255, 255, 0.93) !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 7.5px !important;
        padding: 5px 14px !important;
        opacity: 0.91 !important;
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
        color: rgba(255, 255, 255, 0.93) !important;
        font-size: 0.98rem !important;
        font-weight: 750 !important;
        white-space: nowrap !important;
        display: inline !important;
    }
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        opacity: 1.0 !important;
        background: rgba(255, 255, 255, 0.19) !important;
        border-radius: 7.5px !important;
    }

    /* ACTIVE SELECTED CHILD FILTER OPTION (PRECISION MICRO-SCALED WHITE PILL WITH EMERALD TEXT - 0.98rem) */
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: #047857 !important;
        font-weight: 850 !important;
        opacity: 1.0 !important;
        border-radius: 7.5px !important;
        padding: 5px 14px !important;
        border: 1px solid #FFFFFF !important;
        box-shadow: 0 2.5px 7px rgba(0, 0, 0, 0.13) !important;
        transform: none !important;
    }
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p,
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) span,
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) div {
        color: #047857 !important;
        background: transparent !important;
        font-size: 0.98rem !important;
        font-weight: 850 !important;
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

# Hero Banner (Emerald Slate Executive Command Headbar)
st.markdown("""
<div class="command-hero-header" style="padding: 3.2rem 4.0rem; border-radius: 28px; background: linear-gradient(135deg, #064E3B 0%, #047857 50%, #022C22 100%) !important; box-shadow: 0 24px 60px rgba(4, 120, 87, 0.35), inset 0 1.5px 2px rgba(255, 255, 255, 0.35); border: 1.8px solid rgba(52, 211, 153, 0.4);">
    <div style="text-align: left; position: relative; z-index: 2;">
        <div class="command-title" style="margin: 0; font-size: 3.5rem; font-weight: 900; letter-spacing: -0.8px; line-height: 1.15; color: #FFFFFF; text-shadow: 0 6px 24px rgba(0,0,0,0.38), 0 2px 6px rgba(0,0,0,0.25);">
            Employee Headcount & Tenure Dashboard
        </div>
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

            // Clear popover open tag on full page refresh / reload so it does not auto-open on refresh
            try {
                var navEntries = performance.getEntriesByType('navigation');
                var isReload = (navEntries.length > 0 && navEntries[0].type === 'reload');
                if (isReload || !targetDoc._hasInitPageTop) {
                    targetDoc._hasInitPageTop = true;
                    sessionStorage.removeItem("openPopoverTag");
                    sessionStorage.removeItem("isCustomCalendarMode");
                    sessionStorage.removeItem("should_autoscroll_to_section");
                    sessionStorage.removeItem("user_scrolled_down");
                }
            } catch(err) {}

            function keepPageAtTop() {
                try {
                    var mainContainer = targetDoc.querySelector('div[data-testid="stAppViewContainer"], section.main');
                    if (mainContainer) {
                        if (!sessionStorage.getItem("should_autoscroll_to_section") && !sessionStorage.getItem("user_scrolled_down")) {
                            mainContainer.scrollTop = 0;
                        }
                    }
                } catch(e) {}
            }

            targetDoc.addEventListener('scroll', function(e) {
                var mainContainer = targetDoc.querySelector('div[data-testid="stAppViewContainer"], section.main');
                if (mainContainer) {
                    if (mainContainer.scrollTop > 250) {
                        sessionStorage.setItem("user_scrolled_down", "true");
                    } else {
                        sessionStorage.removeItem("user_scrolled_down");
                    }
                }
            }, true);

            function alignChildFilterBar() {
                try {
                    var activeTabBtn = targetDoc.querySelector('div[data-testid="stTabs"] button[aria-selected="true"], div[data-testid="stTabs"] [aria-selected="true"]');
                    var activeTabContent = targetDoc.querySelector('div[data-testid="stTabContent"]:not([hidden]), div[role="tabpanel"]:not([hidden])');
                    
                    if (activeTabBtn && activeTabContent) {
                        var radioBar = activeTabContent.querySelector('div[data-testid="stRadio"]');
                        if (radioBar) {
                            var tabRect = activeTabBtn.getBoundingClientRect();
                            var contentRect = activeTabContent.getBoundingClientRect();
                            var tabCenter = tabRect.left + (tabRect.width / 2);
                            var radioWidth = radioBar.getBoundingClientRect().width;
                            
                            if (radioWidth > 0 && contentRect.width > 0) {
                                var targetLeft = tabCenter - (radioWidth / 2) - contentRect.left;
                                if (targetLeft < 0) targetLeft = 0;
                                var maxLeft = contentRect.width - radioWidth;
                                if (maxLeft > 0 && targetLeft > maxLeft) targetLeft = maxLeft;
                                
                                radioBar.style.setProperty('margin-left', Math.round(targetLeft) + 'px', 'important');
                            }
                        }
                    }
                } catch(err) {}
            }
            setInterval(alignChildFilterBar, 120);
            targetDoc.defaultView.addEventListener('resize', alignChildFilterBar);

            function checkAutoScrollToSection() {
                try {
                    if (sessionStorage.getItem("should_autoscroll_to_section") === "true") {
                        var tableCard = targetDoc.querySelector('.custom-table-card, table.custom-table');
                        var mainContainer = targetDoc.querySelector('div[data-testid="stAppViewContainer"], section.main');
                        
                        if (tableCard) {
                            sessionStorage.removeItem("should_autoscroll_to_section");
                            sessionStorage.setItem("user_scrolled_down", "true");
                            
                            setTimeout(function() {
                                var rect = tableCard.getBoundingClientRect();
                                var containerRect = mainContainer ? mainContainer.getBoundingClientRect() : { top: 0 };
                                var currentScroll = mainContainer ? mainContainer.scrollTop : (targetDoc.defaultView.pageYOffset || 0);
                                var targetTop = currentScroll + (rect.top - containerRect.top) - 15;
                                
                                if (mainContainer) {
                                    mainContainer.scrollTo({
                                        top: Math.max(0, targetTop),
                                        behavior: 'smooth'
                                    });
                                }
                                if (targetDoc.defaultView) {
                                    targetDoc.defaultView.scrollTo({
                                        top: Math.max(0, targetTop),
                                        behavior: 'smooth'
                                    });
                                }
                            }, 80);
                        }
                    }
                } catch(err) {}
            }
            setInterval(checkAutoScrollToSection, 100);

            function getExpanderIdx(exp) {
                var all = Array.from(targetDoc.querySelectorAll('div[data-testid="stExpander"]'));
                return 'exp_idx_' + all.indexOf(exp);
            }

            if (!targetDoc._hasExpanderPersistListenerP5) {
                targetDoc._hasExpanderPersistListenerP5 = true;

                targetDoc.addEventListener('click', function(e) {
                    var radioBar = e.target.closest('div[data-testid="stRadio"], div[role="radiogroup"], label[data-baseweb="radio"]');
                    if (radioBar) {
                        sessionStorage.setItem("should_autoscroll_to_section", "true");
                    }

                    var popoverBody = e.target.closest('div[data-testid="stPopoverBody"]');
                    var popoverBtn = e.target.closest('button[data-testid="stPopoverButton"]');
                    var isCustomCal = sessionStorage.getItem("isCustomCalendarMode") === "true";

                    if (popoverBody) {
                        var isTimePopover = popoverBody.innerText && (
                            popoverBody.innerText.includes("Select Time Mode") || 
                            popoverBody.innerText.includes("Monthly (MTD)") ||
                            popoverBody.innerText.includes("Custom Calendar") ||
                            popoverBody.innerText.includes("Date Range") ||
                            popoverBody.innerText.includes("Select Year")
                        );
                        if (isTimePopover && !targetDoc._preventPopoverReopen) {
                            sessionStorage.setItem("openPopoverTag", "time");
                        }
                    } else if (popoverBtn) {
                        var btnText = popoverBtn.innerText || "";
                        if (btnText.includes("Time Period") || btnText.includes("🗓️") || btnText.includes("📊") || btnText.includes("📆") || btnText.includes("📅")) {
                            sessionStorage.setItem("openPopoverTag", "time");
                        } else {
                            if (!isCustomCal) {
                                sessionStorage.removeItem("openPopoverTag");
                            }
                        }
                    } else {
                        var isInsideSelectDropdown = e.target.closest('ul[role="listbox"]') || 
                                                     e.target.closest('div[role="listbox"]') ||
                                                     e.target.closest('div[data-baseweb="menu"]') ||
                                                     e.target.closest('div[data-baseweb="calendar"]') ||
                                                     e.target.closest('div[data-baseweb="datepicker"]') ||
                                                     e.target.closest('div[data-baseweb="popover"]') ||
                                                     e.target.closest('div[role="gridcell"]') ||
                                                     e.target.closest('button[aria-label="Previous month"]') ||
                                                     e.target.closest('button[aria-label="Next month"]');
                        if (isInsideSelectDropdown || isCustomCal) {
                            sessionStorage.setItem("openPopoverTag", "time");
                        } else {
                            sessionStorage.removeItem("openPopoverTag");
                        }
                    }

                    var isCalendarClick = e.target.closest('div[data-baseweb="calendar"]') ||
                                         e.target.closest('div[data-baseweb="datepicker"]') ||
                                         e.target.closest('input[aria-label="Date Range"]') ||
                                         e.target.closest('div[role="gridcell"]') ||
                                         e.target.closest('button[aria-label="Previous month"]') ||
                                         e.target.closest('button[aria-label="Next month"]');
                    if (isCalendarClick) {
                        sessionStorage.setItem("openPopoverTag", "time");
                    }

                    var opt = e.target.closest('li[role="option"]') || e.target.closest('div[role="option"]') || e.target.closest('[role="option"]');
                    if (opt) {
                        var optTxt = opt.innerText ? opt.innerText.trim() : "";
                        
                        var isEmpOption = ["All EmpTypes", "JDA", "ME", "TME", "JDS"].indexOf(optTxt) !== -1;
                        var isBranchOption = ["All 11 Cities", "Ahmedabad", "Bangalore", "Chandigarh", "Chennai", "Coimbatore", "Delhi", "Hyderabad", "Jaipur", "Kolkata", "Mumbai", "Pune"].indexOf(optTxt) !== -1;
                        var isTeamOption = (optTxt === "All Teams") || ["B2B BDE", "BLANK", "Bounce", "Corporate", "Corporate ME", "DF", "Field Sales", "Hot Data", "JDA Corporate", "JDA Direct", "JDA Partner", "Key Accounts", "Merchant Onboarding", "Multiple team", "Online", "Revival (Expiry)", "SHT", "Super", "Super Cat", "trainee"].indexOf(optTxt) !== -1;

                        var isScopeOption = isEmpOption || isBranchOption || isTeamOption;

                        if (isScopeOption) {
                            // 1-CLICK INSTANT AUTO CLOSE FOR EMPLOYEE, BRANCH, AND TEAM POPOVERS!
                            sessionStorage.removeItem("openPopoverTag");
                            sessionStorage.removeItem("isCustomCalendarMode");
                            targetDoc._preventPopoverReopen = true;
                            setTimeout(function() {
                                targetDoc.body.click();
                                var activePopoverBodys = targetDoc.querySelectorAll('div[data-testid="stPopoverBody"]');
                                activePopoverBodys.forEach(function(pb) { pb.style.display = 'none'; });
                                setTimeout(function() {
                                    targetDoc._preventPopoverReopen = false;
                                }, 500);
                            }, 50);
                        } else {
                            // TIME PERIOD POPOVER MULTI-STEP LOGIC
                            var activePopoverBody = targetDoc.querySelector('div[data-testid="stPopoverBody"]');
                            var bodyText = activePopoverBody ? activePopoverBody.innerText : "";
                            
                            var isCustomCalendarActive = (sessionStorage.getItem("isCustomCalendarMode") === "true") || bodyText.includes("Custom Calendar") || bodyText.includes("Date Range");
                            var isCustomCalendarOption = optTxt.includes("Custom Calendar");
                            
                            if (isCustomCalendarOption) {
                                sessionStorage.setItem("isCustomCalendarMode", "true");
                                sessionStorage.setItem("openPopoverTag", "time");
                            }

                            var isYearModeActive = bodyText.includes("Yearly") && !bodyText.includes("Monthly (MTD)") && !isCustomCalendarActive;
                            var isYearNum = /^\d{4}$/.test(optTxt);
                            var isMonthName = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].indexOf(optTxt) !== -1;
                            var isQuarterName = optTxt.startsWith("Q1") || optTxt.startsWith("Q2") || optTxt.startsWith("Q3") || optTxt.startsWith("Q4");
                            var isToday = (optTxt === "Today" || optTxt.includes("Today"));

                            if (optTxt === "Monthly (MTD)" || optTxt.includes("Monthly") || optTxt === "Quarterly" || optTxt === "Yearly" || isToday) {
                                sessionStorage.removeItem("isCustomCalendarMode");
                            }

                            // CUSTOM CALENDAR MODE NEVER AUTO-CLOSES!
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
                                    }, 300);
                                }, 60);
                            }
                        }
                    }
                }

                function alignChildFilterToActiveTab() {
                    try {
                        var tabList = targetDoc.querySelector('.stTabs [role="tablist"], [data-baseweb="tab-list"], [role="tablist"]');
                        if (!tabList) return;
                        
                        var activeTab = tabList.querySelector('button[aria-selected="true"], [data-baseweb="tab"][aria-selected="true"], [aria-selected="true"]');
                        if (!activeTab) return;
                        
                        var tabListRect = tabList.getBoundingClientRect();
                        var activeTabRect = activeTab.getBoundingClientRect();
                        var activeTabCenter = (activeTabRect.left - tabListRect.left) + (activeTabRect.width / 2);
                        
                        var tabPanels = Array.from(targetDoc.querySelectorAll('div[data-testid="stTabContent"], div[role="tabpanel"]'));
                        tabPanels.forEach(function(panel) {
                            var radioContainer = panel.querySelector('div[data-testid="stRadio"]');
                            if (radioContainer) {
                                var radioWidth = radioContainer.offsetWidth || 440;
                                var offsetLeft = Math.max(0, Math.round(activeTabCenter - (radioWidth / 2)));
                                radioContainer.style.setProperty('margin-left', offsetLeft + 'px', 'important');
                            }
                        });
                    } catch(err) {}
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

# Branch & Team Scope Lists (Dynamic extraction from dataset)
tme_all_teams = sorted([str(t) for t in raw_df['team_type'].dropna().unique() if str(t).strip() != ""])
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
            sel_q_name = st.selectbox("Quarter", options=["Q1 (Apr-Jun)", "Q2 (Jul-Sep)", "Q3 (Oct-Dec)", "Q4 (Jan-Mar)"], index=1, key="hdr_dd_q_quarter")
            
            sq = sel_q_name.split(" ")[0]
            q_start_dates = {"Q1": datetime(sel_year, 4, 1), "Q2": datetime(sel_year, 7, 1), "Q3": datetime(sel_year, 10, 1), "Q4": datetime(sel_year + 1, 1, 1)}
            q_end_dates = {"Q1": datetime(sel_year, 6, 30), "Q2": datetime(sel_year, 9, 30), "Q3": datetime(sel_year, 12, 31), "Q4": datetime(sel_year + 1, 3, 31)}
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
            components.html("""
            <script>
                sessionStorage.setItem("isCustomCalendarMode", "true");
                sessionStorage.setItem("openPopoverTag", "time");
            </script>
            """, height=0, width=0)
            cal_range = st.date_input("Date Range", value=(date(2026, 8, 1), date(2026, 8, 31)), min_value=date(2018, 1, 1), max_value=date(2028, 12, 31), key="hdr_dd_cal_range")
            if isinstance(cal_range, (tuple, list)) and len(cal_range) == 2:
                start_date = pd.Timestamp(cal_range[0])
                end_date = pd.Timestamp(cal_range[1])
                st.markdown(f'<div class="period-chip">📅 {start_date.strftime("%d %b %Y")} to {end_date.strftime("%d %b %Y")}</div>', unsafe_allow_html=True)
            else:
                start_date = pd.Timestamp(today)
                end_date = pd.Timestamp(today)

# 2. 👤 Employee Scope Category Dropdown (White Popover Card - Identical to Time Period)
with filter_c2:
    with st.popover(emp_type_header_label, use_container_width=True):
        emp_type_option = st.selectbox(
            "Select Employee Type",
            ["All EmpTypes", "JDA", "ME", "TME", "JDS"],
            index=0,
            key="hdr_dd_emp_type",
            label_visibility="collapsed"
        )

# 3. 🏢 Branch Scope Category Dropdown (White Popover Card - Identical to Time Period)
with filter_c3:
    with st.popover(city_header_label, use_container_width=True):
        selected_city_single = st.selectbox(
            "Select Branch/City",
            branches_11_options,
            index=0,
            key="hdr_dd_city",
            label_visibility="collapsed"
        )

# 4. 👥 Team Scope Category Dropdown (White Popover Card - Identical to Time Period)
with filter_c4:
    with st.popover(team_header_label, use_container_width=True):
        selected_team_single = st.selectbox(
            "Select Team Scope",
            team_type_single_options,
            index=0,
            key="hdr_dd_team",
            label_visibility="collapsed"
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

# Main Metrics (Total employees who worked during the selected period)
total_count = len(df_filtered)
if total_count > 0:
    active_count = len(df_filtered) # Total worked during period
    exited_count = len(df_filtered[df_filtered['status_as_of_obs'] == 'Exited'])
    
    active_jda_count = len(df_filtered[df_filtered['emp_type'] == 'JDA'])
    active_me_count = len(df_filtered[df_filtered['emp_type'] == 'ME'])
    active_tme_count = len(df_filtered[df_filtered['emp_type'] == 'TME'])
    
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

# Calculate YoY %, MoM %, QtQ % with Respect to Selected Filter Period
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

# Exact Prior Period Dates matching Selected Period (`start_date` to `end_date`)
mom_start = start_date - pd.DateOffset(months=1)
mom_end = end_date - pd.DateOffset(months=1)

# Function to get exact Previous Financial Quarter Start & End Dates (Q1: Apr-Jun, Q2: Jul-Sep, Q3: Oct-Dec, Q4: Jan-Mar)
def get_previous_quarter_dates(ref_date):
    m = ref_date.month
    y = ref_date.year
    if m in [4, 5, 6]:    # Current: Q1 (Apr-Jun) -> Previous Quarter: Q4 same year (Jan-Mar y)
        return pd.Timestamp(datetime(y, 1, 1)), pd.Timestamp(datetime(y, 3, 31))
    elif m in [7, 8, 9]:  # Current: Q2 (Jul-Sep) -> Previous Quarter: Q1 same year (Apr-Jun y)
        return pd.Timestamp(datetime(y, 4, 1)), pd.Timestamp(datetime(y, 6, 30))
    elif m in [10, 11, 12]: # Current: Q3 (Oct-Dec) -> Previous Quarter: Q2 same year (Jul-Sep y)
        return pd.Timestamp(datetime(y, 7, 1)), pd.Timestamp(datetime(y, 9, 30))
    else:                 # Current: Q4 (Jan-Mar) -> Previous Quarter: Q3 prior year (Oct-Dec y-1)
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

# ==============================================================================
# Calculate New Joiners in selected period
if not df_filtered.empty:
    new_joiners_count = ((pd.to_datetime(df_filtered['doj']) >= start_date) & (pd.to_datetime(df_filtered['doj']) <= end_date)).sum()
else:
    new_joiners_count = 0

# ==============================================================================
# TOP EXECUTIVE KPI METRIC CARDS (PERIOD & EMPTYPE SCALED)
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)

time_mode_current = st.session_state.get("hdr_dd_time_mode", "Monthly (MTD)")

if time_mode_current == "Yearly":
    # YEARLY MODE (ANY EMPTYPE): Remove MoM & QtQ, add New Joiners in Year! (4 Cards)
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
    # QUARTERLY MODE (ANY EMPTYPE): Remove MoM, keep QtQ, add New Joiners in Quarter! (5 Cards)
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
    # MONTHLY (MTD) / TODAY / CUSTOM CALENDAR MODE
    if time_mode_current == "Today":
        # TODAY MODE (ANY EMPTYPE): 4 Cards (Headcount, MoM %, QtQ %, YoY %)
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
        # ALL EMPTYPES IN MONTHLY / CUSTOM CALENDAR MODE: 4 Cards (Headcount, Active JDA, Active ME, Active TME)
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
        # MONTHLY / CUSTOM CALENDAR MODE FOR SPECIFIC EMPTYPE: 5 Cards (Headcount, Exited, MoM, New Joiners, YoY)
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
        <div style="font-size: 0.92rem; color: #5E2D91; margin-bottom: 0.9rem; font-weight:600;">
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
        
        is_today = (time_mode_current == "Today")

        if s_mode == "📊 Pan India / Branch Summary":
            st.markdown(f"#### 📊 {'Pan India' if is_pan_india else selected_branches[0]} Headcount Summary")
            
            br_hc_df = df_filtered.groupby('branch').agg(
                Active_Count=('emp_code', 'count'), # Total worked in period
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
                html_b.append(f'<td style="font-weight:700; text-align:left; color:#047857;">{r["branch"]}</td>')
                html_b.append(f'<td style="color:#059669; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html_b.append(f'<td style="color:#E11D48; font-weight:700;">{r["Exited_Count"]}</td>')
                    html_b.append(f'<td style="color:#0284C7; font-weight:800;">{r["New_Joiners_Count"]}</td>')
                html_b.append('</tr>')
            html_b.append('</tbody></table></div>')
            st.markdown("".join(html_b), unsafe_allow_html=True)

        else: # 👥 Team Type Summary
            st.markdown("#### 👥 Team Type Headcount Summary")
            team_hc_df = df_filtered.groupby('team_type').agg(
                Active_Count=('emp_code', 'count'), # Total worked in period
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
                html_t.append(f'<td style="font-weight:700; text-align:left; color:#047857;">{r["team_type"]}</td>')
                html_t.append(f'<td style="color:#059669; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html_t.append(f'<td style="color:#E11D48; font-weight:700;">{r["Exited_Count"]}</td>')
                    html_t.append(f'<td style="color:#0284C7; font-weight:800;">{r["New_Joiners_Count"]}</td>')
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
            options=["⏳ Overall Tenure Buckets", "🏢 Branch-Wise Tenure", "👥 Team-Wise Tenure"],
            index=0,
            horizontal=True,
            key="tenure_view_pill_toggle",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)

        if "Overall Tenure" in v_mode:
            st.markdown(f"#### ⏳ Headcount Wise Tenure ({start_date.strftime('%d-%b-%Y')} to {end_date.strftime('%d-%b-%Y')})")
            
            tb_df = df_filtered.groupby('tenure_bucket').agg(
                Total_Headcount=('emp_code', 'count'), # Total worked in this bucket
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
                html_tb.append(f'<td style="font-weight:700; text-align:left; color:#047857;">{r["tenure_bucket"]}</td>')
                html_tb.append(f'<td style="color:#059669; font-weight:800;">{int(r["Total_Headcount"])}</td>')
                if not is_today:
                    html_tb.append(f'<td style="color:#E11D48; font-weight:700;">{int(r["Exited_Count"])}</td>')
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
                html_bp.append(f'<td style="font-weight:700; text-align:left; color:#047857;">{r["branch"]}</td>')
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
                html_tp.append(f'<td style="font-weight:700; text-align:left; color:#047857;">{r["team_type"]}</td>')
                for bo in bucket_order:
                    html_tp.append(f'<td>{int(r[bo])}</td>')
                html_tp.append('</tr>')
            html_tp.append('</tbody></table></div>')
            st.markdown("".join(html_tp), unsafe_allow_html=True)

    render_download_section("tab2_tenure_breakdown")

# ------------------------------------------------------------------------------
# TAB 3: EMPLOYEE DRILL-DOWN & DATA MATRICES
# ------------------------------------------------------------------------------
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
                html5.append(f'<td style="font-weight:700; color:#7B4BB3;">{r["emp_code"]}</td>')
                html5.append(f'<td style="text-align:left; font-weight:700; color:#172033;">{r["emp_name"]}</td>')
                html5.append(f'<td style="color:#5E2D91;">{r["branch"]}</td>')
                html5.append(f'<td><b>{r["emp_type"]}</b></td>')
                html5.append(f'<td>{r["team_type"]}</td>')
                html5.append(f'<td>{r["doj"]}</td>')
                html5.append(f'<td>{dol_str}</td>')
                html5.append(f'<td style="font-size:0.9rem; color:#59677D;">{r["designation"]}</td>')
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
                Active_Count=('emp_code', 'count'), # Total worked in period
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
                html3.append(f'<td style="text-align:left; font-weight:700; color:#047857;">{r["branch"]}</td>')
                html3.append(f'<td style="color:#059669; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html3.append(f'<td style="color:#E11D48; font-weight:700;">{r["Exited_Count"]}</td>')
                html3.append('</tr>')
                
            html3.append('</tbody></table></div>')
            st.markdown("".join(html3), unsafe_allow_html=True)

    elif d_mode == "👥 Team List":
        st.markdown("#### 👥 Team-Wise Table")
        if df_filtered.empty:
            st.warning("No records matching filter criteria.")
        else:
            team_stats = df_filtered.groupby('team_type').agg(
                Active_Count=('emp_code', 'count'), # Total worked in period
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
                html4.append(f'<td style="text-align:left; font-weight:700; color:#047857;">{r["team_type"]}</td>')
                html4.append(f'<td style="color:#059669; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html4.append(f'<td style="color:#E11D48; font-weight:700;">{r["Exited_Count"]}</td>')
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
                st.info("No employees exited during the selected period.")
            else:
                st.write(f"Total **{len(exited_df)}** employee(s) exited during this period:")
                
                html_ex = ['<div class="custom-table-card"><table class="custom-table"><thead><tr>']
                html_ex.append('<th>Emp Code</th><th>Employee Name</th><th>Branch</th><th>Type</th><th>Team Type</th><th>DOJ</th><th>DOL (Exit Date)</th><th>Designation</th><th>Email</th><th>Phone</th>')
                html_ex.append('</tr></thead><tbody>')
                
                for _, r in exited_df.iterrows():
                    dol_str = r['dol'] if pd.notnull(r['dol']) and str(r['dol']).strip() != "" else "-"
                    
                    html_ex.append('<tr>')
                    html_ex.append(f'<td style="font-weight:700; color:#E74C3C;">{r["emp_code"]}</td>')
                    html_ex.append(f'<td style="text-align:left; font-weight:700; color:#172033;">{r["emp_name"]}</td>')
                    html_ex.append(f'<td>{r["branch"]}</td>')
                    html_ex.append(f'<td><b>{r["emp_type"]}</b></td>')
                    html_ex.append(f'<td>{r["team_type"]}</td>')
                    html_ex.append(f'<td>{r["doj"]}</td>')
                    html_ex.append(f'<td style="color:#E74C3C; font-weight:800;">{dol_str}</td>')
                    html_ex.append(f'<td style="font-size:0.9rem; color:#59677D;">{r["designation"]}</td>')
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
