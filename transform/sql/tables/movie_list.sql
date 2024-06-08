CREATE TABLE IF NOT EXISTS movie_list (
    movie_id       INTEGER PRIMARY KEY,
    is_movie_adult BOOLEAN
);

CREATE INDEX idx_movie_id on movie_list(movie_id);

COMMENT ON COLUMN movie_list.movie_id IS 'TMDB movie ID';
COMMENT ON COLUMN movie_list.is_movie_adult IS 'True if movie for adult or not';
COMMENT ON TABLE movie_list IS 'This table contains the list of movies and wether they are for adult or not';