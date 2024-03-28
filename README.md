# PiHole Analytics
## About
PiHole is great, but the UI's analytic capability can be a tad lacking. This project aims to provide advanced analytics on PiHole's underlying database. 

Currently this is just an exploratory research project, for fun. Feel free to contribute.  
# How To
- git clone the repo.
- copy /etc/pihole/pihole-FTL.db into /pihole_analytics
- presuming you have poetry installed already, run `poetry install` at the project's root directory.
- run `python -m pihole_analytics.app` to spin up the dev server.
# ToDo / Features
## Logging
- add logger to each page/component.
## Pages
### Analytics Page
- Accordion|dropdown|or some equivalent for following figures
    - uncommon DNS queries
    - baseline of registry date for frequented domains, capture queries outside of threshold.
    - entropy analysis 
    - n-gram analysis 
    - frequency analysis
    - Pearson's | Spearman's Correlation between domains
- #### References
    - https://machinelearningmastery.com/how-to-use-correlation-to-understand-the-relationship-between-variables/
    - https://machinelearningmastery.com/gentle-introduction-autocorrelation-partial-autocorrelation/
    - https://d3fend.mitre.org/technique/d3f:DNSTrafficAnalysis/
    - https://arxiv.org/abs/1611.00791
    - https://techfirst.medium.com/correlation-analysis-in-time-series-7c18a88d27a9
### FTLDNS Browser Page
 - Fix the Calendar CSS. DARKLY for life.
 - Add input component for custom queries?
 - Add buttons for .csv export
 - share button via Dash App State?
- #### References
    - https://dash.plotly.com/urls#example-2:-serializing-the-app-state-in-the-url-hash

### Deployment
- write compose stacks for:
    - dash app
    - dash app, pihole
    - dash app, pihole, rProxy, auto certs, gunicorn?
- Add options for ENV vars to set FTLDNS path.
    - Looks like there may be an issue that stems from reading the db while pihole is running.
        - COPY statement in the Dockerfile won't work, due to hash of db changing while building image.
        - Bind mount creates an issue with the container not being able to read from the DB. Possibly a permissions issue?
        - For now, I just manually copied the pihole-FTL.db into the /pihole_analytics dir for dev. Better workaround would be a bash script to cp the db. Final solution should be able to read directly from the db.
- #### References
     - https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
    - https://github.com/orgs/python-poetry/discussions/1879
## Software Stack & References
- python
    - https://www.python.org/
    - https://docs.python.org/3/library/sqlite3.html
- poetry
    - https://python-poetry.org/docs/
- Plotly Dash
    - https://dash.plotly.com/urls
    - https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/
    - https://dash.plotly.com/dash-ag-grid
    - https://dash-bootstrap-components.opensource.faculty.ai/
- pandas
    - https://pandas.pydata.org/docs/git
- git
    - https://git-scm.com/
- docker compose
    - https://docs.docker.com/compose/
- pihole
    - https://docs.pi-hole.net/database/ftl/#example-for-interaction-with-the-long-term-query-database
