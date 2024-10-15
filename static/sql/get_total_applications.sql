
WITH DateSeries AS (
    SELECT generate_series(
        current_date - interval '6 days',
        current_date,
        '1 day'::interval
    )::date AS date
),
 all_rows as (
select cast(application_date as date) application_date,count(1) totals from "Applications"
where "Applications".user_id = %s and date(application_date) between current_date - interval '7' day and current_date
group  by application_date 

)
SELECT
    cast(ds.date as varchar),
    coalesce(all_rows.totals,0) AS counter
FROM
    DateSeries ds
LEFT JOIN
    all_rows 
ON
    ds.date = all_rows .application_date

GROUP BY
    1,2
ORDER BY
    1