import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# STEP 1 — LOAD DATA
# ─────────────────────────────────────────
df = pd.read_csv("Psl_Complete_Dataset(2016-2024).csv")

print("=" * 45)
print("PSL DATASET LOADED")
print("=" * 45)
print(f"Total deliveries : {len(df):,}")
print(f"Total matches    : {df['match_id'].nunique()}")
print(f"Seasons covered  : {df['season'].min()} to {df['season'].max()}")
print(f"Total teams      : {df['batting_team'].nunique()}")
print(f"Total players    : {df['batter'].nunique()}")


# ─────────────────────────────────────────
# STEP 2 — CLEAN DATA
# ─────────────────────────────────────────
df['extras_type'].fillna('none', inplace=True)
df['player_dismissed'].fillna('not_out', inplace=True)
df['dismissal_kind'].fillna('not_out', inplace=True)
df['fielder'].fillna('none', inplace=True)
df['date'] = pd.to_datetime(df['date'])

# is_wicket is True/False — convert to 1/0 for easy counting
df['is_wicket'] = df['is_wicket'].astype(int)

print("\nData cleaned successfully. No missing values remaining.")


# ─────────────────────────────────────────
# QUESTION 1 — Which team won the most?
# ─────────────────────────────────────────
print("\n--- Q1: Team Wins ---")

# Each match has same winner repeated on every ball
# So we get unique matches first then count wins
match_winners = df.drop_duplicates(subset='match_id')[['match_id', 'winner']]
wins = match_winners['winner'].value_counts()

print(wins)

plt.figure(figsize=(10, 5))
colors = ['#f43f5e','#a78bfa','#38bdf8','#34d399','#fbbf24','#fb923c']
bars = plt.bar(wins.index, wins.values, color=colors, edgecolor='#0e0e1a', width=0.5)

for bar, val in zip(bars, wins.values):
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.3,
             str(val), ha='center', fontsize=11, fontweight='bold')

