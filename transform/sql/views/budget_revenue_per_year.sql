CREATE OR REPLACE VIEW budget_revenue_per_year AS
SELECT
    EXTRACT(YEAR FROM release_date) AS year,
    SUM(budget) AS total_budget,
    SUM(revenue) AS total_revenue,
    SUM(CASE WHEN EXTRACT(YEAR FROM release_date) <= EXTRACT(YEAR FROM CURRENT_DATE)
            THEN revenue - budget
            ELSE 0
    END) AS revenue_budget_difference
FROM
    movies_info
WHERE
    EXTRACT(YEAR FROM release_date) IS NOT NULL 
    AND budget > 0
GROUP BY
    year
ORDER BY
    year DESC;
