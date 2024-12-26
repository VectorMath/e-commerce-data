--Incoming products quantity--
SELECT
date,
row_count,
SUM(row_count) OVER(ORDER BY date) as cum_products_sum
FROM (
	SELECT date, COUNT(*) AS row_count
	FROM public.products
	GROUP BY date
) AS agg_table
ORDER BY date;

--General information about current price--
SELECT
t1.date,
t1.made_in AS country,
t1.subj_root_name as main_category,
t2.price
FROM public.products AS t1
LEFT JOIN public.price AS t2
ON t1.product_id = t2.product_id
WHERE t2.price IS NOT NULL

--General information about price history--
SELECT
t2.date,
t1.made_in AS country,
t1.subj_root_name as main_category,
t2.price
FROM public.products AS t1
LEFT JOIN public.price_history AS t2
ON t1.product_id = t2.product_id
WHERE t2.price IS NOT NULL

--General information about feedbacks--
SELECT
t1.made_in AS country,
t1.subj_root_name AS main_category,
t2.grade,
CASE
    WHEN t2.grade >= 4 THEN 1
    ELSE 0
END AS is_good_feedback
FROM public.products AS t1
LEFT JOIN public.feedbacks AS t2
ON t1.product_id = t2.product_id
AND t1.root_id = t2.root_id

SELECT
t1.made_in AS country,
t1.subj_root_name AS main_category,
t2.mean_grade,
t2.mean_grade_filtered
FROM public.products AS t1
LEFT JOIN public.grade_history AS t2
ON t1.product_id = t2.product_id