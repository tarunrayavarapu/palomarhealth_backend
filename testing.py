import pandas as pd

df = pd.read_json('twitter_data.json')

properties_df = pd.json_normalize(df['otherPropertiesMap'])

properties_df['reply_count'] = pd.to_numeric(properties_df['reply_count'])

df = pd.concat([df, properties_df], axis=1)

sorted_df = df.sort_values(by='reply_count', ascending=False)

print(sorted_df[['reply_count', 'otherPropertiesMap']])