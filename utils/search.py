def search_transcript(transcript, query):
    sentences = transcript.split(".")

    results = []

    for sentence in sentences:
        if query.lower() in sentence.lower():
            results.append(sentence.strip())

    return results