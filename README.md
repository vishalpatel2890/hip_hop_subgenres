# Identifying Subgenres in Hip Hop
 
Hip hop music has been evolving constantly since its inception in the early 1980s. Different styles of rapping and music production have developed through time and have been influenced by many factors including locale, political climate, economics, technology, as well as other pop culture. As a result, music labeled as hip hop is very diverse and the label does very little to inform  the listener. In this analysis, I look to develop imperical metrics of different hip hop songs to use as features for clustering to indentify sub-genres (clusters) of hip hop music that share similar lyrical and musical properties. 

## The Data
 
Lyrical data for every song of for over 150 hip hop artists over the past four decades was scraped from [Genius](http://genius.com). Spotify has developed a series of audio features for every song in their library including danceability, valence, energy, tempo, loudness, speechiness, instrumentalness, liveness, acousticness. Spotify has been these features available through their API and for each song song scraped I collected these features. 
 
After removing duplicates, instrumental songs, skits, and songs which didn't have audio features (because they were not in Spotify's library) I was left with ~25,000 songs for my analysis. 

## Generating Lyrical Features

### Rhyming Score

### Repetitiveness

## EDA 

## Clustering

## Next Steps 

- Expand dataset by scraping/fetching additional songs
  - Set up distributed scraping services using AWS ECS/EC2
  - Schedule service to update for new artists/albums 
- Dashboard to view subsets of data 
- Fine tune clustering and try different algorithms and explore properties of the clusters
 
 
