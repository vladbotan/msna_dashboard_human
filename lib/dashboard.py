"""Shared data loading, sidebar filters and KPI header for every dashboard page.

Every page renders the same sidebar and the same KPI block, so both live here
and each view calls `page_setup()` before drawing its own charts.
"""

import pandas as pd
import streamlit as st

# (widget label, column in the sheet, session_state key)
FILTERS = [
    ("Please select Sex", "What is your sex?", "filter_sex"),
    ("Please select Age Group", "Age_grp", "filter_age"),
    ("Please select Nationality", "What is your citizenship?", "filter_nationality"),
    (
        "Please select Legal Status",
        "What is your current status (e.g., refugee, asylum seeker, etc.)?",
        "filter_legal_status",
    ),
    (
        "Please select Ethnicity",
        "Please specify what ethnic minority group",
        "filter_ethnicity",
    ),
    (
        "Please select Accommodation",
        "Do you currently live in a city or a village?",
        "filter_accommodation",
    ),
    (
        "Please select the duration of stay in Moldova",
        "How long have you been in the Republic of Moldova?",
        "filter_duration_of_stay",
    ),
]

HOUSEHOLD_SIZE_COLUMN = "How many members are in your household, including you?"
CHILDREN_COLUMN = "Of these, how many are children under 18?"
ELDERLY_COLUMN = "Of these, how many are senior citizens, aged over 60?"
AGE_COLUMN = "What is your age?"


@st.cache_data
def load_data():
    """Read the survey export. Cached once for the whole app, not per page."""
    sheet_id = st.secrets["data_link"]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(csv_url)


def _apply_filters(df, selections):
    mask = pd.Series(True, index=df.index)
    for column, selected in selections.items():
        # isin() matches NaN against NaN, so blank answers survive the default
        # selection instead of being silently dropped.
        mask &= df[column].isin(selected)
    return df[mask]


def render_sidebar(df):
    """Draw the filter sidebar and return the filtered dataframe."""
    selections = {}
    with st.sidebar:
        st.header("Filters")

        for label, column, key in FILTERS:
            options = df[column].unique()
            selections[column] = st.multiselect(
                label, options=options, default=options, key=key
            )

        filtered_df = _apply_filters(df, selections)

        st.markdown("---")
        st.header("Actions")
        button_col1, button_col2 = st.columns(2)
        with button_col1:
            refresh_button = st.button("Data Refresh")
        with button_col2:
            reset_button = st.button("Reset Filters")

        if refresh_button:
            load_data.clear()
            st.rerun()

        if reset_button:
            # Widgets keep their state across reruns, so the stored selections
            # have to be dropped for the defaults to apply again.
            for _, _, key in FILTERS:
                st.session_state.pop(key, None)
            st.rerun()

        st.markdown(f"**Total Submissions: {len(filtered_df)}**")

    return filtered_df


def render_kpis(df):
    total_submissions = len(df)
    average_value = round(df[HOUSEHOLD_SIZE_COLUMN].mean(), 1)
    max_value = df[HOUSEHOLD_SIZE_COLUMN].max()
    kid_value = round(df[CHILDREN_COLUMN].mean(), 1)
    elderly_value = round(df[ELDERLY_COLUMN].mean(), 1)
    age_value = round(df[AGE_COLUMN].mean(), 1)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Total Submissions:** {total_submissions}")
    with col2:
        st.markdown(f"**Avg household size:** {average_value}")
    with col3:
        st.markdown(f"**Max household size:** {max_value}")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(f"**Avg # of children in a household:** {kid_value}")
    with col5:
        st.markdown(f"**Avg # of elderly in a household:** {elderly_value}")
    with col6:
        st.markdown(f"**Avg age:** {age_value}")


def page_setup(page_title):
    """Load data, draw the sidebar, KPIs and page header.

    Returns the filtered dataframe the page should chart. Halts the page when
    the active filters match nothing.
    """
    df = render_sidebar(load_data())

    if df.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    render_kpis(df)
    st.markdown("---")
    st.header(page_title)
    return df
