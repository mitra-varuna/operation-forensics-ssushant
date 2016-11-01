# Index Editorial Application

An [App engine](https://cloud.google.com/appengine/docs) application to index and calculate sentiments of the editorial pages of [The Hindu](http://www.thehindu.com/) Newspaper.
It provides a REST endpoint to get an editorial's sentiment score, entities appearing in the editorial with the Wikipedia Page URL.

```bash
$ gcloud app deploy --project operation-forensics-ssushant app.yaml cron.yaml

```
