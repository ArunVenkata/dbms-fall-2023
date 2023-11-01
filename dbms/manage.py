#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
# from django.db import connection

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dbms.settings')
    try:
        from django.core.management import execute_from_command_line
        #
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT * FROM course")
        #     results = cursor.fetchall()
        #
        # print(results)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

# from django.db import connection
#
# # 执行原始 SQL 查询
# with connection.cursor() as cursor:
#     cursor.execute("SELECT * FROM hw1_course")
#
#     # 获取查询结果
#     results = cursor.fetchall()
#
# # 打印结果
# for row in results:
#     print(f"Course ID: {row[0]}")
#     print(f"Course Name: {row[1]}")
#     print(f"Course Description: {row[2]")