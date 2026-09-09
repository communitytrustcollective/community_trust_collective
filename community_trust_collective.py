import os
import tempfile

import polars as pl
import streamlit as st
from cryptography.fernet import Fernet
st.set_option("client.disableDataExport", True)


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
st.caption('***Helping communities share safety information***')



left, right = st.columns(2)
with left:
    st.link_button("Submit a report", "https://forms.gle/PAd3saAcoHnLrmeK9", type="primary", use_container_width=True)
with right:
    st.link_button("Request Access", "https://forms.gle/3f6bBRaiBmrmRQGSA", type="primary", use_container_width=True)






st.text('')
st.markdown('''**:gray-background[Problem -]** Individuals with a history of misconduct may move between communities to where organizers are unaware of their history. 

**:gray-background[Solution -]** This tool helps organizers identify potential safety concerns by securely sharing limited information about reported misconduct and, where appropriate, allows them to contact the original community for additional context.

**:gray-background[Challenges -]** International privacy laws make sharing sensitive allegations difficult, so we intentionally limit the information we provide to reduce legal and privacy risks.


Reports may range from code-of-conduct concerns that led to community action, to more serious allegations. Information in this system is provided for community safety purposes and does not constitute a finding of guilt or wrongdoing. A record should be treated as a reason for organizers to seek additional information and make their own informed decisions. Users are responsible for using and handling information in accordance with applicable laws and privacy requirements.''')



st.link_button('Contact/Feedback', 'https://forms.gle/LMJTYYKUoPixNjn59')
st.caption("Positive feedback helps us know we're on the right track, and constructive feedback helps us improve.")


with st.expander("Legal Disclaimer"):
    st.caption('''The West Coast Swing **Community Trust Collective** (**CTC**) is a private safeguarding and coordination system. It is not a court, law-enforcement database, criminal-record database, investigative agency, or adjudicative body.

The existence of a report in CTC does not establish that an allegation is true and does not constitute a finding of criminal or civil liability. Reports may concern circumstances of substantially different nature and seriousness, and an organizer's response may range from a warning or conversation to more significant organizational action.

A CTC match should therefore be treated as an indication that relevant information may exist - not as proof of misconduct or as an automatic basis for exclusion. Organizers are responsible for evaluating information in context and making their own decisions in accordance with their applicable legal and safeguarding responsibilities.

CTC reviews submissions and maintains safeguards intended to reduce fabricated, duplicate, abusive, or otherwise inappropriate submissions. However, no reporting or review system can guarantee that every underlying report is complete or accurate.

CTC is designed around data minimization, restricted access, and controlled disclosure. Personal information is used for the purposes of safeguarding and coordination and is not intended for public publication.

Where applicable, CTC processes personal information in accordance with relevant data-protection and privacy requirements, including the GDPR and applicable U.S. privacy laws.
''')











