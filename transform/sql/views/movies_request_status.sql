CREATE VIEW movie_status_view AS
SELECT
    ml.movie_id,
    CASE
        WHEN mi.movie_id IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS is_request_successful
FROM
    movie_list ml
LEFT JOIN
    movies_info mi ON ml.movie_id = mi.movie_id;
