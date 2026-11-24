import pandas as pd

# Load raw Kaggle dataset
df = pd.read_csv('nytcrosswordsdata.csv', encoding='latin1').dropna(subset=['Date', 'Word', 'Clue'])
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])

# Derive temporal & length attributes
df['Year'] = df['Date'].dt.year
df = df[(df['Year'] >= 1993) & (df['Year'] <= 2021)]
df['Decade'] = (df['Year'] // 10) * 10
df['Weekday'] = df['Date'].dt.day_name()
df['Word_Len'] = df['Word'].astype(str).str.len()
df['Clue_Len'] = df['Clue'].astype(str).str.len()

# Export aggregated summaries for D3 frontend
df.groupby(['Decade', 'Weekday'])[['Word_Len', 'Clue_Len']].mean().round(2).to_csv('weekday_decade_summary.csv')
df.groupby('Year')[['Word_Len', 'Clue_Len']].mean().round(2).to_csv('yearly_trends.csv')
df['Word'].value_counts().head(100).to_csv('top_words.csv')