from flask import Flask, render_template, request
from googleapiclient.discovery import build
import googleapiclient.errors
import pandas as pd
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import matplotlib.pyplot as plt

app = Flask(__name__)

DEVELOPER_KEY = "AIzaSyDSYvuwqlepbVvujbmC5nfEF-F5NWpfVRs"
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/You Tube comment_analysis', methods=['POST'])
def comment_analysis():
    video_id = request.form['video_id']

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        )
        response = request.execute()

        comments = []

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])

        df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])
        df.head(10)
        
        # analyzer = SentimentIntensityAnalyzer()

        # sentiment = []
        # for text in df['text']:
        #     score = analyzer.polarity_scores(text)
        #     sentiment.append(score['compound'])
    
        # df['sentiment'] = sentiment
        # pos = (df.sentiment > 0).sum()
        # neg = (df.sentiment < 0).sum() 
        # neu = (df.sentiment == 0).sum()

        # total = len(df)
        
        # pos_pct = round(pos/total*100, 2)
        # neg_pct = round(neg/total*100, 2)  
        # neu_pct = round(neu/total*100, 2)
        
        # sentiment_df = pd.DataFrame({'sentiment': ['Positive', 'Negative', 'Neutral'],'percentage': [pos_pct, neg_pct, neu_pct]})
        
        # fig, ax = plt.subplots()
        # ax.pie(sentiment_df['percentage'], labels=sentiment_df['sentiment'], autopct='%1.1f%%')
        # ax.set_title('Comment Sentiment Analysis')
        
        # plt.savefig('sentiment.png')
        # 'pos_pct': pos_pct 
        # 'neg_pct': neg_pct
        # 'neu_pct': neu_pct
        # 'sentiment_df': sentiment_df.to_dict()
        # 'sentiment_plot': 'sentiment.png'

        
        return df.to_json(orient='records')
    except googleapiclient.errors.HttpError as e:
        return f"An error occurred: {e}", 400

if __name__ == '__main__':
    app.run(debug=True)