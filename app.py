import streamlit as st
import numpy as np
import pandas as pd
import joblib

# -----------------------------
# Load the trained XGBoost model
# -----------------------------
@st.cache_resource
def load_model():
    return joblib.load("tuned_xgboost_instagram_model.pkl")

model = load_model()

# -----------------------------
# Config & Feature Columns
# -----------------------------
st.set_page_config(page_title="Instagram Impressions Predictor", layout="centered")

FEATURE_COLUMNS = [
    'Saves', 'Comments', 'Shares', 'Likes',
    'Profile Visits', 'Follows', 'Hashtag Count',
    'Caption Length', 'Engagement Rate'
]

st.title("📊 Instagram Impressions Predictor")
st.write("Predict how many *impressions* your Instagram post might get based on engagement data.")

st.markdown("---")

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.header("Navigation")
mode = st.sidebar.radio("Choose Mode:", ["Single Prediction", "Batch Prediction (CSV Upload)"])

# -----------------------------
# Single Prediction Mode
# -----------------------------
if mode == "Single Prediction":
    st.subheader("Enter Post Engagement Details")

    saves = st.number_input("Saves", min_value=0, step=1)
    comments = st.number_input("Comments", min_value=0, step=1)
    shares = st.number_input("Shares", min_value=0, step=1)
    likes = st.number_input("Likes", min_value=0, step=1)
    profile_visits = st.number_input("Profile Visits", min_value=0, step=1)
    follows = st.number_input("Follows", min_value=0, step=1)
    caption_length = st.number_input("Caption Length (characters)", min_value=0, step=1)
    hashtag_count = st.number_input("Hashtag Count", min_value=0, step=1)
    engagement_rate = st.number_input("Engagement Rate (%)", min_value=0.0, step=0.01, format="%.2f")

    if st.button("🔮 Predict Impressions"):
        input_data = pd.DataFrame([[saves, comments, shares, likes, profile_visits,
                                    follows, hashtag_count, caption_length, engagement_rate]],
                                  columns=FEATURE_COLUMNS)

        prediction = model.predict(input_data)
        st.success(f"*Predicted Impressions:* {int(prediction[0]):,}")
        st.info("💡 Tip: Try adjusting likes & shares to see impact on impressions.")

# -----------------------------
# Batch Prediction Mode
# -----------------------------
elif mode == "Batch Prediction (CSV Upload)":
    st.subheader("📂 Batch Predictions from CSV")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    # Provide sample template
    sample_csv = """Saves,Comments,Shares,Likes,Profile Visits,Follows,Hashtag Count,Caption Length,Engagement Rate
10,5,3,200,20,5,7,120,4.5
2,1,1,50,10,2,3,80,2.1
5,3,2,150,15,4,6,100,3.8
0,0,0,20,2,0,1,40,1.2
"""

    st.download_button(
        label="📥 Download Sample CSV Template",
        data=sample_csv,
        file_name="instagram_input_template.csv",
        mime="text/csv"
    )

    if uploaded_file is not None:
        try:
            user_df = pd.read_csv(uploaded_file)

            # ✅ Auto-fix: ensure correct columns
            for col in FEATURE_COLUMNS:
                if col not in user_df.columns:
                    user_df[col] = 0
            user_df = user_df[FEATURE_COLUMNS]  # drop extras + reorder

            st.write("✅ Processed Input Data:")
            st.dataframe(user_df.head())

            # Predictions
            predictions = model.predict(user_df)
            user_df["Predicted Impressions"] = predictions.astype(int)

            st.write("📊 Predictions:")
            st.dataframe(user_df)

            # Download option
            st.download_button(
                label="📥 Download Predictions as CSV",
                data=user_df.to_csv(index=False),
                file_name="predicted_impressions.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

st.markdown("---")
st.caption("Developed with ❤ using Streamlit and XGBoost")