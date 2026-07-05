import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        label = ent.label_

        # Simple correction
        if label == "PRODUCT" and "my name is" in text.lower():
            if ent.start_char > text.lower().find("my name is"):
                label = "PERSON"

        entities.append({
            "text": ent.text,
            "label": label
        })

    return entities