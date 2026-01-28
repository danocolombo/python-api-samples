# Dynamic API Client and JSON Saver

A flexible Python tool to make various REST API calls (GET, POST, etc.) and save the responses directly to local JSON files. This project is designed to be dynamic, allowing you to easily interact with different endpoints and persist the data for further analysis.

## Features

- **Dynamic Requests**: Supports all standard HTTP methods (GET, POST, PUT, DELETE, etc.).
- **Automatic JSON Saving**: Easily save `requests.Response` objects to formatted JSON files.
- **Flexible Configuration**: Use a `config.yml` file to manage base URLs, default headers, and secrets.
- **Error Handling**: Basic error handling for network requests and JSON parsing.

## Installation

1.  **Clone the repository** (or copy the files):
    ```bash
    git clone <repository-url>
    cd apiSample
    ```

2.  **Install dependencies**:
    This project requires `requests` and `PyYAML`.
    ```bash
    pip install requests PyYAML
    ```

3.  **Setup Configuration**:
    Copy the example configuration file and customize it:
    ```bash
    cp config.yml.example config.yml
    ```
    Note: `config.yml` is ignored by Git to keep your secrets safe.

## Configuration

The project uses a `config.yml` file to manage environment-specific settings. You can define your base URL, default headers, and secrets here.

### Configuration Structure

```yaml
server:
  base_url: "https://api.example.com"
  output_dir: "data_files"

headers:
  Content-Type: "application/json"
  Authorization: "Bearer your_token_here"

secrets:
  api_key: "your_secret_key"
```

- **`server.base_url`**: The root URL for your API requests. If set, you can use relative paths in `make_request`.
- **`server.output_dir`**: The directory where JSON response files will be saved (defaults to `data_files`).
- **`headers`**: A dictionary of headers that will be included in every request by default.
- **`secrets`**: A place to store sensitive information that can be retrieved using `client.get_secret('key_name')`.

## Usage

### Basic Example

You can use the `DynamicApiClient` in your own scripts as follows:

```python
from api_client import DynamicApiClient

# Initialize the client (optional base_url)
client = DynamicApiClient(base_url="https://fortsonguru.com/jericho/public/api")

# Make a GET request (gat_all_meetings_for_org_desc)
response = client.make_request(
    method="GET", 
    endpoint="/meetings/9abfdbc2-378d-4c69-b140-7c55c5db7222",
    params={"direction": "desc"}
)

# Save to a specific file
if response:
    client.save_to_json(response, "meetings_data.json")
```

### POST Request with Data

```python
client = DynamicApiClient()

data = {
    "title": "foo",
    "body": "bar",
    "userId": 1
}

response = client.make_request(
    method="POST",
    endpoint="https://jsonplaceholder.typicode.com/posts",
    data=data
)

if response:
    client.save_to_json(response, "post_result.json")
```

## Running the Sample Script

The project includes a `main.py` file that demonstrates both GET and POST requests using the [JSONPlaceholder](https://jsonplaceholder.typicode.com/) API.

To run it:
```bash
python3 main.py
```

This will generate `get_response.json` and `post_response.json` in the `data_files/` directory.

## Project Structure

- `api_client.py`: Contains the `DynamicApiClient` class.
- `main.py`: A demonstration script showing how to use the client.
- `README.md`: Project documentation.

## Connecting to GitHub

To push this project to your GitHub account:

1.  **Create a new repository** on GitHub (do not initialize it with a README or license).
2.  **Add the remote** to your local repository:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/apiSample.git
    ```
3.  **Rename the branch** (if necessary, though we use `main` here):
    ```bash
    git branch -M main
    ```
4.  **Push your code**:
    ```bash
    git push -u origin main
    ```