plt.title('Which PSL Team Won the Most Matches? (2016-2024)',
          fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Team')
plt.ylabel('Number of Wins')
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig('q1_team_wins.png', dpi=150)
plt.show()
print("Chart saved: q1_team_wins.png")


# ─────────────────────────────────────────
# QUESTION 2 — Top 10 run scorers
# ─────────────────────────────────────────
print("\n--- Q2: Top Run Scorers ---")

top_batters = (df.groupby('batter')['batsman_runs']
               .sum()
               .sort_values(ascending=False)
               .head(10))

print(top_batters)

plt.figure(figsize=(10, 5))
bars = plt.barh(top_batters.index[::-1],
                top_batters.values[::-1],
                color='#a78bfa', edgecolor='#0e0e1a')

for bar, val in zip(bars, top_batters.values[::-1]):
    plt.text(bar.get_width() + 20,
             bar.get_y() + bar.get_height()/2,
             str(val), va='center', fontsize=10, fontweight='bold')

plt.title('Top 10 Run Scorers in PSL History',
          fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Total Runs Scored')
plt.tight_layout()
plt.savefig('q2_top_batters.png', dpi=150)
plt.show()
print("Chart saved: q2_top_batters.png")


# ─────────────────────────────────────────
# QUESTION 3 — Top 10 wicket takers
# ─────────────────────────────────────────
print("\n--- Q3: Top Wicket Takers ---")

top_bowlers = (df[df['is_wicket'] == 1]
               .groupby('bowler')['is_wicket']
               .count()
               .sort_values(ascending=False)
               .head(10))

print(top_bowlers)

plt.figure(figsize=(10, 5))
bars = plt.barh(top_bowlers.index[::-1],
                top_bowlers.values[::-1],
                color='#f43f5e', edgecolor='#0e0e1a')

for bar, val in zip(bars, top_bowlers.values[::-1]):
    plt.text(bar.get_width() + 0.3,
             bar.get_y() + bar.get_height()/2,
             str(val), va='center', fontsize=10, fontweight='bold')

plt.title('Top 10 Wicket Takers in PSL History',
          fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Total Wickets Taken')
plt.tight_layout()
plt.savefig('q3_top_bowlers.png', dpi=150)
plt.show()
print("Chart saved: q3_top_bowlers.png")


# ─────────────────────────────────────────
# QUESTION 4 — Which venue hosted the most?
# ─────────────────────────────────────────
print("\n--- Q4: Top Venues ---")

venues = (df.drop_duplicates(subset='match_id')
          .groupby('venue')['match_id']
          .count()
          .sort_values(ascending=False)
          .head(8))

print(venues)

plt.figure(figsize=(11, 5))
bars = plt.bar(venues.index, venues.values,
               color='#38bdf8', edgecolor='#0e0e1a', width=0.5)

for bar, val in zip(bars, venues.values):
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.2,
             str(val), ha='center', fontsize=10, fontweight='bold')

plt.title('Top PSL Venues by Number of Matches Hosted',
          fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Venue')
plt.ylabel('Matches Hosted')
plt.xticks(rotation=25, ha='right')
plt.tight_layout()
plt.savefig('q4_venues.png', dpi=150)
plt.show()
print("Chart saved: q4_venues.png")


# ─────────────────────────────────────────
# QUESTION 5 — Average runs per over
# ─────────────────────────────────────────
print("\n--- Q5: Runs Per Over ---")

over_runs = df.groupby('over')['total_runs'].mean().round(2)

print(over_runs)

plt.figure(figsize=(11, 5))
plt.plot(over_runs.index, over_runs.values,
         marker='o', color='#34d399',
         linewidth=2.5, markersize=7,
         markerfacecolor='white', markeredgewidth=2)
plt.fill_between(over_runs.index, over_runs.values,
                 alpha=0.15, color='#34d399')

plt.title('Average Runs Scored Per Over in PSL',
          fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Over Number')
plt.ylabel('Average Runs')
plt.xticks(range(1, 21))
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('q5_runs_per_over.png', dpi=150)
plt.show()
print("Chart saved: q5_runs_per_over.png")


# ─────────────────────────────────────────
# QUESTION 6 — How do batters get out?
# ─────────────────────────────────────────
print("\n--- Q6: Dismissal Types ---")

dismissals = (df[df['is_wicket'] == 1]
              ['dismissal_kind']
              .value_counts())

print(dismissals)

import matplotlib.cm as cm
colors = [cm.tab20(i / max(len(dismissals), 1)) for i in range(len(dismissals))]

# Only print a % label ON the slice if it's big enough to hold text.
# Tiny slices (e.g. "hit wicket", "obstructing the field") get their
# name + % moved into a side legend instead, so nothing overlaps.
def autopct_if_big(pct):
    return f'{pct:.1f}%' if pct >= 3 else ''

plt.figure(figsize=(10, 7))
wedges, _, _ = plt.pie(dismissals.values,
        labels=None,
        autopct=autopct_if_big,
        pctdistance=0.75,
        colors=colors,
        wedgeprops={'edgecolor': '#0e0e1a', 'linewidth': 2},
        textprops={'fontsize': 11, 'fontweight': 'bold', 'color': 'white'})

legend_labels = [f'{name} ({count} — {count/dismissals.sum()*100:.1f}%)'
                 for name, count in dismissals.items()]
plt.legend(wedges, legend_labels,
           title='Dismissal Type',
           loc='center left',
           bbox_to_anchor=(1, 0, 0.5, 1),
           fontsize=10)

plt.title('Most Common Ways of Getting Out in PSL',
          fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig('q6_dismissals.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved: q6_dismissals.png")


# ─────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────
print("\n" + "=" * 45)
print("ANALYSIS COMPLETE — KEY FINDINGS")
print("=" * 45)

match_winners = df.drop_duplicates(subset='match_id')
most_wins = match_winners['winner'].value_counts()
print(f"Most titles       : {most_wins.index[0]} ({most_wins.iloc[0]} wins)")

top_batter = df.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False)
print(f"Top run scorer    : {top_batter.index[0]} ({top_batter.iloc[0]} runs)")

top_bowler = (df[df['is_wicket']==1]
              .groupby('bowler')['is_wicket']
              .count()
              .sort_values(ascending=False))
print(f"Top wicket taker  : {top_bowler.index[0]} ({top_bowler.iloc[0]} wickets)")

print(f"Total sixes       : {(df['batsman_runs'] == 6).sum():,}")
print(f"Total fours       : {(df['batsman_runs'] == 4).sum():,}")
print(f"Total wickets     : {df['is_wicket'].sum():,}")
print("=" * 45)