#FAQ
with st.expander("FAQ - Privacy, Safeguarding & Data Protection"):
    st.caption('''#### What is the CTC?
The West Coast Swing **Community Trust Collective** (**CTC**) is a permissioned incident-coordination network for the West Coast Swing community and its event organizers, with controlled matching and case-by-case disclosure.

CTC exists to help organizers in the West Coast Swing community avoid repeatedly rediscovering the same safeguarding concerns when people move between events or communities. It is designed as a private coordination tool, not a public blacklist or criminal-record database.

Authorized organizers can use CTC to determine whether prior incident reports may exist and, where appropriate, contact the organizer or point of contact responsible for the original report. CTC does not publicly publish allegations or automatically disclose the details of reports.

Submitting a report does not create a public listing, automatically trigger action, or determine that an allegation is true. Every submission is reviewed by the CTC review/moderation team before a report is recorded in the system.

A CTC record indicates that a report exists. It is not a criminal conviction, legal finding, or determination of guilt. Reports may vary considerably in nature and seriousness, and organizers remain responsible for evaluating information in context and making their own decisions.

---

#### How it works

**Report → Review → Limit → Connect → Decide**

**1. Report**  
A member/community submits a safety or code-of-conduct concern.

**2. Review**  
Our Care Team reviews the information against established inclusion criteria. We review reports, not people, and do not determine guilt.

**3. Limit**  
Only the minimum information necessary to identify a potential concern is added to the shared system. Sensitive allegations and personal details are not publicly published.

**4. Connect**  
When an authorized organizer identifies a potential match, they can contact the community that holds the underlying information.

**5. Decide**  
The organizer considers the additional context and makes their own informed decision according to their community's policies and applicable requirements.

> **The goal is not to create a blacklist. It is to help interconnected communities avoid safety information becoming isolated simply because someone travels from one community to another.**

#### Oversight

The process is supported by a **Care Team**, responsible for reviewing submissions, and an **Independent Audit Team**, responsible for reviewing the consistency, fairness, privacy, and security of the overall process.

---

#### What information does CTC store?
CTC follows a **data-minimization approach**.

Following review of a submission, the incident record is intended to contain only information necessary for its coordination purpose, generally:

- Name
- Report date
- Organizer action taken
- Appropriate point-of-contact information

CTC is not intended to serve as a repository for detailed allegations or unnecessary personal information.

Information necessary to operate, secure, and administer the service may also be retained where appropriate.

---

#### Why we keep information limited

Safety reports can contain highly sensitive personal information, and privacy laws vary between countries. Sharing detailed allegations across international borders can create significant legal and privacy risks. Unverified or inaccurate allegations can also cause serious reputational harm and potentially affect someone’s employment, professional opportunities, or livelihood.

To reduce these risks, this system intentionally stores and displays only the minimum information needed to identify a potential safety concern: whether relevant reports exist and how an authorized organizer can contact the community that holds the underlying information.

The system does **not** publish the details or allegations behind a report. Organizers who receive a potential match can contact the original reporting community directly to determine whether further information is appropriate and lawful to share.

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

#### How long is information retained?

CTC does not intend to retain information indefinitely simply because it was once submitted.

Information is retained only for as long as it is reasonably necessary for its intended purpose or where there is another applicable reason for continued retention.

Retention and deletion are subject to applicable legal and operational requirements.

---

#### Why is the data view designed this way?

Dance communities are highly interconnected, and people frequently travel between regions and countries. Limiting information geographically can leave organizers unaware of relevant safety concerns simply because they were reported somewhere else.

***Authorized community organizers need sufficient visibility across communities to identify safety concerns that would otherwise remain geographically siloed.*** To balance this need with privacy, the system limits the amount of information displayed and the way information is presented may evolve as we evaluate privacy, safety, and legal considerations.

---

# For Those Covered by GDPR

#### How can CTC store information about me if I never gave consent?

**Consent is not the only legal basis for processing personal data under the GDPR.**

The GDPR allows personal data to be processed in circumstances where consent has not been given. One potential legal basis is **legitimate interests**, where processing is necessary for a legitimate purpose and the interests or fundamental rights and freedoms of the individual do not override that purpose.

CTC is designed around the legitimate interest of helping protect people participating in the West Coast Swing community and helping organizers respond appropriately to safeguarding concerns.

This does **not** mean that CTC can collect whatever information it wants. The GDPR still requires personal data to be processed lawfully and transparently, collected for specified purposes, limited to what is necessary, and protected against unauthorized access.

---

#### Why does CTC need to keep information about people who have not consented?

Safeguarding information can lose much of its value if it must be deleted simply because the person concerned does not consent to its retention.

For example, if an incident is reported to an organizer and that information is immediately deleted whenever the person concerned objects to its existence, a future organizer may have no way to know that relevant information previously existed.

CTC therefore uses a limited amount of information for the specific purpose of helping organizers identify whether relevant safeguarding information may exist. The purpose is **not to create a public record about people or to label people as dangerous or guilty.**

---

#### What information does CTC actually store?

CTC is designed to use **data minimization**: information should be limited to what is necessary for the purpose for which it is being processed.

The CTC record is intentionally limited rather than attempting to maintain a complete dossier about an individual. The information used for coordination is primarily intended to identify a person, indicate that a report exists, record the date and relevant organizational action, and allow an appropriate point of contact to be identified where necessary.

CTC does not need to maintain every piece of information that may have existed in connection with an underlying incident.

---

#### Who can see information about me?

CTC is **not a public database**.

Access is restricted to authorized users with a legitimate role in West Coast Swing event or community coordination. Information is not intended to be published publicly or made available to everyone in the community.

Access to additional information about a particular report is also controlled separately. In particular, contact information belonging to another person is not automatically disclosed simply because a match exists.

This restricted-access approach is part of CTC's effort to limit unnecessary disclosure of personal information. The GDPR requires appropriate technical and organizational measures to protect personal data against unauthorized or unlawful processing and unauthorized access.

---

#### Does being listed in CTC mean that I did something wrong?

**No.**

The existence of a CTC record means that a report has been submitted and recorded. It does not by itself establish that an allegation is true, that the person committed a crime, or that the person should be excluded from an event.

Reports can concern circumstances of substantially different nature and seriousness, and an organizer's response may range from a warning or conversation to more significant action.

CTC is a coordination system, not a court or law-enforcement database.

---

#### Can I object to my information being processed?

Yes. GDPR provides data-subject rights that can apply to information held by CTC, including rights relating to access, rectification, erasure, restriction of processing, and objection, subject to the circumstances and applicable legal exceptions.

Where processing is based on legitimate interests, an individual generally has a right to object based on their particular situation. Processing may nevertheless continue where there are compelling legitimate grounds that override the individual's interests, rights, and freedoms, or where another applicable GDPR provision permits continued processing.

Requests are therefore considered individually rather than automatically granting or denying every request.

---

#### Why can't you simply delete my record if I ask?

The GDPR's right to erasure is **not absolute**.

Whether information can be deleted depends on the circumstances, including the legal basis for processing and whether there are legitimate grounds for continuing to retain the information.

For a safeguarding system, deleting relevant information solely because the person concerned objects could undermine the very purpose for which the information is being retained. At the same time, CTC does not treat indefinite retention as automatically justified.

Information should only be retained for as long as it is necessary for its legitimate purpose, consistent with the GDPR's principle of storage limitation.

---

#### Why don't you publish the reports so everyone can make their own decision?

Because **privacy and safeguarding are not served by making sensitive allegations publicly searchable**.

CTC is intended to provide relevant information to people who have a legitimate need for it, rather than create a public blacklist.

Keeping access restricted also reduces unnecessary disclosure of personal information and limits the potential impact on both the person named in a report and the people who provided information about an incident.

---

#### Does CTC assume that every report is accurate?

**No.**

CTC does not represent that every underlying report is complete or accurate. Reports may be incomplete, disputed, mistaken, or based on information that requires further context.

That is why a CTC match is an indication that **relevant information may exist**, rather than a determination that misconduct occurred.

Organizers remain responsible for evaluating information in context and making their own decisions.

---

#### Is CTC claiming that GDPR gives it permission to ignore people's privacy rights?

**No.**

The opposite is the intention.

The fact that consent may not be required does not mean that GDPR requirements disappear. CTC still needs an appropriate legal basis for processing, a defined purpose, data minimization, appropriate security, appropriate retention, and respect for applicable data-subject rights.

The goal is to balance two legitimate interests: **protecting people participating in the community and protecting the privacy and rights of the individuals whose information is processed.**

''')







