# Queries

- aggregate sales and profit of the products

```sql
SELECT
    SUM(sutd.quantity) AS total_sold,
    SUM(sutd.price * sutd.quantity) AS total_sales,
    SUM((sutd.price - sp.original_cost) * sutd.quantity) AS total_profit
FROM
    shop_usertransactiondetails sutd
JOIN
    shop_product sp ON sutd.product_id = sp.id;
```    
   
- TOP GAME CATEGORIES

```sql
SELECT
    category,
    SUM(quantity) AS total_sold
FROM
    shop_usertransactiondetails
GROUP BY
    category
ORDER BY
    total_sold DESC
LIMIT 5;
```

- How do the various regions compare by sales volume
```sql
SELECT
    sr."name" AS region_name,
    SUM(sutd.price * sutd.quantity) AS total_sales
FROM
    shop_usertransactiondetails sutd
JOIN
    shop_usertransaction sut ON sutd.transaction_id = sut.id
JOIN
    shop_product sp ON sutd.product_id = sp.id
JOIN
    shop_store ss ON sp.store_id = ss.id
JOIN
    shop_region sr ON ss.region_id = sr.id
GROUP BY
    sr."name"
ORDER BY
    total_sales DESC;
```
- Which businesses are buying given products the most?

```sql
SELECT
    uu."username" AS business_username,
    COUNT(sut.id) AS transaction_count,
    AVG(sutd.price * sutd.quantity) AS avg_per_transaction
FROM
    shop_usertransaction sut
JOIN
    userauth_user uu ON sut.purchased_by_id = uu.id
JOIN
    shop_usertransactiondetails sutd ON sut.id = sutd.transaction_id
WHERE
    uu.user_type = 'business'
GROUP BY
    uu."username"
ORDER BY
    transaction_count DESC;
```   
   
   
   
   
   
   


