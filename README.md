# Azure Key Vault Management CLI

A Python-based Command Line Interface (CLI) tool for managing Azure Key Vault resources including Keys, Secrets, and Certificates. This tool provides a user-friendly interface to perform CRUD operations, manage versions, and handle resource properties.

## Features

*   **Resource Management**: Create, Read, Update, and Delete (CRUD) operations for:
    *   **Keys**: Support for RSA and EC keys, custom sizes/curves, and activation/expiration dates.
    *   **Secrets**: Manage secret values and tags.
    *   **Certificates**: Create and renew certificates.
*   **Version Control**:
    *   List all versions of a resource.
    *   Enable/Disable specific versions.
    *   **Rotation**: Create new versions of keys and secrets.
    *   **Cleanup**: One-click option to "Disable all but newest version".
*   **Enhanced UI/UX**:
    *   Interactive menus with color-coded output.
    *   **Sidebar View**: Displays a list of available items (Keys/Secrets/Certs) on the right side of the terminal when prompting for selection.
    *   **Navigation**: Press `Esc` to go back from selection prompts.
*   **Safety**:
    *   Error handling for operations on resources managed by certificates (prevents accidental modification of managed keys/secrets).

## Prerequisites

*   Python 3.8+
*   An Azure Subscription
*   An Azure Key Vault instance

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd script.kv-mgmt
    ```

2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    # .venv\Scripts\activate   # Windows
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the root directory with your Azure credentials and Key Vault URL. You can use a Service Principal or other authentication methods supported by `DefaultAzureCredential`.

Example `.env`:
```env
KEY_VAULT_URL=https://<your-key-vault-name>.vault.azure.net/
AZURE_TENANT_ID=<your-tenant-id>
AZURE_CLIENT_ID=<your-client-id>
AZURE_CLIENT_SECRET=<your-client-secret>
```

## Usage

Run the main script to start the application:

```bash
python main.py
```

### Navigation
- Use the number keys to select menu options.
- When asked to enter a name, a list of available items will appear on the right.
- Press `Esc` at a name prompt to return to the previous menu.
- Press `Enter` on an empty prompt to go back (if Esc is not supported/working).

## Project Structure

*   `main.py`: Entry point of the application. Handles the CLI menu loop and UI logic.
*   `src/`: Contains the core logic modules.
    *   `auth.py`: Handles Azure authentication.
    *   `get.py`: Functions to retrieve resources.
    *   `create.py`: Functions to create resources.
    *   `delete.py`: Functions to delete resources.
    *   `edit.py`: Functions to update and manage resources.
*   `tests/`: Unit tests for the application.

## Testing

To run the unit tests:

```bash
python -m unittest discover tests
```
