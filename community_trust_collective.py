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


st.markdown('## WCS Community Trust Collective')

st.link_button("Submit a report", "https://forms.gle/PAd3saAcoHnLrmeK9", type='primary')

st.markdown('''The Community Trust Collective (CTC) is a permissioned incident-coordination network for the West Coast Swing community and its event organizers, with controlled matching and case-by-case disclosure.

CTC exists to help organizers in the West Coast Swing community avoid repeatedly rediscovering the same safeguarding concerns when people move between events or communities. It is designed as a private coordination tool, not a public blacklist or criminal-record database.

Authorized organizers can use CTC to determine whether prior incident reports may exist and, where appropriate, contact the organizer or point of contact responsible for the original report. CTC does not publicly publish allegations or automatically disclose the details of reports.

Submitting a report does not create a public listing, automatically trigger action, or determine that an allegation is true. Every submission is reviewed by the CTC review/moderation team before a report is recorded in the system.

A CTC record indicates that a report exists. It is not a criminal conviction, legal finding, or determination of guilt. Reports may vary considerably in nature and seriousness, and organizers remain responsible for evaluating information in context and making their own decisions.
''')

st.link_button("Request Access", "https://forms.gle/3f6bBRaiBmrmRQGSA")

st.caption('''#### Important Disclaimer
The Community Trust Collective (CTC) is a private safeguarding and coordination system. It is not a court, law-enforcement database, criminal-record database, investigative agency, or adjudicative body.

The existence of a report in CTC does not establish that an allegation is true and does not constitute a finding of criminal or civil liability. Reports may concern circumstances of substantially different nature and seriousness, and an organizer's response may range from a warning or conversation to more significant organizational action.

A CTC match should therefore be treated as an indication that relevant information may exist - not as proof of misconduct or as an automatic basis for exclusion. Organizers are responsible for evaluating information in context and making their own decisions in accordance with their applicable legal and safeguarding responsibilities.

CTC reviews submissions and maintains safeguards intended to reduce fabricated, duplicate, abusive, or otherwise inappropriate submissions. However, no reporting or review system can guarantee that every underlying report is complete or accurate.

CTC is designed around data minimization, restricted access, and controlled disclosure. Personal information is used for the purposes of safeguarding and coordination and is not intended for public publication.

Where applicable, CTC processes personal information in accordance with relevant data-protection and privacy requirements, including the GDPR and applicable U.S. privacy laws.
''')











