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

# True Merged Palette (Port 8595 Imperial Purple #5E2D91 + Port 8590 Oceanic Cyan #0284C7 & Midnight Sapphire #0F172A)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* HIDE ALL STREAMLIT WATERMARKS, FOOTERS, HEADERS, MENU & DEPLOY BUTTONS */
    #MainMenu { visibility: hidden !important; display: none !important; }
    header { visibility: hidden !important; display: none !important; }
    footer { visibility: hidden !important; display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    div[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stStatusWidget"] { display: none !important; }
    .viewerBadge_container__1QSob { display: none !important; }
    div[class*="viewerBadge"] { display: none !important; }
    div[class*="stAppHeader"] { display: none !important; }
    button[title="View app in Streamlit Community Cloud"] { display: none !important; }

    /* REDUCE TOP PADDING & MOVE ENTIRE WEBSITE UP TO THE VERY TOP EDGE */
    .block-container,
    div[data-testid="block-container"],
    .main .block-container,
    section.main > div {
        padding-top: 0.6rem !important;
        padding-bottom: 1.5rem !important;
        margin-top: 0px !important;
    }
    div[data-testid="stHeader"],
    header[data-testid="stHeader"] {
        height: 0px !important;
        min-height: 0px !important;
        display: none !important;
    }

    html, body {
        scroll-behavior: smooth !important;
    }

    .stApp {
        background-color: #F8FAFC !important;
        background-image: 
            /* Clean Light Ambient Executive Mesh Auras */
            radial-gradient(at 12% 5%, rgba(233, 213, 255, 0.55) 0px, transparent 45%),
            radial-gradient(at 88% 12%, rgba(224, 242, 254, 0.55) 0px, transparent 50%),
            radial-gradient(at 50% 45%, rgba(243, 232, 255, 0.4) 0px, transparent 60%),
            radial-gradient(at 20% 88%, rgba(209, 250, 229, 0.35) 0px, transparent 45%);
        background-size: 100% 100%, 100% 100%, 100% 100%, 100% 100%;
        background-attachment: fixed;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A !important;
    }

    /* HIGH-CONTRAST ACCESSIBILITY KEYBOARD FOCUS RINGS MATCHING FILTER CARD CURVES 100% */
    :focus-visible,
    button:focus-visible,
    div[role="button"]:focus-visible,
    label:focus-visible,
    input:focus-visible,
    select:focus-visible,
    [tabindex]:focus-visible,
    .stTabs button:focus-visible,
    div[data-testid="stTabs"] button:focus-visible,
    .stTabs div[data-testid="stRadio"] label:focus-visible {
        outline: 3px solid #5E2D91 !important;
        outline-offset: 2px !important;
        box-shadow: 0 0 0 4px rgba(94, 45, 145, 0.25) !important;
        border-radius: 10px !important;
    }

    /* Executive Command Hero Header (Silky Smooth Imperial Purple Gradient) */
    .command-hero-header {
        position: relative;
        background: linear-gradient(135deg, #4A1D75 0%, #5E2D91 40%, #7B4BB3 75%, #3B1C63 100%) !important;
        padding: 1.4rem 2.2rem !important;
        border-radius: 14px !important;
        color: #FFFFFF !important;
        margin-bottom: 1.4rem !important;
        box-shadow: 0 14px 35px rgba(94, 45, 145, 0.38), inset 0 1px 2px rgba(255, 255, 255, 0.3);
        border: 1.5px solid rgba(255, 255, 255, 0.28);
        overflow: hidden;
    }
    .command-hero-header h1 {
        font-size: 1.65rem !important;
        font-weight: 900 !important;
        margin: 0 !important;
    }
    .command-hero-header p {
        font-size: 0.88rem !important;
        margin-top: 0.3rem !important;
    }

    /* 4-CATEGORY DROPDOWN POPOVER HEADER TRIGGERS (REDUCED 0.76rem FONT SIZE) */
    div[data-testid="stPopover"] {
        width: 100% !important;
        margin-bottom: 0.8rem !important;
    }
    div[data-testid="stPopover"] button,
    button[data-testid="stPopoverButton"],
    button[data-testid="stBaseButton-secondary"] {
        border-radius: 9px !important;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05) !important;
        padding: 0.35rem 0.6rem !important;
        min-height: 32px !important;
        width: 100% !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="stPopover"] button:hover,
    button[data-testid="stPopoverButton"]:hover {
        transform: translateY(-1.5px) !important;
        box-shadow: 0 5px 14px rgba(15, 23, 42, 0.12) !important;
    }
    div[data-testid="stPopover"] button *,
    button[data-testid="stPopoverButton"] *,
    button[data-testid="stPopoverButton"] p,
    button[data-testid="stPopoverButton"] span,
    button[data-testid="stPopoverButton"] div,
    button[data-testid="stPopoverButton"] svg {
        font-weight: 800 !important;
        font-size: 0.76rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* UNIFIED EXECUTIVE MIDNIGHT SLATE & PLATINUM ICE COLOR FOR ALL 4 POPOVER FILTER HEADING CARDS */
    div[data-testid="column"] div[data-testid="stPopover"] button,
    div[data-testid="column"] button[data-testid="stPopoverButton"],
    div[data-testid="stColumn"] div[data-testid="stPopover"] button,
    div[data-testid="stColumn"] button[data-testid="stPopoverButton"],
    div[data-testid="column"] button,
    div[data-testid="stColumn"] button,
    button[data-testid="stPopoverButton"] {
        background: 
            radial-gradient(circle at 100% 0%, rgba(255, 255, 255, 0.8) 0%, transparent 60%),
            linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%) !important;
        background-color: #E2E8F0 !important;
        border: 1.5px solid #CBD5E1 !important;
        border-top: 3.5px solid #1E293B !important;
        color: #0F172A !important;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.08) !important;
    }
    div[data-testid="column"] div[data-testid="stPopover"] button *,
    div[data-testid="column"] button[data-testid="stPopoverButton"] *,
    div[data-testid="stColumn"] div[data-testid="stPopover"] button *,
    div[data-testid="stColumn"] button[data-testid="stPopoverButton"] *,
    div[data-testid="column"] button *,
    div[data-testid="stColumn"] button *,
    button[data-testid="stPopoverButton"] * {
        color: #0F172A !important;
        fill: #0F172A !important;
        font-weight: 850 !important;
    }

    /* POPOVER BODY CONTAINER - FIT ALL TEXT CLEANLY INSIDE WHITE CARD */
    div[data-testid="stPopoverBody"] {
        background: #FFFFFF !important;
        border: 2px solid #5E2D91 !important;
        border-top: 3.5px solid #7B4BB3 !important;
        border-radius: 11px !important;
        box-shadow: 0 12px 30px rgba(94, 45, 145, 0.25) !important;
        padding: 0.5rem 0.75rem 1.1rem 0.75rem !important;
        overflow: visible !important;
    }

    /* REDUCE VERTICAL SPACING & MARGINS INSIDE POPOVER */
    div[data-testid="stPopoverBody"] div[data-testid="stVerticalBlock"],
    div[data-testid="stPopoverBody"] div[data-testid="stVerticalBlock"] > div,
    div[data-testid="stPopoverBody"] div[data-testid="stSelectbox"] {
        gap: 0.2rem !important;
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }

    /* REDUCE ALL LABELS & TEXT SIZES INSIDE POPOVER */
    div[data-testid="stPopoverBody"] label,
    div[data-testid="stPopoverBody"] [data-testid="stWidgetLabel"],
    div[data-testid="stPopoverBody"] label p,
    div[data-testid="stPopoverBody"] label span,
    div[data-testid="stPopoverBody"] [data-testid="stWidgetLabel"] p,
    div[data-testid="stPopoverBody"] [data-testid="stWidgetLabel"] span {
        color: #5E2D91 !important;
        font-weight: 800 !important;
        font-size: 0.68rem !important;
        letter-spacing: -0.2px !important;
        margin-bottom: 0.1rem !important;
        line-height: 1.1 !important;
    }

    /* COMPACT ULTRA-SLEEK POPOVER SELECTBOX INPUTS (26px HEIGHT) */
    div[data-testid="stPopoverBody"] div[data-baseweb="select"],
    div[data-testid="stPopoverBody"] div[data-baseweb="select"] > div {
        border-radius: 6px !important;
        border: 1px solid #CBD5E1 !important;
        outline: none !important;
        box-shadow: none !important;
        background: #F8FAFC !important;
        min-height: 26px !important;
        height: 26px !important;
        max-height: 26px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        padding-left: 4px !important;
        padding-right: 4px !important;
    }
    div[data-testid="stPopoverBody"] div[data-baseweb="select"]:focus-within,
    div[data-testid="stPopoverBody"] div[data-baseweb="select"] > div:focus-within {
        border-color: #5E2D91 !important;
        box-shadow: 0 0 0 2px rgba(94, 45, 145, 0.2) !important;
    }
    div[data-testid="stPopoverBody"] div[data-baseweb="select"] *,
    div[data-testid="stPopoverBody"] div[data-baseweb="select"] p,
    div[data-testid="stPopoverBody"] div[data-baseweb="select"] span,
    div[data-testid="stPopoverBody"] div[data-baseweb="select"] div,
    div[data-testid="stPopoverBody"] div[data-baseweb="select"] input {
        font-size: 0.70rem !important;
        font-weight: 700 !important;
        line-height: 1.1 !important;
        outline: none !important;
        border-color: transparent !important;
    }

    /* REDUCE DROPDOWN OPTION ITEMS */
    div[data-baseweb="menu"] ul,
    div[data-baseweb="menu"] ul li,
    div[data-baseweb="menu"] ul li * {
        font-size: 0.70rem !important;
        padding: 2px 6px !important;
        min-height: 24px !important;
        font-weight: 700 !important;
    }

    /* PERIOD CHIP - CLEAN NEUTRAL IMPERIAL PURPLE TEXT INSIDE POPOVER BOX WITH NO OUTSIDE BLEED OR BLUE BOX */
    .period-chip {
        display: block !important;
        font-size: 0.72rem !important;
        font-weight: 750 !important;
        color: #5E2D91 !important;
        background: transparent !important;
        border: none !important;
        padding: 4px 0px 2px 0px !important;
        margin-top: 6px !important;
        margin-bottom: 2px !important;
        white-space: nowrap !important;
    }

    /* 5 ARTISTIC EXECUTIVE GLASS & SHIMMER KPI CARDS (67% Proportional Scale) */
    .metric-card-exec {
        border-radius: 14px !important;
        padding: 1.1rem 1.0rem 1.0rem 1.1rem !important;
        text-align: left !important;
        position: relative !important;
        overflow: hidden !important;
        transition: transform 0.32s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.32s ease, border-color 0.32s ease !important;
        backdrop-filter: blur(16px) !important;
    }
    .metric-card-exec::before {
        content: '';
        position: absolute;
        top: -20px;
        right: -20px;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.7) 0%, rgba(255, 255, 255, 0.1) 50%, transparent 75%);
        pointer-events: none;
    }
    .metric-card-exec::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.35) 0%, transparent 60%);
        pointer-events: none;
    }

    /* 🔵 Card 1: Headcount (67% Scale) */
    .kpi-emerald {
        background: linear-gradient(135deg, #FFFFFF 35%, #E0F2FE 80%, #BAE6FD 100%) !important;
        border: 1.5px solid #7DD3FC !important;
        border-top: 4px solid #0284C7 !important;
        box-shadow: 0 6px 18px rgba(2, 132, 199, 0.1), inset 0 1px 1px rgba(255, 255, 255, 0.9) !important;
    }
    .metric-val-emerald { font-size: 2.15rem !important; font-weight: 900 !important; color: #0284C7 !important; line-height: 1.05 !important; }
    .badge-bg-emerald { background: rgba(224, 242, 254, 0.9) !important; color: #0284C7 !important; border: 1px solid #7DD3FC !important; font-weight: 850 !important; }

    /* 🟢 Card 2: Active JDA (67% Scale) */
    .kpi-orange {
        background: linear-gradient(135deg, #FFFFFF 35%, #D1FAE5 80%, #A7F3D0 100%) !important;
        border: 1.5px solid #6EE7B7 !important;
        border-top: 4px solid #059669 !important;
        box-shadow: 0 6px 18px rgba(5, 150, 105, 0.1), inset 0 1px 1px rgba(255, 255, 255, 0.9) !important;
    }
    .metric-val-orange { font-size: 2.15rem !important; font-weight: 900 !important; color: #059669 !important; line-height: 1.05 !important; }
    .badge-bg-orange { background: rgba(209, 250, 229, 0.9) !important; color: #059669 !important; border: 1px solid #6EE7B7 !important; font-weight: 850 !important; }

    /* 🟠 Card 3: Active ME (67% Scale) */
    .kpi-blue {
        background: linear-gradient(135deg, #FFFFFF 35%, #FEF3C7 80%, #FDE68A 100%) !important;
        border: 1.5px solid #FCD34D !important;
        border-top: 4px solid #D97706 !important;
        box-shadow: 0 6px 18px rgba(217, 119, 6, 0.1), inset 0 1px 1px rgba(255, 255, 255, 0.9) !important;
    }
    .metric-val-blue { font-size: 2.15rem !important; font-weight: 900 !important; color: #D97706 !important; line-height: 1.05 !important; }
    .badge-bg-blue { background: rgba(254, 243, 199, 0.9) !important; color: #D97706 !important; border: 1px solid #FCD34D !important; font-weight: 850 !important; }

    /* 🟣 Card 4: Active TME / Exited (67% Scale) */
    .kpi-rose {
        background: linear-gradient(135deg, #FFFFFF 35%, #F3E8FF 80%, #E9D5FF 100%) !important;
        border: 1.5px solid #C084FC !important;
        border-top: 4px solid #7E22CE !important;
        box-shadow: 0 6px 18px rgba(126, 34, 206, 0.1), inset 0 1px 1px rgba(255, 255, 255, 0.9) !important;
    }
    .kpi-rose:hover {
        transform: translateY(-4px) scale(1.015) !important;
        box-shadow: 0 12px 28px rgba(126, 34, 206, 0.22) !important;
    }
    .metric-val-rose { font-size: 2.15rem !important; font-weight: 900 !important; color: #7E22CE !important; line-height: 1.05 !important; }
    .badge-bg-rose { background: rgba(243, 232, 255, 0.9) !important; color: #7E22CE !important; border: 1px solid #C084FC !important; font-weight: 850 !important; }

    /* 🌸 Card 5: MoM % Change / QtQ Growth (Artistic Rose Quartz Persona) */
    .kpi-cyan {
        background: linear-gradient(135deg, #FFFFFF 35%, #FCE7F3 80%, #FBCFE8 100%) !important;
        border: 1.5px solid #F472B6 !important;
        border-top: 4px solid #DB2777 !important;
        box-shadow: 0 6px 18px rgba(219, 39, 119, 0.1), inset 0 1px 1px rgba(255, 255, 255, 0.9) !important;
    }
    .kpi-cyan:hover {
        transform: translateY(-4px) scale(1.015) !important;
        box-shadow: 0 12px 28px rgba(219, 39, 119, 0.22) !important;
    }
    .metric-val-cyan { font-size: 2.15rem !important; font-weight: 900 !important; color: #DB2777 !important; line-height: 1.05 !important; }
    .badge-bg-cyan { background: rgba(252, 231, 243, 0.9) !important; color: #DB2777 !important; border: 1px solid #F472B6 !important; font-weight: 850 !important; }

    .metric-lbl-exec {
        font-size: 0.82rem !important;
        color: #475569 !important;
        font-weight: 850 !important;
        margin-top: 4px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.4px !important;
    }
    .metric-badge-exec {
        display: inline-block !important;
        font-size: 0.72rem !important;
        font-weight: 800 !important;
        padding: 3px 10px !important;
        border-radius: 10px !important;
        margin-top: 6px !important;
    }

    /* Executive Tables (67% Scale) */
    .custom-table-card {
        background: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 1.0rem !important;
        border: 1.5px solid #CBD5E1 !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04) !important;
        margin-bottom: 1.5rem !important;
        overflow-x: auto !important;
    }
    .custom-table {
        width: 100% !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        border-radius: 9px !important;
        overflow: hidden !important;
        font-size: 0.88rem !important;
    }
    .custom-table th {
        background: linear-gradient(90deg, #5E2D91 0%, #0F172A 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        padding: 10px 14px !important;
        text-align: center !important;
        border-bottom: 2px solid #38BDF8 !important;
        font-size: 0.88rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.4px !important;
    }
    .custom-table td {
        padding: 9px 14px !important;
        text-align: center !important;
        border-bottom: 1px solid #E2E8F0 !important;
        color: #0F172A !important;
        font-weight: 750 !important;
        font-size: 0.88rem !important;
    }
    .custom-table tr.total-row td {
        background-color: #E0F2FE !important;
        color: #0369A1 !important;
        font-weight: 850 !important;
        font-size: 0.92rem !important;
        border-top: 2px solid #0284C7 !important;
    }

        border-top: 4px solid #0F172A;
        border-radius: 20px;
        padding: 2.0rem 2.6rem;
        margin-top: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
    }
    .export-title {
        font-size: 1.5rem;
        font-weight: 850;
        color: #0F172A;
        margin-bottom: 0.4rem;
    }

    /* Streamlit Download Buttons */
    div[data-testid="stDownloadButton"] button {
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06) !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: #F8FAFC !important;
        color: #0284C7 !important;
        border-color: #0284C7 !important;
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

    /* DYNAMIC SMOOTH SLIDING TRANSITION ANIMATIONS FOR PARENT TABS & CHILD FILTERS */
    @keyframes tabSlideInFromRight {
        0% {
            opacity: 0;
            transform: translateX(32px) scale(0.98);
        }
        100% {
            opacity: 1;
            transform: translateX(0) scale(1.0);
        }
    }

    @keyframes childFilterSlideIn {
        0% {
            opacity: 0;
            transform: translateY(-8px) scale(0.96);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1.0);
        }
    }

    /* Apply smooth slide-in animation to tab panel content on parent tab change */
    div[data-testid="stTabContent"] {
        animation: tabSlideInFromRight 0.38s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
        will-change: transform, opacity !important;
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
        transition: margin-left 0.45s cubic-bezier(0.34, 1.56, 0.64, 1), transform 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        animation: childFilterSlideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
    }

    /* Child Filter Segmented Bar Container (Dynamic centering transition) */
    div[data-testid="stRadio"] {
        margin-left: 0px;
        transition: margin-left 0.45s cubic-bezier(0.34, 1.56, 0.64, 1), transform 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    /* UNSELECTED PARENT TAB BUTTONS (REFINED EXECUTIVE COMPACT SCALE: 1.05rem FONT) */
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
        border: 2px solid #D8B4FE !important;
        border-radius: 10px !important;
        padding: 8px 18px !important;
        min-height: 38px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        cursor: pointer !important;
        box-shadow: 0 4px 12px rgba(94, 45, 145, 0.08) !important;
        transition: transform 0.32s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease !important;
    }

    /* ALL PARENT TAB TEXT (REFINED 1.05rem FONT) */
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
        font-size: 1.05rem !important;
        font-weight: 850 !important;
        color: #5E2D91 !important;
        fill: #5E2D91 !important;
        background: transparent !important;
        white-space: nowrap !important;
        line-height: 1.2 !important;
        opacity: 1.0 !important;
    }

    /* PARENT TAB HOVER STATE (LIGHT AMETHYST TINT) */
    .stTabs button[role="tab"]:hover,
    div[data-testid="stTabs"] button[role="tab"]:hover {
        background: #F3E8FF !important;
        background-color: #F3E8FF !important;
        border-color: #5E2D91 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(94, 45, 145, 0.15) !important;
    }
    .stTabs button[role="tab"]:hover *,
    div[data-testid="stTabs"] button[role="tab"]:hover * {
        color: #4A1E7A !important;
    }

    /* ACTIVE PARENT TAB BUTTON (SOLID ROYAL PURPLE #5E2D91 BACKGROUND - REFINED SCALE: 1.05rem) */
    .stTabs button[aria-selected="true"],
    .stTabs [data-baseweb="tab"][aria-selected="true"],
    .stTabs [data-testid="stTab"][aria-selected="true"],
    div[data-testid="stTabs"] button[aria-selected="true"],
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
    div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"],
    div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] {
        background: #5E2D91 !important;
        background-color: #5E2D91 !important;
        border: 2px solid #5E2D91 !important;
        border-radius: 10px !important;
        box-shadow: 0 6px 20px rgba(94, 45, 145, 0.38) !important;
    }

    /* ACTIVE PARENT TAB TEXT (CRISP SOLID WHITE #FFFFFF - REFINED 1.05rem FONT) */
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
        font-size: 1.05rem !important;
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

    /* HIDE RADIO DOT INDICATOR GRAPHICS COMPLETELY FOR CLEAN ELEGANT PILLS */
    div[data-testid="stRadio"] label input,
    div[data-testid="stRadio"] label svg,
    div[data-testid="stRadio"] label > div:first-child:not([data-testid="stMarkdownContainer"]),
    .stTabs div[data-testid="stRadio"] label input,
    .stTabs div[data-testid="stRadio"] label svg,
    .stTabs div[data-testid="stRadio"] label > div:first-child:not([data-testid="stMarkdownContainer"]),
    .custom-radio-dot {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
        height: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
        opacity: 0 !important;
        position: absolute !important;
        pointer-events: none !important;
    }

    /* ALWAYS FORCE TEXT MARKDOWN CONTAINERS & INNER NODES TO BE FULLY VISIBLE & SHOWN */
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"],
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] *,
    .stTabs div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"],
    .stTabs div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] * {
        background: transparent !important;
        background-color: transparent !important;
        display: inline-block !important;
        visibility: visible !important;
        opacity: 1.0 !important;
        box-shadow: none !important;
    }

    /* CHILD FILTER SEGMENTED BAR CONTAINER (REFINED COMPACT PURPLE TRACK) */
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 4px !important;
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        background: #5E2D91 !important;
        padding: 3px 4px !important;
        border-radius: 9px !important;
        border: 1.5px solid #4A1E7A !important;
        margin-top: 4px !important;
        margin-bottom: 4px !important;
        width: fit-content !important;
        box-shadow: 0 2px 8px rgba(94, 45, 145, 0.22) !important;
    }

    /* UNSELECTED CHILD FILTER OPTIONS (REFINED ULTRA-COMPACT 0.78rem FONT) */
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label {
        font-size: 0.78rem !important;
        font-weight: 800 !important;
        color: rgba(255, 255, 255, 0.95) !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 5.5px !important;
        padding: 4px 11px !important;
        opacity: 0.95 !important;
        box-shadow: none !important;
        transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.28s ease, color 0.28s ease, box-shadow 0.28s ease !important;
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
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 0.78rem !important;
        font-weight: 800 !important;
        white-space: nowrap !important;
        display: inline !important;
        transition: color 0.28s ease !important;
    }
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        opacity: 1.0 !important;
        background: rgba(255, 255, 255, 0.2) !important;
        border-radius: 5.5px !important;
        transform: translateY(-1px) !important;
    }

    /* ACTIVE SELECTED CHILD FILTER OPTION (SOLID WHITE PILL WITH PURPLE TEXT - 0.78rem FONT) */
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: #5E2D91 !important;
        font-weight: 850 !important;
        opacity: 1.0 !important;
        border-radius: 5.5px !important;
        padding: 4px 11px !important;
        border: 1px solid #FFFFFF !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.18) !important;
        transform: translateY(-1px) scale(1.02) !important;
        transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.28s ease, color 0.28s ease, box-shadow 0.28s ease !important;
    }
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p,
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) span,
    .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) div {
        color: #5E2D91 !important;
        fill: #5E2D91 !important;
        background: transparent !important;
        font-size: 0.78rem !important;
        font-weight: 850 !important;
    }

    /* ========================================================= */
    /* COMPREHENSIVE MOBILE & TABLET RESPONSIVE SYSTEM           */
    /* ========================================================= */

    /* TABLETS & SMALL LAPTOPS (< 1024px) */
    @media only screen and (max-width: 1024px) {
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }
        .command-hero-header {
            padding: 2.2rem 2.5rem !important;
        }
        .command-title {
            font-size: 2.6rem !important;
        }
    }

    /* MOBILE PHONES (< 768px - iPhone Pro / Samsung Galaxy / Pixel) */
    @media only screen and (max-width: 768px) {
        /* Main Container Padding */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            max-width: 100% !important;
        }

        /* Hero Header Banner */
        .command-hero-header {
            padding: 1.6rem 1.4rem !important;
            border-radius: 18px !important;
        }
        .command-title {
            font-size: 1.8rem !important;
            line-height: 1.25 !important;
            text-align: center !important;
        }

        /* Main Navigation Tabs */
        div[data-testid="stTabs"] [role="tablist"] {
            gap: 6px !important;
            justify-content: center !important;
            flex-wrap: wrap !important;
            width: 100% !important;
        }
        div[data-testid="stTabs"] button[role="tab"] {
            font-size: 0.85rem !important;
            padding: 8px 12px !important;
            flex-grow: 1 !important;
            text-align: center !important;
            border-radius: 10px !important;
        }

        /* Child Filter Segmented Control Bar */
        .stTabs div[data-testid="stRadio"] div[role="radiogroup"] {
            width: 100% !important;
            max-width: 100% !important;
            justify-content: center !important;
            gap: 4px !important;
            padding: 6px !important;
            border-radius: 14px !important;
            margin-left: 0 !important;
        }
        .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label {
            padding: 6px 10px !important;
            font-size: 0.82rem !important;
            flex-grow: 1 !important;
            text-align: center !important;
            white-space: normal !important;
        }
        .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label p,
        .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label span {
            font-size: 0.82rem !important;
            text-align: center !important;
        }

        /* Metric KPI Cards Layout */
        div[data-testid="stMetricValue"],
        div[data-testid="metric-container"] {
            font-size: 1.5rem !important;
        }

        /* Popover Filter Buttons Grid */
        div[data-testid="stPopover"] {
            width: 100% !important;
        }
        div[data-testid="stPopover"] > button {
            width: 100% !important;
            font-size: 0.85rem !important;
            padding: 8px 12px !important;
        }

        /* Charts & Figures Height & Fit */
        div[data-testid="stPlotlyChart"] {
            width: 100% !important;
            overflow-x: auto !important;
        }

        /* Tables Horizontal Scroll Safety */
        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {
            width: 100% !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
        }
    }

    /* SMALL MOBILE PHONES (< 480px - iPhone SE / Compact Phones) */
    @media only screen and (max-width: 480px) {
        .command-hero-header {
            padding: 1.2rem 1rem !important;
            border-radius: 14px !important;
        }
        .command-title {
            font-size: 1.45rem !important;
        }
        div[data-testid="stTabs"] button[role="tab"] {
            font-size: 0.8rem !important;
            padding: 6px 8px !important;
        }
        .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label {
            padding: 5px 8px !important;
            font-size: 0.78rem !important;
        }
        .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label p,
        .stTabs div[data-testid="stRadio"] div[role="radiogroup"] label span {
            font-size: 0.78rem !important;
        }
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

# Hero Banner (Enlarged Executive Command Headbar - Left Aligned Title)
st.markdown("""
<div class="command-hero-header" style="padding: 3.2rem 4.0rem; border-radius: 28px; background: linear-gradient(135deg, #4A1E7A 0%, #5E2D91 50%, #3B1663 100%) !important; box-shadow: 0 24px 60px rgba(94, 45, 145, 0.35), inset 0 1.5px 2px rgba(255, 255, 255, 0.35); border: 1.8px solid rgba(255, 255, 255, 0.25);">
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

            // Disable browser native scroll restoration so refresh always starts at the top
            try {
                if (targetDoc.defaultView && 'scrollRestoration' in targetDoc.defaultView.history) {
                    targetDoc.defaultView.history.scrollRestoration = 'manual';
                }
            } catch(e) {}

            // Always clear scroll session state on page refresh / load
            try {
                sessionStorage.removeItem("openPopoverTag");
                sessionStorage.removeItem("isCustomCalendarMode");
                sessionStorage.removeItem("should_autoscroll_to_section");
                sessionStorage.removeItem("user_scrolled_down");
            } catch(err) {}

            function forcePageToTopOnRefresh() {
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

            // Immediately force scroll to top on script load and refresh
            forcePageToTopOnRefresh();
            setTimeout(forcePageToTopOnRefresh, 50);
            setTimeout(forcePageToTopOnRefresh, 150);
            setTimeout(forcePageToTopOnRefresh, 400);

            function alignChildFilterBar() {
                try {
                    // Hide radio circle indicator graphics cleanly for uncluttered modern pill filter bar
                    var radioLabels = targetDoc.querySelectorAll('div[data-testid="stRadio"] label');
                    radioLabels.forEach(function(lbl) {
                        var oldCustomDots = lbl.querySelectorAll('.custom-radio-dot');
                        oldCustomDots.forEach(function(cd) { cd.remove(); });

                        var firstChild = lbl.firstElementChild;
                        if (firstChild && !firstChild.getAttribute('data-testid')?.includes('stMarkdownContainer')) {
                            firstChild.style.setProperty('display', 'none', 'important');
                            firstChild.style.setProperty('visibility', 'hidden', 'important');
                        }
                        
                        var textContainer = lbl.querySelector('div[data-testid="stMarkdownContainer"]');
                        if (textContainer) {
                            textContainer.style.setProperty('display', 'inline-block', 'important');
                            textContainer.style.setProperty('visibility', 'visible', 'important');
                            textContainer.style.setProperty('opacity', '1', 'important');
                        }
                    });

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
                    sessionStorage.removeItem("should_autoscroll_to_section");
                    sessionStorage.removeItem("user_scrolled_down");
                } catch(err) {}
            }
            setInterval(checkAutoScrollToSection, 200);

            function getExpanderIdx(exp) {
                var all = Array.from(targetDoc.querySelectorAll('div[data-testid="stExpander"]'));
                return 'exp_idx_' + all.indexOf(exp);
            }

            if (!targetDoc._hasExpanderPersistListenerP5) {
                targetDoc._hasExpanderPersistListenerP5 = true;

                // FULL 100% KEYBOARD ACCESSIBILITY & NAVIGATION ENGINE
                targetDoc.addEventListener('keydown', function(e) {
                    var activeEl = targetDoc.activeElement;

                    // TIME PERIOD POPOVER KEYBOARD WORKFLOW:
                    // 1. On Time Period Popover Button -> Enter/Space opens Popover Body
                    // 2. Inside Open Popover Body -> ArrowDown moves focus to Time Mode Selection Dropdown
                    // 3. On Time Mode Selection Dropdown -> Enter opens Yearly, Quarterly, MTD, Custom options list!
                    var openPopoverBody = targetDoc.querySelector('div[data-testid="stPopoverBody"]');
                    var isTimePopoverBtn = activeEl && (activeEl.closest('div[data-testid="stPopover"]') || activeEl.closest('button[data-testid="stPopoverButton"]')) && 
                                          (activeEl.innerText && (activeEl.innerText.includes("Time Period") || activeEl.innerText.includes("🗓️") || activeEl.innerText.includes("📅") || activeEl.innerText.includes("Monthly") || activeEl.innerText.includes("Yearly") || activeEl.innerText.includes("Quarterly")));

                    if (isTimePopoverBtn && (e.key === 'Enter' || e.key === ' ')) {
                        setTimeout(function() {
                            var popBody = targetDoc.querySelector('div[data-testid="stPopoverBody"]');
                            if (popBody) {
                                var firstSelectable = popBody.querySelector('div[data-testid="stSelectbox"] div[role="combobox"], div[data-baseweb="select"] input, div[data-baseweb="select"], select, div[data-testid="stRadio"] label');
                                if (firstSelectable) {
                                    firstSelectable.focus();
                                }
                            }
                        }, 150);
                    }

                    if (openPopoverBody) {
                        var isInsidePopoverBody = activeEl && activeEl.closest('div[data-testid="stPopoverBody"]');
                        var isInsideSubList = activeEl && (activeEl.closest('ul[role="listbox"]') || activeEl.closest('div[data-baseweb="menu"]'));

                        // ArrowDown inside Popover Body -> Moves focus down to Time Period Selection Dropdown
                        if (e.key === 'ArrowDown' && isInsidePopoverBody && !isInsideSubList) {
                            var timeModeSelectbox = openPopoverBody.querySelector('div[data-testid="stSelectbox"] div[role="combobox"], div[data-baseweb="select"] input, div[data-baseweb="select"], select, div[data-testid="stRadio"] label:has(input:checked), div[data-testid="stRadio"] label');
                            if (timeModeSelectbox && activeEl !== timeModeSelectbox) {
                                e.preventDefault();
                                timeModeSelectbox.focus();
                                timeModeSelectbox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                            }
                        }

                        // Enter or Space on Time Mode Dropdown -> Opens Sub-Dropdown List of Yearly, Quarterly, MTD
                        if ((e.key === 'Enter' || e.key === ' ') && isInsidePopoverBody) {
                            var isSelectbox = activeEl && (activeEl.closest('div[data-testid="stSelectbox"]') || activeEl.closest('div[data-baseweb="select"]') || activeEl.getAttribute('role') === 'combobox');
                            if (isSelectbox) {
                                var selectClick = activeEl.querySelector('div[role="combobox"], input') || activeEl;
                                selectClick.click();
                            }
                        }
                    }

                    // ESCAPE KEY: Close all open popover bodies cleanly
                    if (e.key === 'Escape') {
                        var activePopovers = targetDoc.querySelectorAll('div[data-testid="stPopoverBody"]');
                        if (activePopovers.length > 0) {
                            e.preventDefault();
                            sessionStorage.removeItem("openPopoverTag");
                            sessionStorage.removeItem("isCustomCalendarMode");
                            targetDoc.body.click();
                            activePopovers.forEach(function(pb) { pb.style.display = 'none'; });
                        }
                    }

                    // ARROW DOWN: Move focus from Parent Tab down to Child Filter
                    if (e.key === 'ArrowDown' && (!openPopoverBody || !activeEl.closest('div[data-testid="stPopoverBody"]'))) {
                        var isParentTab = activeEl && (activeEl.closest('div[data-testid="stTabs"] button') || activeEl.closest('.stTabs button') || activeEl.getAttribute('role') === 'tab');
                        if (isParentTab) {
                            var activeTabContent = targetDoc.querySelector('div[data-testid="stTabContent"]:not([hidden]), div[role="tabpanel"]:not([hidden])');
                            if (activeTabContent) {
                                var targetChildOption = activeTabContent.querySelector('div[data-testid="stRadio"] label:has(input:checked)') || activeTabContent.querySelector('div[data-testid="stRadio"] label');
                                if (targetChildOption) {
                                    e.preventDefault();
                                    targetChildOption.focus();
                                    targetChildOption.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                                }
                            }
                        }
                    } 
                    // ARROW UP: Move focus from Child Filter back up to Parent Tab
                    else if (e.key === 'ArrowUp' && (!openPopoverBody || !activeEl.closest('div[data-testid="stPopoverBody"]'))) {
                        var isChildFilter = activeEl && activeEl.closest('div[data-testid="stRadio"]');
                        if (isChildFilter) {
                            var activeParentTab = targetDoc.querySelector('div[data-testid="stTabs"] button[aria-selected="true"], div[data-testid="stTabs"] [aria-selected="true"]');
                            if (activeParentTab) {
                                e.preventDefault();
                                activeParentTab.focus();
                                activeParentTab.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                            }
                        }
                    }
                    // ARROW LEFT & ARROW RIGHT: Switch tabs or child options seamlessly
                    else if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
                        var isParentTab = activeEl && activeEl.closest('div[data-testid="stTabs"] button, .stTabs button');
                        var isChildFilter = activeEl && activeEl.closest('div[data-testid="stRadio"]');

                        if (isParentTab) {
                            var allParentTabs = Array.from(targetDoc.querySelectorAll('div[data-testid="stTabs"] button, .stTabs button[role="tab"]'));
                            var currIdx = allParentTabs.indexOf(isParentTab);
                            if (currIdx !== -1) {
                                e.preventDefault();
                                var nextIdx = (e.key === 'ArrowRight') ? (currIdx + 1) % allParentTabs.length : (currIdx - 1 + allParentTabs.length) % allParentTabs.length;
                                allParentTabs[nextIdx].focus();
                                allParentTabs[nextIdx].click();
                            }
                        } else if (isChildFilter) {
                            var activeTabContent = targetDoc.querySelector('div[data-testid="stTabContent"]:not([hidden]), div[role="tabpanel"]:not([hidden])');
                            if (activeTabContent) {
                                var allChildOptions = Array.from(activeTabContent.querySelectorAll('div[data-testid="stRadio"] label'));
                                var currChild = activeEl.closest('label');
                                var currChildIdx = allChildOptions.indexOf(currChild);
                                if (currChildIdx !== -1) {
                                    e.preventDefault();
                                    var nextChildIdx = (e.key === 'ArrowRight') ? (currChildIdx + 1) % allChildOptions.length : (currChildIdx - 1 + allChildOptions.length) % allChildOptions.length;
                                    allChildOptions[nextChildIdx].focus();
                                    allChildOptions[nextChildIdx].click();
                                }
                            }
                        }
                    }
                }, true);

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

# Live Active Snapshot Metrics (Irrespective of Time Period chosen)
today_dt = pd.Timestamp(date.today())

if "status_as_of_obs" in raw_df.columns:
    is_active_mask = (raw_df['status_as_of_obs'] == 'Active') | (raw_df['dol'].isna()) | (pd.to_datetime(raw_df['dol'], errors='coerce') >= today_dt)
    is_exited_mask = (raw_df['status_as_of_obs'] == 'Exited')
elif "dol" in raw_df.columns:
    dol_dt = pd.to_datetime(raw_df['dol'], errors='coerce')
    is_active_mask = dol_dt.isna() | (dol_dt >= today_dt)
    is_exited_mask = ~is_active_mask
else:
    is_active_mask = pd.Series(True, index=raw_df.index)
    is_exited_mask = pd.Series(False, index=raw_df.index)

raw_active_df = raw_df[is_active_mask].copy()

if selected_city_single != "All 11 Cities":
    raw_active_df = raw_active_df[raw_active_df['branch'].isin(selected_branches)]
if selected_team_single != "All Teams":
    raw_active_df = raw_active_df[raw_active_df['team_type'].isin(selected_teams)]

active_snapshot_headcount = len(raw_active_df)
active_snapshot_me = len(raw_active_df[raw_active_df['emp_type'].astype(str).str.upper() == 'ME'])
active_snapshot_tme = len(raw_active_df[raw_active_df['emp_type'].astype(str).str.upper() == 'TME'])
active_snapshot_jda = len(raw_active_df[raw_active_df['emp_type'].astype(str).str.upper() == 'JDA'])

exited_df_snap = raw_df[is_exited_mask].copy()
if selected_city_single != "All 11 Cities":
    exited_df_snap = exited_df_snap[exited_df_snap['branch'].isin(selected_branches)]
active_snapshot_exited = len(exited_df_snap)

# ==============================================================================
# TOP EXECUTIVE KPI METRIC CARDS (PERIOD & EMPTYPE SCALED)
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)

time_mode_current = st.session_state.get("hdr_dd_time_mode", "Monthly (MTD)")

if emp_type_option == "All EmpTypes":
    # WHEN ALL EMP TYPES SELECTED: SHOW HEADCOUNT, ACTIVE JDA, ACTIVE ME, ACTIVE TME KPI CARDS!
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
        <div class="metric-badge-exec badge-bg-rose">🟪 Active TME</div>
    </div>
    ''', unsafe_allow_html=True)

elif time_mode_current == "Yearly":
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

    elif time_mode_current == "Custom Calendar":
        # CUSTOM CALENDAR MODE (ANY EMPTYPE): 5 Executive Cards (Headcount, New Joiners, Exited Count, MoM %, YoY %)
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
            <div class="metric-badge-exec badge-bg-orange">✨ New Joiners in Period</div>
        </div>
        ''', unsafe_allow_html=True)

        c3.markdown(f'''
        <div class="metric-card-exec kpi-rose">
            <div class="metric-val-rose">{exited_count}</div>
            <div class="metric-lbl-exec">Exited Count</div>
            <div class="metric-badge-exec badge-bg-rose">🔴 Exited in Period</div>
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
        <div class="metric-card-exec kpi-blue">
            <div class="metric-val-blue">{yoy_str}</div>
            <div class="metric-lbl-exec">YoY % Change</div>
            <div class="metric-badge-exec badge-bg-blue">📈 Year-over-Year</div>
        </div>
        ''', unsafe_allow_html=True)

    elif emp_type_option == "All EmpTypes":
        # ALL EMPTYPES IN MONTHLY MODE: 4 Cards (Headcount, Active JDA, Active ME, Active TME)
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
                html_b.append(f'<td style="font-weight:700; text-align:left; color:#5E2D91;">{r["branch"]}</td>')
                html_b.append(f'<td style="color:#28A745; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html_b.append(f'<td style="color:#E74C3C; font-weight:700;">{r["Exited_Count"]}</td>')
                    html_b.append(f'<td style="color:#7B4BB3; font-weight:800;">{r["New_Joiners_Count"]}</td>')
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
                html_t.append(f'<td style="font-weight:700; text-align:left; color:#5E2D91;">{r["team_type"]}</td>')
                html_t.append(f'<td style="color:#28A745; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html_t.append(f'<td style="color:#E74C3C; font-weight:700;">{r["Exited_Count"]}</td>')
                    html_t.append(f'<td style="color:#7B4BB3; font-weight:800;">{r["New_Joiners_Count"]}</td>')
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
                html_tb.append(f'<td style="font-weight:700; text-align:left; color:#5E2D91;">{r["tenure_bucket"]}</td>')
                html_tb.append(f'<td style="color:#28A745; font-weight:800;">{int(r["Total_Headcount"])}</td>')
                if not is_today:
                    html_tb.append(f'<td style="color:#E74C3C; font-weight:700;">{int(r["Exited_Count"])}</td>')
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
                html_bp.append(f'<td style="font-weight:700; text-align:left; color:#5E2D91;">{r["branch"]}</td>')
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
                html_tp.append(f'<td style="font-weight:700; text-align:left; color:#5E2D91;">{r["team_type"]}</td>')
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
                html3.append(f'<td style="text-align:left; font-weight:700; color:#5E2D91;">{r["branch"]}</td>')
                html3.append(f'<td style="color:#28A745; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html3.append(f'<td style="color:#E74C3C; font-weight:700;">{r["Exited_Count"]}</td>')
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
                html4.append(f'<td style="text-align:left; font-weight:700; color:#5E2D91;">{r["team_type"]}</td>')
                html4.append(f'<td style="color:#28A745; font-weight:800;">{r["Active_Count"]}</td>')
                if not is_today:
                    html4.append(f'<td style="color:#E74C3C; font-weight:700;">{r["Exited_Count"]}</td>')
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

# Vercel Serverless Top-Level Handlers Export
def handler(req=None, res=None):
    return "Workforce Intelligence Executive Dashboard Suite"

app = handler
application = handler
