# tag-music
Simple MP3 file tagging program. Uses yt-dl to download music, itunes api for metadata and librosa for bpm. and 

Itunes API required fields:
    # https://performance-partners.apple.com/search-api
    # term (the api search) [Required]: masgo+drive+long+way
    # country (2 letter country code - Wikipedia IS_3166-1_alpha-2) [Required]: US
    # media (type of media): music
    # entity (type of result returned):
         # returns: [musicArtist, musicTrack, album, musicVideo, mix, song]
    # attribute (search terms): music+[mixTerm, genreIndex, artistTerm, composerTerm, albumTerm, ratingIndex, songTerm]
    # limit (number of searches returned): 1 to 200
    # lang (The language used): en_us [Use the 5 letter codename, eg. ja_jp for japanese,, japan]
    # explicit (include explicit content?): default Yes

Itunes API returned fields (## means used):
    # artistId (numeric ID)
    # collectionId (numeric album ID)
    # trackId (numeric track ID)
    ## artistName (Artist)
    ## collectionName (Album)
    ## trackName (Track)
    # collectionCensoredName (Album censored)
    # trackCensoredName (Censored track name)
    # artistViewUrl (Artist link on apple music)
    # collectionViewUrl (Album link on apple music)
    # trackViewUrl (Track link on apple music)
    # previewUrl (Song preview link)
    # artworkUrl30 (artwork - 30x30)
    # artworkUrl60 (artwork - 60x60)
    ## artworkUrl100 (artwork - 100x100)
    # collectionPrice (Album price)
    ## releaseDate (Date released)
    # collectionExplicitness (Album is explicit?)
    # trackEcplicitness (track explicit?)
    ## discCount (Number of discs in album)
    ## discNumber (disc Number of album)
    ## trackNumber (track Number in disc)
    ## trackCount (Number of tracks in disc)
    ## trackTimeMillis (Track length in milliseconds)
    ## country (Country of origin)
    # currency (Price currency)
    ## primaryGenreName (primary genre)
    # isStreamable (is it streamable?)