#FAQ
with st.expander("Privacy, Safeguarding & Data Protection FAQ"):
    st.markdown('''#### What information does CTC store?
CTC follows a **data-minimization approach**.

Following review of a submission, the incident record is intended to contain only information necessary for its coordination purpose, generally:

- Name
- Report date
- Organizer action taken
- Appropriate point-of-contact information

CTC is not intended to serve as a repository for detailed allegations or unnecessary personal information.

Information necessary to operate, secure, and administer the service may also be retained where appropriate.

---

#### Who can submit a report?

Reports may be submitted by people with relevant firsthand information about an incident or concern.

Submitting a report does not create a public listing, automatically trigger action, or establish that an allegation is true. Submissions are reviewed before being recorded in the CTC coordination system.

---
#### What happens when someone submits a report?

A submission is reviewed before a report is recorded in CTC.

The purpose of the review is to determine whether the submission is appropriate for inclusion in the coordination system and to reduce inappropriate or abusive use.

A submission does not automatically result in a public listing, exclusion from an event, or other action against the person named in the report.

---
#### Does CTC publish allegations?

**No.**

CTC does not operate as a public list of people accused of misconduct.

Access to information is restricted, and information is disclosed on a case-by-case basis for legitimate safeguarding and coordination purposes.

Where appropriate, CTC can help an authorized organizer determine whether a prior report exists and contact the organizer or point of contact responsible for that report.

---

#### Why does CTC need to retain this information?

The purpose is to allow event organizers to determine whether a relevant prior report may exist and, when appropriate, communicate with the organizer who handled the original matter.

Without some persistent record, organizers may repeatedly encounter the same safeguarding concern without knowing that another organizer has previously dealt with it.

CTC therefore focuses on retaining the information necessary to facilitate responsible coordination rather than attempting to maintain a comprehensive history about an individual.

---

#### Does being in CTC mean someone has been found guilty?

**No.**

A CTC record is not a criminal conviction, judicial finding, or determination that an allegation is true.

Reports may concern circumstances of substantially different nature and seriousness. An organizer's response may range from a warning or conversation to more significant organizational action.

The existence of a report should therefore not be treated as proof of misconduct.

---

#### Does CTC determine whether an allegation is true?

**No.**

CTC is not a court, law-enforcement agency, investigative authority, or adjudicative body.

The purpose of reviewing submissions is to determine whether they are appropriate for inclusion in the coordination system, not to make a legal determination about the underlying conduct.

Where additional information is appropriate, authorized organizers may communicate with the organizer or point of contact responsible for the original report.

---

#### Does CTC automatically ban people?

**No.**

CTC does not make admission, exclusion, or disciplinary decisions for event organizers.

A CTC match does not automatically require an organizer to exclude someone or take any particular action.

Organizers are responsible for considering information in context and making their own decisions regarding their events.

---

#### What if a report only resulted in a warning?

Not every report represents the same level of concern.

An organizer may respond to an incident with a conversation, warning, behavioral expectation, temporary restriction, exclusion from a particular event, or another safeguarding measure.

The action taken is therefore important context. A report resulting in a warning should not be assumed to represent the same circumstances as a report resulting in more significant action.

---

#### What safeguards are there against misuse?

Submissions are reviewed before a report is recorded in the coordination system.

CTC also maintains safeguards intended to reduce fabricated, duplicate, abusive, or otherwise inappropriate use of the system.

Use of CTC for harassment, retaliation, knowingly false reporting, or purposes unrelated to legitimate safeguarding coordination is not permitted.

---

#### Can someone use CTC to blacklist another person?

CTC is specifically designed not to function as a public blacklist.

The existence of a report does not by itself determine that a person should be excluded from events or communities.

Information is intended to be considered by authorized organizers in the context of their own safeguarding responsibilities rather than treated as an automatic classification of an individual.

---

#### Why isn't everything made public?

A public database of allegations could expose individuals to significant privacy and reputational harm, particularly where allegations have not resulted in a legal finding.

CTC instead uses controlled access and case-by-case disclosure so that relevant organizers can coordinate without creating a publicly searchable list of allegations.

---

#### Who can see information in CTC?

CTC uses permissioned access. Information is made available only to users who are authorized to access it for legitimate purposes within the system.

---

#### What happens if someone disputes a report?

Individuals who believe information about them is inaccurate, incomplete, or inappropriate may raise the issue with CTC.

Requests are considered in light of the circumstances and applicable privacy law. Where appropriate, information may be corrected, restricted, or removed.

Because CTC also has privacy responsibilities toward people who provide information, addressing a dispute does not necessarily mean that confidential information about another person will be disclosed.

---

#### Can someone request access to information held about them?

Where applicable law provides such rights, individuals may request access to personal information held about them and may have additional rights concerning correction, restriction, objection, or deletion.

Such requests are handled in accordance with applicable privacy law, including any lawful exceptions or limitations.

---

#### Can someone request deletion?

Where applicable law provides a right to deletion, an individual may request that personal information be deleted.

Deletion rights are not absolute, and certain information may be retained where there is a lawful reason to do so, such as legitimate safeguarding, legal, security, or dispute-resolution purposes.

CTC does not intend to retain personal information indefinitely when it is no longer necessary for its purpose.

---

#### What about sensitive information or reports involving sexual misconduct?

CTC recognizes that safeguarding reports can involve highly sensitive information.

The system is therefore designed around **data minimization and controlled disclosure**.

CTC is not intended to retain unnecessary details about an incident, including information that is not needed for its coordination purpose.

The existence of a report should not be interpreted as a criminal conviction or legal finding.

At the same time, event organizers may need to make safeguarding decisions without a criminal conviction or formal legal proceeding. Those organizational decisions and a legal determination of criminal conduct are separate matters.

---

#### Does CTC assume that every report is accurate?

**No.**

Incident reports can be disputed, incomplete, misunderstood, or contain errors.

The review process is intended to reduce inappropriate use of the system, but no reporting or review process can guarantee that every underlying report is complete or accurate.

For that reason, a CTC record should be treated as information requiring appropriate context rather than as an unquestionable statement of fact.

---

#### Is CTC a criminal-record database?

**No.**

CTC is a private safeguarding and coordination system.

A CTC record does not establish that an individual has been arrested, charged, prosecuted, or convicted of a crime.

---

#### Is a CTC record proof that someone is dangerous?

**No.**

A record indicates that a report exists. Reports can differ substantially in their circumstances, seriousness, and outcome.

CTC is not intended to create a definitive risk score or classification of an individual.

Organizers should consider relevant information in context and make their own decisions.

---

#### How does CTC protect personal information?

CTC seeks to protect personal information through data minimization, restricted access, and controlled disclosure.

Personal information is used for the purposes of safeguarding and coordination and is not intended for public publication.

CTC does not sell personal information.

---

### How long is information retained?

CTC does not intend to retain information indefinitely simply because it was once submitted.

Information is retained only for as long as it is reasonably necessary for its intended purpose or where there is another applicable reason for continued retention.

Retention and deletion are subject to applicable legal and operational requirements.

---
''')







access_code = st.text_input(
    "Secure Access Token",
    type="password",
)

if access_code.strip() not in ACCESS_CODES:
    st.stop()

df = load_database()





st.dataframe(df, use_container_width=True)


st.link_button("Request PoC Information", "https://forms.gle/gppbdjb5aYjAzSTk7")

to_find = st.text_area('Input attendee list')

#attendee list