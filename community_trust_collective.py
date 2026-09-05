import streamlit as st

st.title("Private Database")

if not st.user.is_logged_in:
    st.button("Log in with Google", on_click=st.login)
    st.stop()

st.success("Google login successful!")
st.write(f"Name: {st.user.name}")
st.write(f"Email: {st.user.email}")

st.button("Log out", on_click=st.logout)






# import os
# import tempfile

# import polars as pl
# import streamlit as st
# from cryptography.fernet import Fernet


# # ============================================================
# # CONFIGURATION
# # ============================================================

# ENCRYPTED_FILE = "CommunityTrustCollective.parquet.enc"


# # ============================================================
# # GOOGLE OIDC AUTHENTICATION
# # ============================================================

# if not st.user.is_logged_in:
#     st.title("Private Database")
#     st.button("Log in with Google", on_click=st.login)
#     st.stop()


# # ============================================================
# # AUTHORIZATION
# # ============================================================

# approved_users = {
#     email.strip().casefold()
#     for email in st.secrets["app"]["approved_users"]
# }

# user_email = st.user.email.strip().casefold()

# if user_email not in approved_users:
#     st.error("Your Google account has not been approved for access.")
#     st.write(f"Signed in as: {st.user.email}")
#     st.button("Log out", on_click=st.logout)
#     st.stop()


# # ============================================================
# # LOAD AND DECRYPT DATABASE
# # ============================================================

# @st.cache_resource
# def load_database():
#     key = st.secrets["ENCRYPTION_KEY"].encode()

#     # Fernet requires the complete encrypted message in memory.
#     with open(ENCRYPTED_FILE, "rb") as f:
#         encrypted_data = f.read()

#     cipher = Fernet(key)

#     # Fernet necessarily creates the complete decrypted file
#     # in memory. This is the unavoidable part.
#     decrypted_data = cipher.decrypt(encrypted_data)

#     # Write the decrypted Parquet to a temporary file instead
#     # of wrapping it in BytesIO. This avoids another in-memory
#     # representation and lets Polars read a real Parquet file.
#     temp_path = None

#     try:
#         with tempfile.NamedTemporaryFile(
#             suffix=".parquet",
#             delete=False,
#         ) as temp_file:
#             temp_path = temp_file.name
#             temp_file.write(decrypted_data)

#         # We no longer need the decrypted bytes.
#         del decrypted_data

#         # Read the actual Parquet file with Polars.
#         df = pl.read_parquet(temp_path)

#     finally:
#         # Remove the temporary plaintext file.
#         if temp_path is not None:
#             try:
#                 os.remove(temp_path)
#             except FileNotFoundError:
#                 pass

#     # The encrypted bytes are also no longer needed.
#     del encrypted_data

#     return df


# df = load_database()


# # ============================================================
# # DISPLAY
# # ============================================================

# st.title("Private Database")

# st.caption(f"Signed in as {st.user.email}")

# st.dataframe(
#     df,
#     use_container_width=True,
# )

# st.button("Log out", on_click=st.logout)