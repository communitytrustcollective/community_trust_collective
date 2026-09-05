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
st.markdown('''# Community Trust Collective

The Community Trust Collective (CTC) is a permissioned incident-coordination network for event organizers, with controlled matching and case-by-case disclosure.

CTC exists to help organizers avoid repeatedly rediscovering the same safeguarding concerns when people move between events or communities. It is designed as a **private coordination tool**, not a public blacklist or criminal-record database.

Authorized organizers can use CTC to determine whether prior incident reports may exist and, where appropriate, contact the organizer or point of contact responsible for the original report. CTC does not publicly publish allegations or automatically disclose the details of reports.

Submitting a report does not create a public listing, automatically trigger action, or determine that an allegation is true. Every submission is reviewed by the CTC review/moderation team before a report is recorded in the system.

A CTC record indicates that a report exists. It is not a criminal conviction, legal finding, or determination of guilt. Reports may vary considerably in nature and seriousness, and organizers remain responsible for evaluating information in context and making their own decisions.



# Important Disclaimer
The Community Trust Collective (CTC) is a private safeguarding and coordination system. It is not a court, law-enforcement database, criminal-record database, investigative agency, or adjudicative body.

The existence of a report in CTC does not establish that an allegation is true and does not constitute a finding of criminal or civil liability. Reports may concern circumstances of substantially different nature and seriousness, and an organizer's response may range from a warning or conversation to more significant organizational action.

A CTC match should therefore be treated as an indication that relevant information may exist—not as proof of misconduct or as an automatic basis for exclusion. Organizers are responsible for evaluating information in context and making their own decisions in accordance with their applicable legal and safeguarding responsibilities.

CTC reviews submissions and maintains safeguards intended to reduce fabricated, duplicate, abusive, or otherwise inappropriate submissions. However, no reporting or review system can guarantee that every underlying report is complete or accurate.

CTC is designed around data minimization, restricted access, and controlled disclosure. Personal information is used for the purposes of safeguarding and coordination and is not intended for public publication.

Where applicable, CTC processes personal information in accordance with relevant data-protection and privacy requirements, including the GDPR and applicable U.S. privacy laws.
''')









access_code = st.text_input(
    "Secure Access Code",
    type="password",
)

if access_code.strip() not in ACCESS_CODES:
    st.stop()

df = load_database()





st.dataframe(df, use_container_width=True)



#request POC information
#request access
#attendee list