access_code = st.text_input(
    "**Enter Secure Access Token**",
    type="password",
)

if access_code.strip() not in ACCESS_CODES:
    st.stop()

df = load_database()




st.text('')

to_find = st.text_area('''**Filter Safety Records:**

Check an attendee list against our safety records by pasting names or WSDC numbers (one per line). This will filter to ***potentially*** relevant results. There may be false positives, please ensure any results refer to the correct individuals.''', placeholder='''Name or WSDC number
Name2 or WSDC number
Name3 or WSDC number''')

st.button('Filter', type="primary")

names_list = [name.strip() for name in to_find.splitlines() if name.strip()]
if not names_list:
    #names_list = ["__EMPTY_INPUT_NO_RESULTS_FOUND__"]
    filtered_results_df = df
else:
    filtered_results_df = (df
    .filter(pl.col("Name").str.contains_any(names_list, ascii_case_insensitive=True)
            | pl.col("WSDC_number").cast(pl.String).str.contains_any(names_list, ascii_case_insensitive=True)
           )
)

st.dataframe(filtered_results_df, 
column_config={"Name": st.column_config.Column(width=160), 
               "WSDC_number": st.column_config.Column(width=100, alignment="center"),
               "Reports": st.column_config.Column(width=60, alignment="center"),
               "Actions_taken": st.column_config.Column(width=100),
               "Points_of_contact": st.column_config.Column(width=120, alignment="center"),
               "Report_dates": st.column_config.Column(width=200),
},
            use_container_width=True)

st.text('')
st.link_button("Request More Information About a Report", "https://forms.gle/gppbdjb5aYjAzSTk7")
st.caption('If you need more context about a report, you can request contact information for additional details.')