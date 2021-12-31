import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns

consumerKey = 'bYGkegpyYHkt3i3bEP5kATj0P'
consumerSecret = 'jZKYSXh3uAuVx16VohKtyd2IbwrJBAzTIiXIpPC4nBDAcgE2qY'
accessToken = '2467440198-RfjVxK0054l6qZCAj7tEIkewFGgPbAsVOqWwb5Q'
accessTokenSecret = 'K7PdN05ulegk5fEjLADpm8YIFhnoQWL5tTOJwcId6MJmA'

#Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret) 
# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True)


def main():
    
    html_temp = """ 
    <div style="background-color:#5858FA; padding:0.1xpx">
        <h2 style="color:white; text-align: center;">Tweet Sentimental Analyser App with Streamlit</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    image = Image.open('banner.jpg')
    st.image(image,use_column_width=True)
    st.title("Tweet Sentiment Analyzer🔥")
    options = ["About this App","Tweet Analysis","Generate twitter data"]
    choice = st.sidebar.selectbox("Select the Activity 👇!!", options)

    if choice == "About this App":
        st.subheader("Analyze the tweets of your favourite Topics and Trends!!")
        st.subheader("This App perfoms the following activities")
        st.write("### A. Tweet Analysis:\n 1. Fetch the top 5 tweets on given trend/topic. \n 2. Word cloud generation. \n 3. Visualize the sentiment analysis through graph")
        st.write("### B. Generate tweet data:\n1. Get the most liked tweet. \n2. Get the most liked re-tweet. \n3. Display the dataframe of tweets and cleaned form")
        st.subheader("Powered by Streamlit & Heroku !!")

    elif choice == "Tweet Analysis":
        raw_text = st.text_area("Your query goes here...")
        Analyzer_choice = st.selectbox("Select the Activities",  ["Show Top 5 recent Tweets","Generate WordCloud" ,"Visualize the Sentiment Analysis"])
        if st.button("Analyze"):
            if Analyzer_choice == "Show Top 5 recent Tweets":
                st.success("Fetching the top 5 recent tweets")
                def stream_tweets(raw_text):
                    posts = api.search(raw_text, count=10, lang='en', exclude='retweets',tweet_mode='extended')
                    def get_tweets():
                        i=0
                        l=[]
                        for tweet in posts[:5]:
                            l.append(tweet.full_text)
                            i += 1
                        return l
                    recent_tweets = get_tweets()
                    return recent_tweets
                recent_tweets = stream_tweets(raw_text)
                st.write(recent_tweets)
            
            elif Analyzer_choice == "Generate WordCloud":
                st.success("Generating word cloud!")
                def generate_wordcloud():
                    posts = api.search(raw_text, count=10, lang='en', exclude='retweets',tweet_mode='extended')
                    df = pd.DataFrame([tweet.full_text for tweet in posts], columns = ['Tweets'])
                    allWords = ' '.join([twts for twts in df['Tweets']])
                    wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
                    plt.imshow(wordCloud, interpolation="bilinear")
                    plt.axis('off')
                    plt.savefig('WC.jpg')
                    img= Image.open("WC.jpg")
                    return img

                img=generate_wordcloud()
                st.image(img)

            else:
                def Plot_Analysis():
                    st.success("Generating Visualisation for Sentiment Analysis")
                    posts = api.search(raw_text, count=10, lang='en', exclude='retweets',tweet_mode='extended')
                    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

                    def clean_tweet(tweet):
                        return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)',' ', tweet).split())

                    df['Tweets'] = df['Tweets'].apply(clean_tweet)
                    def getSubjectivity(text):
                        return TextBlob(text).sentiment.subjectivity
                    def getPolarity(text):
                        return  TextBlob(text).sentiment.polarity
                    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
                    df['Polarity'] = df['Tweets'].apply(getPolarity)

                    def analyze_tweet(score):
                        if score < 0:
                            return 'Negative'
                        elif score == 0:
                            return 'Neutral'
                        else:
                            return 'Positive'
                    df['Analysis'] = df['Polarity'].apply(analyze_tweet)

                    return df

                df = Plot_Analysis()
                st.write(sns.countplot(x=df['Analysis'],data=df))
                plt.xlabel("Tweet Sentiment")
                plt.ylabel("Count")
                st.pyplot(use_container_width=True)

    else:
        raw_text = st.text_area("Your query goes here...")
        generate_options = st.selectbox("Select the Activities",  ["Most liked tweet","Most retweeted tweet" ,"Get cleaned text tweets"])
        if st.button("Generate"):
            if generate_options == "Most liked tweet":
                st.success("Fetching the most liked tweet")
                def get_data(raw_text):
                    posts = api.search(raw_text, count = 100, lang ="en", tweet_mode="extended")
                    df = pd.DataFrame([[tweet.full_text, tweet.id, tweet.favorite_count, tweet.retweet_count] for tweet in posts], columns=['Tweets','ID','fav_count','rt_count'])

                    def clean_tweet(tweet):
                        return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)',' ', tweet).split())

                    df['cleaned_tweets'] = df['Tweets'].apply(clean_tweet)
                    return df

                df=get_data(raw_text)
                max_fav = df['fav_count'].max()
                st.write("Most liked tweet is:\n")
                st.write(df[df['fav_count'] == max_fav]['Tweets'])

            elif generate_options == "Most retweeted tweet":
                st.success("Fetching the most retweeted tweet")
                def get_data(raw_text):
                    posts = api.search(raw_text, count = 100, lang ="en", tweet_mode="extended")
                    df = pd.DataFrame([[tweet.full_text, tweet.id, tweet.favorite_count, tweet.retweet_count] for tweet in posts], columns=['Tweets','ID','fav_count','rt_count'])

                    def clean_tweet(tweet):
                        return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)',' ', tweet).split())

                    df['cleaned_tweets'] = df['Tweets'].apply(clean_tweet)
                    return df

                df=get_data(raw_text)
                max_rt = df['rt_count'].max()
                st.write("Most retweeted tweet is:\n")
                st.write(df[df['rt_count'] == max_rt]['Tweets'])

            else:
                st.success("Fetching the last 100 tweets and cleaned texts")
                def get_data(raw_text):
                    posts = api.search(raw_text, count = 100, lang ="en", tweet_mode="extended")
                    df = pd.DataFrame([[tweet.full_text] for tweet in posts], columns=['Tweets'])

                    def clean_tweet(tweet):
                        return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)',' ', tweet).split())

                    df['cleaned_tweets'] = df['Tweets'].apply(clean_tweet)
                    return df

                df = get_data(raw_text)
                st.write(df)
    
if __name__ == "__main__":
	main()
