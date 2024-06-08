CREATE OR REPLACE FUNCTION get_movie_ids(force_update BOOLEAN)
RETURNS INTEGER[] AS $$
DECLARE
    movie_ids INTEGER[];
BEGIN
    IF force_update THEN
        SELECT ARRAY(SELECT movie_id FROM public.movie_list)
        INTO movie_ids;
    ELSE
        SELECT ARRAY(
            SELECT movie_id 
            FROM public.movie_list 
            EXCEPT 
            SELECT movie_id 
            FROM public.movies_info
        )
        INTO movie_ids;
    END IF;

    RETURN movie_ids;
END;
$$ LANGUAGE plpgsql;
