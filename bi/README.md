# BI part of project

Folder **bi** contains Microsoft Power BI presentation with report-analyse. All data was taken from database **e_commerce**

## Files

 * [**queries.sql**](queries.sql) - File that contain SQL queries for creating tables that using in presentation.

 * [**report-analys.pbix**](report-analys.pbix) - Power BI file with presentation.


## Slides from BI-file

### Incoming products quantity

Slide that shows us a chart with the frequency of daily product arrivals in the database, along with some brief analytical information, such as the average number of products added daily, etc.

<p align="center">
  <img src=../docs/bi/incoming_products.png alt="incoming_products">
</p>

SQL that using in this slide:

```sql
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
```

### General information about products

Slide that show us what kind of products do we have in database, that group by category/country

<p align="center">
  <img src=../docs/bi/general_products_1.png alt="general_products_1">
</p>

<p align="center">
  <img src=../docs/bi/general_products_2.png alt="general_products_2">
</p>

### General information about current price

Slide that show us general information about current price for products by country and category.

<p align="center">
  <img src=../docs/bi/general_curr_price_1.png alt="general_curr_price_1">
</p>

<p align="center">
  <img src=../docs/bi/general_curr_price_2.png alt="general_curr_price_2">
</p>

SQL that using in this slide:

```sql
SELECT
t1.date,
t1.made_in AS country,
t1.subj_root_name as main_category,
t2.price
FROM public.products AS t1
LEFT JOIN public.price AS t2
ON t1.product_id = t2.product_id
WHERE t2.price IS NOT NULL
```

### General information about price history

Slide that show us price history for products by country and category.

<p align="center">
  <img src=../docs/bi/ph_1.png alt="ph_1">
</p>

<p align="center">
  <img src=../docs/bi/ph_2.png alt="ph_2">
</p>

<p align="center">
  <img src=../docs/bi/ph_3.png alt="ph_3">
</p>

```sql
SELECT
t2.date,
t1.made_in AS country,
t1.subj_root_name as main_category,
t2.price
FROM public.products AS t1
LEFT JOIN public.price_history AS t2
ON t1.product_id = t2.product_id
WHERE t2.price IS NOT NULL
```

### General information about feedbacks

Slide that shows us the ratio of good and bad feedbacks (a feedback with a rating of 4 or higher on a 5-point scale is considered good) across countries and categories.

There are also tables with two average ratings for products, broken down by country and category.

<p align="center">
  <img src=../docs/bi/feedbacks.png alt="feedbacks">
</p>

SQL that using in this slide:

```sql
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
```

```sql
SELECT
t1.made_in AS country,
t1.subj_root_name AS main_category,
t2.mean_grade,
t2.mean_grade_filtered
FROM public.products AS t1
LEFT JOIN public.grade_history AS t2
ON t1.product_id = t2.product_id
```