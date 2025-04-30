from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import seaborn as sns

class SocialMediaModel:
    # Beginning of LLM for Palomar Social Media
    _instance = None
    
    def __init__(self):
        self.model = None
        self.dt = None
        self.features = ['is_retweet']
        # We can make this multi-variable but until then we are just judging by favorite count.
        self.target = 'favorite_count'
        # Loading dataset
        self.social_media_data = pd.read_json('twitter_data.json')
        self.properties_df = pd.json_normalize(self.social_media_data['otherPropertiesMap'])
        # self.properties_df['reply_count'] = pd.to_numeric(self.properties_df['reply_count'])
        self.properties_df['favorite_count'] = pd.to_numeric(self.properties_df['favorite_count'])
        # self.properties_df['quote_count'] = pd.to_numeric(self.properties_df['quote_count'])
        # self.properties_df['retweet_count'] = pd.to_numeric(self.properties_df['retweet_count'])
        
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        
    def _clean(self):
        self.properties_df.drop(['CustomFolderName', 'CustomFileName', 
                                 'FileExtensionHandleMethod', 'status_id', 
                                 'owner_screen_name', 'owner_display_name', 
                                 'media_urls'], axis=1, inplace=True)
        media_details_df = pd.json_normalize(self.properties_df['media_details'][0])
        self.properties_df = pd.concat([self.properties_df, media_details_df], axis=1)
        if 'type' not in self.properties_df.columns:
            self.properties_df['type'] = 0
        # Replaces the categoricals of image and video with 1 and 2 respectively. If there is no image or video the value will be set to 0
        self.properties_df['type'] = self.properties_df['type'].map({'image': 1, 'video': 2}).fillna(0)
        self.properties_df['is_retweet'] = self.properties_df['is_retweet'].map({'false': 0, 'true': 1})
        
        onehot = self.encoder.fit_transform(self.properties_df[['tweet_text']]).toarray()
        cols = ['tweet_text_' + str(val) for val in self.encoder.categories_[0]]
        onehot_df = pd.DataFrame(onehot, columns=cols)
        self.properties_df = pd.concat([self.properties_df, onehot_df], axis=1)
        self.properties_df.drop(['tweet_text'], axis=1, inplace=True)
        # Add cols to take place of tweet_text
        self.features.extend(cols)
        self.properties_df.rename(columns={'type': 'media_type'}, inplace=True)
        if 'media_type' not in self.features:
            self.features.append('media_type')
        # Drop empty data as it may cause issues accord to GPT and Mort does it too    
        # self.properties_df.dropna(inplace=True)

    def _train(self):
        X = self.properties_df[self.features]
        y = self.properties_df[self.target]
        
        self.model = LinearRegression()
        
        self.model.fit(X,y)
        # Tfw you have no idea what you coding and just praying
        self.dt = DecisionTreeRegressor()
        self.dt.fit(X, y)
        
    # NO idea what this does, just praying
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        # return the instance, to be used for prediction
        return cls._instance
    
    def predict(self, tweet):
        # Takes the tweet in as a dict
        tweet_df = pd.DataFrame(tweet, index=[0])
        if 'type' not in tweet_df.columns:
            tweet_df['type'] = 0
        tweet_df['type'] = tweet_df['type'].map({'image': 1, 'video': 2}).fillna(0)
        tweet_df.rename(columns={'type': 'media_type'}, inplace=True)
        # Seperation
        tweet_df['is_retweet'] = tweet_df['is_retweet'].map({'false': 0, 'true': 1})
        onehot = self.encoder.transform(tweet_df[['tweet_text']]).toarray()
        cols = ['tweet_text_' + str(val) for val in self.encoder.categories_[0]]
        onehot_df = pd.DataFrame(onehot, columns=cols)
        tweet_df = pd.concat([tweet_df, onehot_df], axis=1)
        tweet_df.drop(['tweet_text'], axis=1, inplace=True)
        # ChatGPT reco
        for col in self.features:
            if col not in tweet_df.columns:
                tweet_df[col] = 0
        tweet_df = tweet_df[self.features]
        # End
        predicted_fav_count = self.model.predict(tweet_df[self.features])[0]
        return predicted_fav_count

def initSocialMedia():
    SocialMediaModel.get_instance()
    
def testSocialMedia():
    tweet= {
        'tweet_text': 'Excited for a new doctor to join us?',
        'is_retweet': 'false',
        'type': None
    }

    socialMediaModel = SocialMediaModel.get_instance()
    probability = socialMediaModel.predict(tweet)
    
    print(f'Value: {probability}')
    
if __name__ == "__main__":
    print(" Begin:", testSocialMedia.__doc__)
    testSocialMedia()