import pandas as pd

df = pd.read_json('twitter_data.json')

properties_df = pd.json_normalize(df['otherPropertiesMap'])

media_details_df = pd.json_normalize(properties_df['media_details'][0])

# media_details_df['type'] = media_details_df['type'].map({'image': 1, 'video': 2})

df = pd.concat([df, properties_df], axis=1)
df = pd.concat([df, media_details_df], axis=1)
df['type'] = df['type'].map({'image': 1, 'video': 2}).fillna(0)

# sorted_df = df.sort_values(by='favorite_count', ascending=False)

# print(sorted_df[['reply_count', 'favorite_count', 'otherPropertiesMap']])

# print(media_details_df['type'])

print(properties_df['media_details'].str.len())
print(df[['type']])