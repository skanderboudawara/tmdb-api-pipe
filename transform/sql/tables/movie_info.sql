CREATE TABLE IF NOT EXISTS movies_info (
    movie_id       INTEGER PRIMARY KEY,
    genres         VARCHAR[],
    imdb_id        VARCHAR,
    original_title VARCHAR,
    overview       TEXT,
    popularity     FLOAT,
    runtime        INTEGER,
    budget         BIGINT,
    revenue        BIGINT,
    release_date   DATE,
    status         VARCHAR,
    vote_average   FLOAT,
    vote_count     INTEGER
);

CREATE INDEX idx_movie_info_id on movies_info(movie_id);

COMMENT ON COLUMN movies_info.movie_id       IS 'Movie Id';
COMMENT ON COLUMN movies_info.genres         IS 'Movies Genra';
COMMENT ON COLUMN movies_info.imdb_id        IS 'Imdb Id';
COMMENT ON COLUMN movies_info.original_title IS 'Original Movie Title';
COMMENT ON COLUMN movies_info.overview       IS 'Movie description';
COMMENT ON COLUMN movies_info.popularity     IS 'Movie Popularity';
COMMENT ON COLUMN movies_info.runtime        IS 'Movie RunTime';
COMMENT ON COLUMN movies_info.budget         IS 'Movie Budget';
COMMENT ON COLUMN movies_info.revenue        IS 'Movie Revenue';
COMMENT ON COLUMN movies_info.release_date   IS 'Movie Release Date';
COMMENT ON COLUMN movies_info.status         IS 'Movie Status';
COMMENT ON COLUMN movies_info.vote_average   IS 'Movie Vote Average';
COMMENT ON COLUMN movies_info.vote_count     IS 'Movie Vote Count';
COMMENT ON TABLE movies_info                 IS 'This table contains the necessary information of a movie';