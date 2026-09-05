import io

import polars as pl
import streamlit as st
from cryptography.fernet import Fernet

ENCRYPTED_FILE = "CommunityTrustCollective.parquet.enc"


ACCESS_CODES = set(st.secrets["access_codes"])


@st.cache_resource
def load_database():
    key = st.secrets["ENCRYPTION_KEY"].encode()
    cipher = Fernet(key)

    with open(ENCRYPTED_FILE, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    return pl.read_parquet(io.BytesIO(decrypted_data))


st.title("Community Trust Collective")

access_code = st.text_input(
    "Access code",
    type="password",
)

if access_code not in ACCESS_CODES:
    st.error("Invalid access code.")
    st.stop()

df = load_database()

st.dataframe(df, use_container_width=True)