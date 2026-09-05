import os
import tempfile

import polars as pl
import streamlit as st
from cryptography.fernet import Fernet

ENCRYPTED_FILE = "CommunityTrustCollective.parquet.enc"


ACCESS_CODES = {
    code.strip()
    for code in st.secrets["access_codes"]
}


@st.cache_resource
def load_database():
    cipher = Fernet(st.secrets["ENCRYPTION_KEY"].encode())

    # Read encrypted file
    with open(ENCRYPTED_FILE, "rb") as f:
        encrypted = f.read()

    # Decrypt into one plaintext bytes object
    decrypted = cipher.decrypt(encrypted)

    # Encrypted bytes no longer needed
    del encrypted

    # Put plaintext on disk instead of keeping it in another RAM buffer
    with tempfile.NamedTemporaryFile(
        suffix=".parquet",
        delete=False,
    ) as temp:
        temp_path = temp.name
        temp.write(decrypted)

    # Plaintext bytes no longer needed
    del decrypted

    try:
        # Polars reads directly from the temporary file
        df = pl.read_parquet(temp_path)
    finally:
        os.remove(temp_path)

    return df


st.title("Community Trust Collective")

access_code = st.text_input(
    "Access code",
    type="password",
)

if access_code.strip() not in ACCESS_CODES:
    st.stop()

df = load_database()

st.dataframe(df, use_container_width=True)