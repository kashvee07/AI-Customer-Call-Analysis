from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)


def summarize_text(text):
    if len(text.split()) < 30:
        return text

    summary = summarizer(
        text,
        max_length=50,
        min_length=10,
        do_sample=False
    )

    return summary[0]["summary_text"]