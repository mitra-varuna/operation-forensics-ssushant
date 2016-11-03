import datetime

from models import OpSummary


def all_articles():
    return [f.to_dict(exclude=['date']) for f in OpSummary.query(OpSummary.when == datetime.date.today()).fetch(
        projection=[OpSummary.summary, OpSummary.url, OpSummary.polarity, OpSummary.magnitude])]
