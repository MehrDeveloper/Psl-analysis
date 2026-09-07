import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="PSL Analysis", page_icon="🏏", layout="wide")

st.title("🏏 Pakistan Super League Data Analysis")
st.write("**Built by Mehr Hussain** | AI Engineer | Karachi")
st.divider()

@st.cache_data
def load_data():
    df = pd.read_csv("Psl_Complete_Dataset(2016-2024).csv")
    df['extras_type'].fillna('none', inplace=True)
    df['player_dismissed'].fillna('not_out', inplace=True)
    df['dismissal_kind'].fillna('not_out', inplace=True)
    df['fielder'].fillna('none', inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['is_wicket'] = df['is_wicket'].astype(int)
    return df

df = load_data()

# Sidebar filter
st.sidebar.header("🔍 Filter")
seasons = ['All'] + sorted(df['season'].unique().tolist())
selected = st.sidebar.selectbox("Select Season", seasons)
if selected != 'All':
    df = df[df['season'] == selected]

# Metrics
st.header("📊 Overview")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Deliveries",  f"{len(df):,}")
c2.metric("Matches",     df['match_id'].nunique())
c3.metric("Players",     df['batter'].nunique())
c4.metric("Sixes",       int((df['batsman_runs'] == 6).sum()))
c5.metric("Wickets",     int(df['is_wicket'].sum()))
st.divider()

# Q1 Team wins
st.header("🏆 Which Team Won the Most?")
wins = df.drop_duplicates('match_id')['winner'].value_counts()
fig1, ax1 = plt.subplots(figsize=(10, 4))
colors = ['#f43f5e','#a78bfa','#38bdf8','#34d399','#fbbf24','#fb923c']
bars = ax1.bar(wins.index, wins.values, color=colors[:len(wins)], width=0.5)
for bar, val in zip(bars, wins.values):
    ax1.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.2,
             str(val), ha='center', fontweight='bold')
ax1.set_xlabel("Team")
ax1.set_ylabel("Wins")
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
st.pyplot(fig1)
plt.close()

# Q2 Top batters
st.header("🏏 Top 10 Run Scorers")
top_batters = df.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.barh(top_batters.index[::-1], top_batters.values[::-1], color='#a78bfa')
for i, val in enumerate(top_batters.values[::-1]):
    ax2.text(val + 10, i, str(val), va='center', fontweight='bold')
ax2.set_xlabel("Total Runs")
plt.tight_layout()
st.pyplot(fig2)
plt.close()

# Q3 Top bowlers
st.header("🎯 Top 10 Wicket Takers")
top_bowlers = df[df['is_wicket']==1].groupby('bowler')['is_wicket'].count().sort_values(ascending=False).head(10)
fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.barh(top_bowlers.index[::-1], top_bowlers.values[::-1], color='#f43f5e')
for i, val in enumerate(top_bowlers.values[::-1]):
    ax3.text(val + 0.2, i, str(val), va='center', fontweight='bold')
ax3.set_xlabel("Total Wickets")
plt.tight_layout()
st.pyplot(fig3)
plt.close()

# Q4 Venues
st.header("🏟️ Top Venues")
venues = df.drop_duplicates('match_id').groupby('venue')['match_id'].count().sort_values(ascending=False).head(8)
fig4, ax4 = plt.subplots(figsize=(10, 4))
ax4.bar(venues.index, venues.values, color='#38bdf8', width=0.5)
for bar, val in zip(ax4.patches, venues.values):
    ax4.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.2,
             str(val), ha='center', fontweight='bold')
ax4.set_ylabel("Matches Hosted")
plt.xticks(rotation=25, ha='right')
plt.tight_layout()
st.pyplot(fig4)
plt.close()

# Q5 Runs per over
st.header("📈 Average Runs Per Over")
over_runs = df.groupby('over')['total_runs'].mean().round(2)
fig5, ax5 = plt.subplots(figsize=(10, 4))
ax5.plot(over_runs.index, over_runs.values,
         marker='o', color='#34d399', linewidth=2.5,
         markersize=7, markerfacecolor='white', markeredgewidth=2)
ax5.fill_between(over_runs.index, over_runs.values, alpha=0.15, color='#34d399')
ax5.set_xlabel("Over Number")
ax5.set_ylabel("Average Runs")
ax5.set_xticks(range(1, 21))
ax5.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig5)
plt.close()

# Q6 Dismissals
st.header("❌ How Do Batters Get Out?")
dismissals = df[df['is_wicket']==1]['dismissal_kind'].value_counts()
fig6, ax6 = plt.subplots(figsize=(9, 6))
import matplotlib.cm as cm
colors6 = [cm.tab20(i / max(len(dismissals), 1)) for i in range(len(dismissals))]

# Only show a % label on slices big enough to hold text; tiny slices
# (e.g. "hit wicket") get their name + % moved into a side legend
# instead, so labels never overlap each other.
def autopct_if_big(pct):
    return f'{pct:.1f}%' if pct >= 3 else ''

wedges, _, _ = ax6.pie(dismissals.values, labels=None,
        autopct=autopct_if_big, pctdistance=0.75,
        colors=colors6[:len(dismissals)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 2},
        textprops={'fontsize': 10, 'fontweight': 'bold', 'color': 'white'})

legend_labels = [f'{name} ({count} — {count/dismissals.sum()*100:.1f}%)'
                 for name, count in dismissals.items()]
ax6.legend(wedges, legend_labels, title='Dismissal Type',
           loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
plt.tight_layout()
st.pyplot(fig6)
plt.close()

# Raw data
st.divider()
if st.checkbox("Show Raw Data"):
    st.dataframe(df.head(50))

st.write("*Python · Pandas · Matplotlib · Streamlit*")