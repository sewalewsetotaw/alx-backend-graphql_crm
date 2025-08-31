from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

HEARTBEAT_LOG_FILE = "/tmp/crm_heartbeat_log.txt"
LOW_STOCK_LOG_FILE = "/tmp/low_stock_updates_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"

def log_crm_heartbeat():
    """Append a heartbeat message to the CRM heartbeat log and optionally query GraphQL hello."""
    with open(HEARTBEAT_LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} CRM heartbeat\n")

    # Optional: Query GraphQL hello field
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query {
            hello
        }
        """
    )

    try:
        client.execute(query)
    except Exception:
        pass  # ignore errors if GraphQL is not available

def update_low_stock():
    """Execute the UpdateLowStockProducts mutation and log updated products."""
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql(
        """
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
        """
    )

    try:
        result = client.execute(mutation)
        updated_products = result['updateLowStockProducts']['updatedProducts']
        message = result['updateLowStockProducts']['message']

        log_lines = [
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Updated Products: "
        ]
        for product in updated_products:
            log_lines.append(f"{product['name']} (Stock: {product['stock']})")
        log_lines.append(f"Message: {message}\n")

        with open(LOW_STOCK_LOG_FILE, "a") as f:
            f.write("\n".join(log_lines))

    except Exception as e:
        with open(LOW_STOCK_LOG_FILE, "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Failed to update low stock: {e}\n")