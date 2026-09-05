import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="House Price Category Predictor", page_icon="🏠", layout="wide")

# =========================================================
# THEME / STYLING
# =========================================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

ACCENT = "#6C5CE7"
ACCENT_2 = "#00CEC9"
GOOD = "#00E5A0"
BAD = "#FF7675"
GOLD = "#FDCB6E"

DARK_MODE = st.session_state.dark_mode
TEXT_COLOR = "#F5F6FA" if DARK_MODE else "#1a1a2e"
MUTED_COLOR = "#B8BDD0" if DARK_MODE else "#5a5f73"
CARD_BG = "rgba(255,255,255,0.06)" if DARK_MODE else "rgba(255,255,255,0.75)"
CARD_BORDER = "rgba(255,255,255,0.12)" if DARK_MODE else "rgba(20,20,43,0.08)"
APP_BG_1 = "#0b0e17" if DARK_MODE else "#eef1fb"
APP_BG_2 = "#151a2b" if DARK_MODE else "#f7f8fd"

BASE_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}
h1, h2, h3, .hero-title {{
    font-family: 'Poppins', sans-serif !important;
}}

/* Animated 3D-ish gradient app background */
.stApp {{
    background:
        radial-gradient(circle at 15% 20%, rgba(108,92,231,0.20), transparent 40%),
        radial-gradient(circle at 85% 15%, rgba(0,206,201,0.16), transparent 42%),
        radial-gradient(circle at 50% 100%, rgba(108,92,231,0.12), transparent 50%),
        linear-gradient(180deg, {APP_BG_1} 0%, {APP_BG_2} 100%);
    background-attachment: fixed;
    color: {TEXT_COLOR};
}}
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {APP_BG_2}, {APP_BG_1});
    border-right: 1px solid {CARD_BORDER};
}}
.stMarkdown, label, p, span {{ color: {TEXT_COLOR}; }}
div[data-testid="stMetricValue"] {{ color: {TEXT_COLOR} !important; }}
div[data-testid="stMetricLabel"] {{ color: {MUTED_COLOR} !important; }}
.stCaption, .st-emotion-cache-1629p8f, small {{ color: {MUTED_COLOR} !important; }}

/* Glass panels: form, dataframe wrappers, expander */
div[data-testid="stForm"], div[data-testid="stExpander"], div[data-testid="stDataFrame"] {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 20px;
    padding: 1.2rem;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.06);
}}

/* 3D hero banner with floating glow orbs */
.hero-banner {{
    position: relative;
    overflow: hidden;
    background: linear-gradient(120deg, {ACCENT} 0%, {ACCENT_2} 100%);
    padding: 2.6rem 2.2rem;
    border-radius: 24px;
    margin-bottom: 1.8rem;
    box-shadow: 0 20px 50px rgba(108, 92, 231, 0.35), inset 0 1px 0 rgba(255,255,255,0.25);
    transform: perspective(900px) rotateX(1.5deg);
}}
.hero-banner::before, .hero-banner::after {{
    content: "";
    position: absolute;
    border-radius: 50%;
    filter: blur(30px);
    opacity: 0.5;
    animation: floaty 7s ease-in-out infinite;
}}
.hero-banner::before {{
    width: 180px; height: 180px;
    background: rgba(255,255,255,0.35);
    top: -60px; right: 10%;
}}
.hero-banner::after {{
    width: 130px; height: 130px;
    background: rgba(255,255,255,0.25);
    bottom: -50px; left: 15%;
    animation-delay: 2s;
}}
@keyframes floaty {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-14px); }}
}}
.hero-title {{
    position: relative;
    color: white;
    font-size: 2.3rem;
    font-weight: 800;
    margin: 0;
    text-shadow: 0 4px 18px rgba(0,0,0,0.25);
}}
.hero-sub {{
    position: relative;
    color: rgba(255,255,255,0.95);
    font-size: 1.04rem;
    margin-top: 0.5rem;
    font-weight: 400;
}}
.hero-badges {{ position: relative; }}
.hero-badges span {{
    display: inline-block;
    background: rgba(255,255,255,0.2);
    color: white;
    padding: 0.3rem 0.85rem;
    border-radius: 999px;
    font-size: 0.8rem;
    margin-right: 0.5rem;
    margin-top: 1rem;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.3);
    backdrop-filter: blur(4px);
}}

/* 3D tilt cards */
.card3d {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 20px;
    padding: 1.5rem 1.6rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.06);
    margin-bottom: 1.2rem;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    transform-style: preserve-3d;
}}
.card3d:hover {{
    transform: perspective(800px) rotateX(2deg) rotateY(-2deg) translateY(-4px);
    box-shadow: 0 22px 45px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.1);
}}

