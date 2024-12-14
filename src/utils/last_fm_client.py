import httpx
from bs4 import BeautifulSoup

class LastFMWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://ws.audioscrobbler.com/2.0/"
        
        
    def search_track(self, track_name, artist_name=''):
        params = {
            'method': 'track.search',
            'track': track_name,
            'api_key': self.api_key,
            'format': 'json'
        }
        if artist_name:
            params['artist'] = artist_name
        
        response = httpx.get(self.base_url, params=params)
        response.raise_for_status()
        
        # Return only the first result
        if len(response.json()['results']['trackmatches']['track']) == 0:
            return None
        else:
            return response.json()['results']['trackmatches']['track'][0]
    
    def get_youtube_link(self, track_url):
        print(track_url)
        # Scrap the YouTube link from the track URL (a class: play-this-track-playlink play-this-track-playlink--youtube)
        response = httpx.get(track_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        youtube_link = soup.find('a', class_='play-this-track-playlink--youtube')
        if youtube_link:
            return youtube_link['href']
        else:
            return None
        
    def get_youtube_link_id(self, track_url):
        return self.get_youtube_link(track_url).split('=')[-1]
    
    def get_similar_tracks(self, track_url):
        # Scrap the ol list with this class: track-similar-tracks
        response = httpx.get(track_url)
        while response.status_code == 301:
            response = httpx.get(response.headers['Location'])
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        similar_tracks = soup.find('ol', class_='track-similar-tracks')
        
        similar_tracks_list = []
        for track in similar_tracks.find_all('h3', class_='track-similar-tracks-item-name'):
            track_name_tag = track.find('a', class_='link-block-target')
            if track_name_tag:
                track_name = track_name_tag.text
                track_url = track_name_tag['href']
                similar_tracks_list.append({'name': track_name, 'url': track_url, 'youtube_url': self.get_youtube_link(track_url)})
        return similar_tracks_list
