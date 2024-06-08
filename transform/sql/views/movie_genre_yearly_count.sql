CREATE OR REPLACE VIEW movie_genre_yearly_count AS
SELECT
    EXTRACT(YEAR FROM release_date) AS year,
    genre,
    COUNT(*) AS movie_count
FROM
    movies_info,
    unnest(genres) AS genre
WHERE
    EXTRACT(YEAR FROM release_date) IS NOT NULL
    AND genre IS NOT NULL
GROUP BY
    year,
    genre
ORDER BY
    year DESC,
    genre;