/* Tabs styling */
button[data-baseweb="tab"] {{
    font-weight: 600;
    border-radius: 12px 12px 0 0 !important;
}}
div[data-baseweb="tab-highlight"] {{
    background-color: {ACCENT} !important;
    height: 3px !important;
}}

/* Buttons — 3D press effect */
div.stButton > button, button[kind="primary"], button[kind="secondary"] {{
    border-radius: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.2px;
    transition: transform 0.12s ease, box-shadow 0.12s ease;
    border: 1px solid {CARD_BORDER} !important;
}}
div.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 22px rgba(108, 92, 231, 0.35);
}}
div.stButton > button:active, button[kind="primary"]:active {{
    transform: translateY(1px) scale(0.98);
}}
button[kind="primary"] {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT_2}) !important;
    border: none !important;
    box-shadow: 0 8px 24px rgba(108, 92, 231, 0.4), inset 0 1px 0 rgba(255,255,255,0.3) !important;
}}
div[data-testid="stDownloadButton"] > button {{
    background: linear-gradient(135deg, {GOLD}, {BAD}) !important;
    color: #241a00 !important;
    border: none !important;
    box-shadow: 0 8px 22px rgba(253, 203, 110, 0.35) !important;
}}

/* Result banner — glowing glass */
.result-banner {{
    position: relative;
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0.8rem 0 1.2rem 0;
    animation: fadeIn 0.45s ease-in;
    backdrop-filter: blur(14px);
    box-shadow: 0 14px 34px rgba(0,0,0,0.22);
}}
.result-expensive {{
    background: linear-gradient(120deg, rgba(255,118,117,0.28), rgba(253,203,110,0.20));
    border: 1px solid rgba(255,118,117,0.4);
}}
.result-affordable {{
    background: linear-gradient(120deg, rgba(0,206,201,0.24), rgba(0,229,160,0.20));
    border: 1px solid rgba(0,229,160,0.4);
}}
.result-label {{
    font-size: 1.7rem;
    font-weight: 800;
    font-family: 'Poppins', sans-serif;
    color: {TEXT_COLOR};
}}
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Section headers */
.section-title {{
    font-weight: 700;
    font-size: 1.2rem;
    margin-top: 0.2rem;
    margin-bottom: 0.7rem;
    font-family: 'Poppins', sans-serif;
    color: {TEXT_COLOR};
}}

footer {{visibility: hidden;}}
</style>
"""

st.markdown(BASE_CSS, unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_artifacts():
    model = joblib.load(os.path.join(BASE_DIR, "house_price_model.pkl"))
    meta = joblib.load(os.path.join(BASE_DIR, "model_metadata.pkl"))
    return model, meta

model, meta = load_artifacts()
num_feats = meta["numeric_features"]
cat_feats = meta["categorical_features"]
cat_options = meta["categorical_options"]
num_ranges = meta["numeric_ranges"]
median_price = meta["median_price"]
test_acc = meta["test_accuracy"]

if "history" not in st.session_state:
    st.session_state.history = []
if "reset_flag" not in st.session_state:
    st.session_state.reset_flag = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🏠 House Price AI")
    st.caption("Ames Housing · Random Forest Classifier")
    st.markdown("---")

    c1, c2 = st.columns(2)
    c1.metric("Accuracy", f"{test_acc*100:.1f}%")
    c2.metric("Median Price", f"${median_price/1000:.0f}K")

    st.markdown("---")
    st.markdown("**How it works**")
    st.markdown(
        """
        1. Enter property details
        2. Hit **Predict**
        3. Get an instant category + confidence
        4. Track & download results in **History**
        """
    )
    st.markdown("---")
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    
    

# =========================================================
# HERO HEADER
# =========================================================
st.markdown(
    f"""
    <div class="hero-banner">
        <div class="hero-title">🏠 House Price Category Predictor</div>
        <div class="hero-sub">AI-powered classification of homes as <b>Expensive</b> or <b>Affordable</b>, trained on the Ames Housing dataset.</div>
        <div class="hero-badges">
            <span>🌲 Random Forest</span>
            <span>🎯 {test_acc*100:.1f}% Accuracy</span>
            <span>⚡ Real-time Inference</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_predict, tab_insights, tab_history = st.tabs(["🔮 Predict", "📊 Model Insights", "📜 History"])

