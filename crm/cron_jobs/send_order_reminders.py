from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

LOG_FILE = "/tmp/order_reminders_log.txt"

def main():
    # Setup GraphQL client to connect to your Django server
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Example using your current 'hello' query
    query = gql(
        """
        query {
            hello
        }
        """
    )

    # Execute the query
    result = client.execute(query)

    # Log result to a file
    with open(LOG_FILE, "a") as f:
        log_line = f"{datetime.now()}: Result -> {result}\n"
        f.write(log_line)
        f.flush()  # Write immediately

    print("Query executed successfully! Result:", result)

if __name__ == "__main__":
    main()