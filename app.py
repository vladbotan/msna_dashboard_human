import streamlit as st

st.set_page_config(
    page_title="MSNA:Dashboard",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("📊MSNA Survey: Data Analysis")
st.markdown("---")

# PAGE_SETUP

demographic_page = st.Page(
    page="views/demographic.py", title="Demographic Information", icon="🚻"
)
accommodation_page = st.Page(
    page="views/accommodation.py", title="Accommodation Information", icon="🏠"
)
household_page = st.Page(
    page="views/household.py", title="Household Information", icon="👨‍👩‍👧"
)
pwd_page = st.Page(page="views/pwd.py", title="PwD Information", icon="👩🏻‍🦯")

healthcare_access = st.Page(
    page="views/healthcare_access.py", title="Healthcare Access", icon="🏥"
)
health_insurance = st.Page(
    page="views/health_insurance.py",
    title="Health Insurance and Informations",
    icon="📝",
)

feedback_assessment = st.Page(
    page="views/feedback_assessment.py",
    title="Overall Assessment and Feedback",
    icon="💬",
)


safety_protection = st.Page(
    page="views/safety_protection.py", title="Safety and Protection", icon="🛡️"
)
mhpss_protection = st.Page(page="views/mhpss.py", title="MHPSS", icon="💆")
education_protection = st.Page(page="views/education.py", title="Education", icon="📚")
employment = st.Page(page="views/employment.py", title="Employment", icon="💼")
integration_and_involvement = st.Page(
    page="views/integration_and_involvement.py",
    title="Future Plans and Needs",
    icon="➡️",
)


pg = st.navigation(
    {
        "Demographic Information": [
            demographic_page,
            accommodation_page,
            household_page,
            pwd_page,
        ],
        "Health": [healthcare_access, health_insurance, feedback_assessment],
        "Protecion": [
            safety_protection,
            mhpss_protection,
            education_protection,
            employment,
            integration_and_involvement,
        ],
    }
)

pg.run()
