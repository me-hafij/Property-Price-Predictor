import streamlit as st

from main import (
    load_dataset,
    train_model,
    predict_price,
    format_price
)

# Page configuration
st.set_page_config(
    page_title="Real Estate Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Train model and cache it
@st.cache_resource
def get_model():
    data = load_dataset()
    model, metrics, method = train_model(data)
    return model, metrics, method


# Website heading
st.title("🏠 Real Estate Price Predictor")

st.subheader(
    "Machine Learning Based Property Price Estimation"
)

st.write(
    "Enter your property details to estimate "
    "its residential market price."
)

# Load model
try:
    model, metrics, method = get_model()

    st.success(f"Model ready: {method}")

    st.caption(
        f"Dataset contains {metrics['samples']} properties."
    )

except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()


st.divider()

# Input section
st.header("Enter Property Details")

col1, col2 = st.columns(2)

with col1:

    area = st.number_input(
        "Area (square feet)",
        min_value=100,
        max_value=10000,
        value=1200
    )

    bedrooms = st.number_input(
        "Number of bedrooms",
        min_value=1,
        max_value=20,
        value=3
    )

    bathrooms = st.number_input(
        "Number of bathrooms",
        min_value=1,
        max_value=20,
        value=2
    )

    age = st.number_input(
        "Property age (years)",
        min_value=0,
        max_value=100,
        value=5
    )

with col2:

    floor = st.number_input(
        "Floor number",
        min_value=0,
        max_value=100,
        value=4
    )

    parking = st.number_input(
        "Parking spaces",
        min_value=0,
        max_value=10,
        value=1
    )

    location = st.selectbox(
        "Property location",
        [
            "Kolkata",
            "Howrah",
            "Salt Lake",
            "New Town",
            "Bardhaman",
            "Durgapur"
        ]
    )


# Prediction button
if st.button("Predict Property Price"):

    property_data = {

        "area_sqft": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "age_years": age,
        "floor": floor,
        "parking": parking,
        "location": location

    }

    try:

        price, used = predict_price(
            property_data,
            model
        )

        st.divider()

        st.subheader("Prediction Result")

        st.metric(
            "Estimated Property Price",
            format_price(price)
        )

        st.info(f"Prediction method: {used}")

        st.caption(
            "This is an academic machine learning estimate, "
            "not a professional property valuation."
        )

    except Exception as e:

        st.error(f"Prediction failed: {e}")


st.divider()

# About section
st.subheader("About This Project")

st.write(
    """
    This project uses a Random Forest Regression model
    to estimate residential property prices.

    Parameters considered:

    - Property area
    - Bedrooms
    - Bathrooms
    - Property age
    - Floor number
    - Parking availability
    - Location

    Developed by Group 9.
    """
)

st.caption(
    "Python for Machine Learning | Brainware University"
)