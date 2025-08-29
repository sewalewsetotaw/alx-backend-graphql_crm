# crm/tasks.py
from celery import shared_task
import requests
from datetime import datetime

GRAPHQL_URL = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/crm_report_log.txt"


@shared_task
def generate_crm_report():
    """
    Celery task to generate a CRM report by querying the GraphQL API.
    Logs the number of customers, orders, and total revenue to a file.
    """

    query = """
    query {
        allCustomers {
            totalCount
        }
        allOrders {
            totalCount
            edges {
                node {
                    totalAmount
                }
            }
        }
    }
    """

    try:
        # Send request to GraphQL endpoint
        response = requests.post(GRAPHQL_URL, json={'query': query})
        response.raise_for_status()  # raise exception if request failed
        data = response.json().get('data', {})

        # Extract customers count
        total_customers = data.get('allCustomers', {}).get('totalCount', 0)

        # Extract orders and revenue
        orders_data = data.get('allOrders', {})
        total_orders = orders_data.get('totalCount', 0)
        total_revenue = sum(
            float(edge['node']['totalAmount']) for edge in orders_data.get('edges', [])
        )

        # Log success
        log_msg = (
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Report: "
            f"{total_customers} customers, {total_orders} orders, "
            f"{total_revenue:.2f} revenue\n"
        )
        with open(LOG_FILE, "a") as f:
            f.write(log_msg)

    except Exception as e:
        # Log failure
        error_msg = (
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
            f"Failed to generate report: {e}\n"
        )
        with open(LOG_FILE, "a") as f:
            f.write(error_msg)