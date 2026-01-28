# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from api_client import DynamicApiClient

def main():
    # Initialize the client. 
    # It will automatically look for 'config.yml'.
    # If config.yml doesn't exist, it will use the defaults or provided arguments.
    client = DynamicApiClient()

    print(f"Using Base URL: {client.base_url}")

    # --- Example: gat_all_meetings_for_org_desc ---
    print("\nMaking gat_all_meetings_for_org_desc request...")
    # Using the specific endpoint and query parameters provided
    # The endpoint is appended to the base_url from config.yml
    meetings_response = client.make_request(
        method="GET",
        endpoint="/meetings/9abfdbc2-378d-4c69-b140-7c55c5db7222",
        params={"direction": "desc"}
    )
    if meetings_response:
        client.save_to_json(meetings_response, "gat_all_meetings_for_org_desc.json")

if __name__ == "__main__":
    main()
