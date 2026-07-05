def generate_report(result):
    report = f"""
==============================
 Customer Support AI Report
==============================

Transcript:
{result['transcript']}

--------------------------------

Sentiment:
Label : {result['sentiment']['label']}
Confidence : {result['sentiment']['score']:.2f}

--------------------------------

Entities:
"""

    for entity in result["entities"]:
        report += f"- {entity['text']} ({entity['label']})\n"

    return report