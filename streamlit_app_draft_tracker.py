
import streamlit as st
import pandas as pd
from utils.value_assignment import assign_values

st.set_page_config(page_title="BLOC Draft Tool", layout="wide")
st.title("🏈 BLOC Fantasy Draft Tool")

# Configurable constants
TOTAL_BUDGET = 320
ROSTER_LIMITS = {
    "QB": 2,
    "RB": 2,
    "WR": 3,
    "TE": 1,
    "FLEX": 1,
    "DEF": 1
}

# Session state initialization
if 'drafted_players' not in st.session_state:
    st.session_state.drafted_players = []
if 'remaining_budget' not in st.session_state:
    st.session_state.remaining_budget = TOTAL_BUDGET
if 'roster_counts' not in st.session_state:
    st.session_state.roster_counts = {pos: 0 for pos in ROSTER_LIMITS}

# File upload and processing
uploaded_file = st.file_uploader("Upload Player Stats CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = assign_values(df)

    st.sidebar.markdown("## 💰 Draft Tracker")
    st.sidebar.write(f"Remaining Budget: ${st.session_state.remaining_budget}")

    for pos, limit in ROSTER_LIMITS.items():
        count = st.session_state.roster_counts.get(pos, 0)
        st.sidebar.write(f"{pos}: {count}/{limit}")

    # Filter out already drafted players
    drafted_names = [p['player_display_name'] for p in st.session_state.drafted_players]
    available_df = df[~df['player_display_name'].isin(drafted_names)]

    # Position filter
    pos_filter = st.selectbox("Filter by Position", ["All"] + list(ROSTER_LIMITS.keys()))
    if pos_filter != "All":
        available_df = available_df[available_df['position'] == pos_filter]

    # Sort by dollar value
    st.dataframe(available_df.sort_values(by="auto_dollar_value", ascending=False), use_container_width=True)

    # Draft player
    draft_name = st.selectbox("Select player to draft", available_df['player_display_name'].tolist())
    if st.button("➕ Draft Player"):
        player_row = available_df[available_df['player_display_name'] == draft_name].iloc[0]
        player_cost = player_row['auto_dollar_value']
        position = player_row['position']

        # Determine applicable roster slot
        is_flex = position in ["RB", "WR", "TE"] and st.session_state.roster_counts["FLEX"] < ROSTER_LIMITS["FLEX"]
        position_filled = st.session_state.roster_counts.get(position, 0) >= ROSTER_LIMITS.get(position, 0)

        if position_filled and not is_flex:
            st.error(f"Cannot draft {position}: position already full.")
        elif st.session_state.remaining_budget < player_cost:
            st.error("Insufficient budget.")
        else:
            # Allocate player
            st.session_state.drafted_players.append(player_row.to_dict())
            st.session_state.remaining_budget -= player_cost

            if is_flex:
                st.session_state.roster_counts["FLEX"] += 1
            else:
                st.session_state.roster_counts[position] += 1

            st.success(f"{draft_name} drafted!")

    # Display drafted players
    if st.session_state.drafted_players:
        st.markdown("### ✅ Drafted Players")
        st.dataframe(pd.DataFrame(st.session_state.drafted_players))
else:
    st.info("Upload a cleaned player stats CSV to begin.")