# =========================================================
# TAB 1 — PREDICT
# =========================================================
with tab_predict:
    st.markdown('<div class="section-title">Property Details</div>', unsafe_allow_html=True)
    suffix = st.session_state.reset_flag

    with st.form(key=f"predict_form_{suffix}"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🏗️ Structure**")
            overall_qual = st.slider("Overall Quality (1=Poor, 10=Excellent)", 1, 10, int(num_ranges["OverallQual"][2]))
            gr_liv_area = st.number_input("Above Ground Living Area (sq ft)", min_value=0, value=int(num_ranges["GrLivArea"][2]))
            total_bsmt_sf = st.number_input("Total Basement Area (sq ft)", min_value=0, value=int(num_ranges["TotalBsmtSF"][2]))
            lot_area = st.number_input("Lot Area (sq ft)", min_value=0, value=int(num_ranges["LotArea"][2]))
            garage_cars = st.number_input("Garage Capacity (cars)", min_value=0, max_value=6, value=int(num_ranges["GarageCars"][2]))

        with col2:
            st.markdown("**✨ Features**")
            full_bath = st.number_input("Full Bathrooms", min_value=0, max_value=6, value=int(num_ranges["FullBath"][2]))
            fireplaces = st.number_input("Fireplaces", min_value=0, max_value=5, value=int(num_ranges["Fireplaces"][2]))
            year_built = st.number_input("Year Built", min_value=1800, max_value=2026, value=int(num_ranges["YearBuilt"][2]))
            year_remod = st.number_input("Year Remodeled/Added", min_value=1800, max_value=2026, value=int(num_ranges["YearRemodAdd"][2]))
            neighborhood = st.selectbox("Neighborhood", cat_options["Neighborhood"])

        st.markdown("**🎨 Style & Quality**")
        col3, col4, col5 = st.columns(3)
        with col3:
            house_style = st.selectbox("House Style", cat_options["HouseStyle"])
        with col4:
            exter_qual = st.selectbox("Exterior Quality", cat_options["ExterQual"])
        with col5:
            kitchen_qual = st.selectbox("Kitchen Quality", cat_options["KitchenQual"])

        st.write("")
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            submitted = st.form_submit_button("🔮 Predict", use_container_width=True, type="primary")
        with col_btn2:
            reset_clicked = st.form_submit_button("🔄 Reset", use_container_width=True)

    if reset_clicked:
        st.session_state.reset_flag += 1
        st.session_state.last_result = None
        st.rerun()

    if submitted:
        errors = []
        if year_remod < year_built:
            errors.append("Year Remodeled cannot be earlier than Year Built.")
        if gr_liv_area <= 0:
            errors.append("Living area must be greater than 0.")
        if lot_area <= 0:
            errors.append("Lot area must be greater than 0.")

        if errors:
            for e in errors:
                st.error(f"⚠️ {e}")
        else:
            input_df = pd.DataFrame([{
                "OverallQual": overall_qual,
                "GrLivArea": gr_liv_area,
                "GarageCars": garage_cars,
                "TotalBsmtSF": total_bsmt_sf,
                "FullBath": full_bath,
                "YearBuilt": year_built,
                "YearRemodAdd": year_remod,
                "LotArea": lot_area,
                "Fireplaces": fireplaces,
                "Neighborhood": neighborhood,
                "HouseStyle": house_style,
                "ExterQual": exter_qual,
                "KitchenQual": kitchen_qual,
            }])

            try:
                pred = model.predict(input_df)[0]
                proba = model.predict_proba(input_df)[0]
                confidence = proba[pred] * 100
                st.session_state.last_result = {
                    "pred": int(pred),
                    "confidence": confidence,
                    "inputs": input_df.iloc[0].to_dict(),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.session_state.history.append({
                    "Time": datetime.now().strftime("%H:%M:%S"),
                    "Neighborhood": neighborhood,
                    "OverallQual": overall_qual,
                    "GrLivArea": gr_liv_area,
                    "Prediction": "Expensive" if pred == 1 else "Affordable",
                    "Confidence": f"{confidence:.1f}%"
                })
            except Exception as e:
                st.error(f"⚠️ Something went wrong while predicting: {e}")

    result = st.session_state.last_result
    if result:
        pred = result["pred"]
        confidence = result["confidence"]
        css_class = "result-expensive" if pred == 1 else "result-affordable"
        label = "💰 Expensive" if pred == 1 else "🏡 Affordable"
        color = BAD if pred == 1 else GOOD

        st.markdown(
            f"""
            <div class="result-banner {css_class}">
                <div class="result-label">{label}</div>
                <div style="text-align:right;">
                    <div style="font-size:0.85rem; opacity:0.8; color:{TEXT_COLOR}; font-weight:600; letter-spacing:0.5px;">CONFIDENCE</div>
                    <div style="font-size:1.8rem; font-weight:900; color:{color}; text-shadow: 0 2px 10px rgba(0,0,0,0.25);">{confidence:.1f}%</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Gauge — explicit high-contrast colors so the number is always readable
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            number={"suffix": "%", "font": {"size": 46, "color": TEXT_COLOR}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": MUTED_COLOR,
                         "tickfont": {"color": MUTED_COLOR, "size": 12}},
                "bar": {"color": color, "thickness": 0.28},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 50], "color": "rgba(255,118,117,0.18)"},
                    {"range": [50, 80], "color": "rgba(253,203,110,0.20)"},
                    {"range": [80, 100], "color": "rgba(0,229,160,0.20)"},
                ],
            },
        ))
        gauge.update_layout(
            height=240, margin=dict(l=30, r=30, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": TEXT_COLOR},
        )
        st.plotly_chart(gauge, use_container_width=True)

        # Quick single-prediction download, right under the score
        quick_df = pd.DataFrame([{
            **result["inputs"],
            "Prediction": "Expensive" if pred == 1 else "Affordable",
            "Confidence (%)": round(confidence, 1),
            "Timestamp": result["timestamp"],
        }])
        st.download_button(
            "⬇️ Download This Prediction (CSV)",
            data=quick_df.to_csv(index=False).encode("utf-8"),
            file_name="house_prediction.csv",
            mime="text/csv",
            use_container_width=True,
        )

        if confidence >= 90:
            st.balloons()

# =========================================================
# TAB 2 — MODEL INSIGHTS
# =========================================================
with tab_insights:
    st.markdown('<div class="section-title">What drives this model\'s predictions?</div>', unsafe_allow_html=True)
    try:
        rf = model.named_steps["classifier"]
        ohe = model.named_steps["preprocessor"].named_transformers_["cat"].named_steps["onehot"]
        cat_names = list(ohe.get_feature_names_out(cat_feats))
        all_names = num_feats + cat_names
        importances = pd.Series(rf.feature_importances_, index=all_names)

        grouped = {}
        for name, val in importances.items():
            parent = name
            for cf in cat_feats:
                if name.startswith(cf + "_"):
                    parent = cf
                    break
            grouped[parent] = grouped.get(parent, 0) + val

        chart_df = pd.DataFrame({"Feature": list(grouped.keys()), "Importance": list(grouped.values())})
        chart_df = chart_df.sort_values("Importance", ascending=True)

        fig = px.bar(
            chart_df, x="Importance", y="Feature", orientation="h",
            color="Importance", color_continuous_scale=[ACCENT_2, ACCENT],
        )
        fig.update_layout(
            height=420, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False, font={"color": TEXT_COLOR},
            xaxis=dict(gridcolor="rgba(128,128,128,0.15)"),
            yaxis=dict(gridcolor="rgba(128,128,128,0.15)"),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Relative importance of each feature in the trained Random Forest — higher bars mean the feature has more influence on the Expensive/Affordable prediction.")
    except Exception:
        st.info("Feature importance chart unavailable.")

    st.markdown('<div class="section-title">Model Summary</div>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Algorithm", "Random Forest")
    m2.metric("Trees", f"{model.named_steps['classifier'].n_estimators}")
    m3.metric("Test Accuracy", f"{test_acc*100:.1f}%")

# =========================================================
# TAB 3 — HISTORY
# =========================================================
with tab_history:
    if not st.session_state.history:
        st.info("No predictions yet — head to the **Predict** tab to get started.")
    else:
        hist_df = pd.DataFrame(st.session_state.history)

        h1, h2, h3 = st.columns(3)
        h1.metric("Total Predictions", len(hist_df))
        h2.metric("Expensive", int((hist_df["Prediction"] == "Expensive").sum()))
        h3.metric("Affordable", int((hist_df["Prediction"] == "Affordable").sum()))

        st.markdown('<div class="section-title">Prediction Log</div>', unsafe_allow_html=True)
        st.dataframe(hist_df, use_container_width=True, hide_index=True)

        csv = hist_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Full History (CSV)", data=csv, file_name="prediction_history.csv", mime="text/csv", use_container_width=True)

        if len(hist_df) > 1:
            st.markdown('<div class="section-title">Confidence Trend</div>', unsafe_allow_html=True)
            conf_series = hist_df["Confidence"].str.rstrip("%").astype(float)
            trend_fig = px.line(
                x=hist_df["Time"], y=conf_series, markers=True,
                labels={"x": "Time", "y": "Confidence %"},
            )
            trend_fig.update_traces(line_color=ACCENT, marker=dict(size=9, color=ACCENT_2))
            trend_fig.update_layout(
                height=320, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font={"color": TEXT_COLOR},
                xaxis=dict(gridcolor="rgba(128,128,128,0.15)"),
                yaxis=dict(gridcolor="rgba(128,128,128,0.15)"),
            )
            st.plotly_chart(trend_fig, use_container_width=True)

        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
