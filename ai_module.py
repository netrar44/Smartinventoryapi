from textblob import TextBlob
 
# Function to analyze the sentiment of a text
POSITIVE_WORDS = {"amazing", "best", "excellent", "good", "great", "happy", "love", "wonderful"}
NEGATIVE_WORDS = {"awful", "bad", "hate", "horrible", "poor", "sad", "terrible", "worst"}
 
 
def analyze_feedback(text):
    words = [word.strip(".,!?;:").lower() for word in text.split()]
    scores = [1 if word in POSITIVE_WORDS else -1
              for word in words
              if word in POSITIVE_WORDS or word in NEGATIVE_WORDS]
    sentiment = sum(scores) / len(scores) if scores else 0
    return round(sentiment, 2)