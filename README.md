# General election in Denmark (Folketingsvalg) - Geographical dispersion
Geographical dispersion at the general election 2026 in Denmark: IGS - Indeks for Geographical Skewness

Are we as voters clustering into more segmented groups geographically across constituencies? 

The question arises when elections are coming up. Also, at the most recent election in March 2026. The answer is 'yes'. But only approximately only as much as in previos elections. The current analysis uses the gini-approach, described in a LinkedIn-post  (in Danish, but an English version is to be found in this rep)
https://www.linkedin.com/feed/update/urn:li:activity:7444483789684256768/

Analysis is done with 2 files:
1) HTML-data for the analysis is scraped from official site with info on voting (Constituencies-scraping.py).
2) Parsing and calculations (Constituencies-parsing.py).

Both python-files are available in the rep along with results described in more detail and illustrations. 

A question came about related to the party splits. In particular one of the old parties Venstre lost some leading politicians who founded new parties. Question is whether the sum of votes for these parties are as geographically skewed/unskewed as the old party was before the splits. The chart 'Old and new parties.png' indicates an answer, not a clear cut one though. Write me for further explanation, code to do the calculations or whatever comes to mind raising question about.
