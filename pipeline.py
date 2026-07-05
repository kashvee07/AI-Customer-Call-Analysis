from utils.speech import transcribe_audio
from utils.sentiment import analyze_sentiment
from utils.ner import extract_entities


def analyze_customer_call(audio_path):
    try:
        transcript = transcribe_audio(audio_path)

        sentiment = analyze_sentiment(transcript)

        entities = extract_entities(transcript)

        return {
            "success": True,
            "transcript": transcript,
            "sentiment": sentiment,
            "entities": entities
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }