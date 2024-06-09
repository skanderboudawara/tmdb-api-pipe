CREATE TABLE IF NOT EXISTS movie_list (
    movie_id       INTEGER PRIMARY KEY,
    is_movie_adult BOOLEAN
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_indexes
        WHERE indexname = 'idx_movie_id'
        AND tablename = 'movie_list'
    ) THEN
        CREATE INDEX idx_movie_id ON movie_list(movie_id);
    END IF;
END $$;


COMMENT ON COLUMN movie_list.movie_id IS 'TMDB movie ID';
COMMENT ON COLUMN movie_list.is_movie_adult IS 'True if movie for adult or not';
COMMENT ON TABLE movie_list IS 'This table contains the list of movies and wether they are for adult or not';