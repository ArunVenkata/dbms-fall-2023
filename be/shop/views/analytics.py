from django.db import connection

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]



def get_aggregate_sales(cursor):
    cursor.execute("""
SELECT
    SUM(sutd.quantity) AS total_sold,
    SUM(sutd.price * sutd.quantity) AS total_sales,
    SUM((sutd.price - sp.original_cost) * sutd.quantity) AS total_profit
FROM
    shop_usertransactiondetails sutd
JOIN
    shop_product sp ON sutd.product_id = sp.id;
""")
    return dictfetchall(cursor)


def get_top_game_categories(cursor):
    cursor.execute("""

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
    """)
    return dictfetchall(cursor)

def region_sales_volume(cursor):
    cursor.execute("""
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
    """)

    return dictfetchall(cursor)


def business_buying_most_products(cursor):
    cursor.execute("""SELECT
    uu."username" AS business_username,
    COUNT(sut.id) AS transaction_count,
    ROUND(AVG(sutd.price * sutd.quantity), 2) AS avg_per_transaction
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
    transaction_count DESC;""")
    return dictfetchall(cursor)


class AnalyticsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
                
        data =  {}
        with connection.cursor() as c:
            data["aggregate_sales"] = get_aggregate_sales(c)
            data["game_categories"] = get_top_game_categories(c)
            data["region_sales_volume"] = region_sales_volume(c)
            data["business_buying_most_products"] = business_buying_most_products(c)
        

        return Response({"data": data})
            