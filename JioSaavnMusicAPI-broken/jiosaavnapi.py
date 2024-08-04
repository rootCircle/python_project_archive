import time
import jiosaavn
import os
from traceback import print_exc

def search(query=None, lyrics_='false', songdata_='true'):
    lyrics = False
    songdata = True
    if lyrics_ and lyrics_.lower()!='false':
        lyrics = True
    if songdata_ and songdata_.lower()!='true':
        songdata = False
    if query:
        return jiosaavn.search_for_song(query, lyrics, songdata)
    else:
        error = {
            "status": False,
            "error":'Query is required to search songs!'
        }
        return error


def get_song(id=None, lyrics_='false'):
    lyrics = False
    if lyrics_ and lyrics_.lower()!='false':
        lyrics = True
    if id:
        resp = jiosaavn.get_song(id,lyrics)
        if not resp:
            error = {
                "status": False,
                "error": 'Invalid Song ID received!'
            }
            return error
        else:
            return resp
    else:
        error = {
            "status": False,
            "error": 'Song ID is required to get a song!'
        }
        return error


def playlist(playlistLink=None, lyrics_='false'):
    lyrics = False

    if lyrics_ and lyrics_.lower()!='false':
        lyrics = True
    if playlistLink:
        id = jiosaavn.get_playlist_id(playlistLink)
        songs = jiosaavn.get_playlist(id,lyrics)
        return songs
    else:
        error = {
            "status": False,
            "error":'Query is required to search playlists!'
        }
        return error


def album(albumLink=None, lyrics_='false'):
    lyrics = False
    if lyrics_ and lyrics_.lower()!='false':
        lyrics = True
    if albumLink:
        id = jiosaavn.get_album_id(albumLink)
        songs = jiosaavn.get_album(id,lyrics)
        return songs
    else:
        error = {
            "status": False,
            "error":'Query is required to search albums!'
        }
        return error


def lyrics(query=None):
    if query:
        try:
            if 'http' in query and 'saavn' in query:
                id = jiosaavn.get_song_id(query)
                lyrics = jiosaavn.get_lyrics(id)
            else:
                lyrics = jiosaavn.get_lyrics(query)
            response = {}
            response['status'] = True
            response['lyrics'] = lyrics
            return response
        except Exception as e:
            error = {
            "status": False,
            "error": str(e)
            }
            return error
        
    else:
        error = {
            "status": False,
            "error":'Query containing song link or id is required to fetch lyrics!'
        }
        return error



def result(query=None, lyrics_='false'):
    lyrics = False
    if lyrics_ and lyrics_.lower()!='false':
        lyrics = True

    if query and 'saavn' not in query:
        return jiosaavn.search_for_song(query,lyrics,True)
    try:
        if '/song/' in query:
            print("Song")
            song_id = jiosaavn.get_song_id(query)
            song = jiosaavn.get_song(song_id,lyrics)
            return song

        elif '/album/' in query:
            print("Album")
            id = jiosaavn.get_album_id(query)
            songs = jiosaavn.get_album(id,lyrics)
            return songs

        elif '/playlist/' or '/featured/' in query:
            print("Playlist")
            id = jiosaavn.get_playlist_id(query)
            songs = jiosaavn.get_playlist(id,lyrics)
            return songs

    except Exception as e:
        print_exc()
        error = {
            "status": True,
            "error":str(e)
        }
        return error
    return None

def fancy_result(query=None,lyrics='true'):
    output = result(query,lyrics_=lyrics)
    minimalkeys=['id', 'song', 'album', 'year', 'primary_artists',
                 'featured_artists', 'singers', 'starring', 'language',
                 '320kbps', 'duration', 'image', 'media_url']
    fancy_out=[]
    for terms in output:
        fancy_out.append([terms[key] for key in minimalkeys])

    return fancy_out

if __name__ == '__main__':
    query=input("Enter Search Term or Album/Playlist/Song Link \n")
    # lyrics_=input("Lyrics \ntrue or false\n")
    print(fancy_result(query))
    

