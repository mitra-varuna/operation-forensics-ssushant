from models import OpSummary


def all_articles():
    return OpSummary.get_today_articles().fetch()
