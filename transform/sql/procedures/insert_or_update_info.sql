CREATE OR REPLACE PROCEDURE insert_or_update_movie_info(
    movie_id integer,
    dict_params json,
    force_update boolean
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF force_update THEN
        -- Update the existing row
        UPDATE movies_info
        SET
            genres = COALESCE(
            CASE 
                WHEN dict_params->>'genres' IS NOT NULL THEN array(select json_array_elements_text(dict_params->'genres')) 
                ELSE genres 
            END,
            genres),
            imdb_id = COALESCE(dict_params->>'imdb_id', imdb_id),
            original_title = COALESCE(dict_params->>'original_title', original_title),
            overview = COALESCE(dict_params->>'overview', overview),
            popularity = COALESCE((dict_params->>'popularity')::numeric, popularity),
            runtime = COALESCE((dict_params->>'runtime')::integer, runtime),
            budget = COALESCE((dict_params->>'budget')::numeric, budget),
            revenue = COALESCE((dict_params->>'revenue')::numeric, revenue),
            release_date = COALESCE((dict_params->>'release_date')::date, release_date),
            status = COALESCE(dict_params->>'status', status),
            vote_average = COALESCE((dict_params->>'vote_average')::numeric, vote_average),
            vote_count = COALESCE((dict_params->>'vote_count')::integer, vote_count)
        WHERE movie_id = movie_id;
    ELSE
        -- Insert a new row
        INSERT INTO movies_info (
            movie_id, genres, imdb_id, original_title, overview, popularity, runtime,
            budget, revenue, release_date, status, vote_average, vote_count
        )
        VALUES (
            movie_id,
            CASE 
                WHEN dict_params->>'genres' IS NOT NULL THEN array(select json_array_elements_text(dict_params->'genres')) 
                ELSE NULL 
            END,
            dict_params->>'imdb_id',
            dict_params->>'original_title',
            dict_params->>'overview',
            (dict_params->>'popularity')::numeric,
            (dict_params->>'runtime')::integer,
            (dict_params->>'budget')::numeric,
            (dict_params->>'revenue')::numeric,
            (dict_params->>'release_date')::date,
            dict_params->>'status',
            (dict_params->>'vote_average')::numeric,
            (dict_params->>'vote_count')::integer
        );
    END IF;
END;
$$;
