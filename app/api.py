from models import OpSummary


def all_articles():
    return [f.to_dict(exclude=['date']) for f in OpSummary.query().fetch(
        projection=[OpSummary.summary, OpSummary.url, OpSummary.polarity, OpSummary.magnitude])]
