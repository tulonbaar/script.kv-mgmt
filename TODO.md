# TODO / Roadmap

## Features
- [ ] **Soft Delete Support**: Add a menu to manage deleted objects (List Deleted, Recover, Purge). Currently, `delete` only performs a "soft" delete.
- [ ] **Backup and Restore**: Implement functions for backing up keys/secrets and restoring them.
- [ ] **Bulk Operations**: Ability to select and delete/disable multiple objects simultaneously.
- [ ] **Permission Management**: View and edit Access Policies or RBAC for the Key Vault.

## UI/UX
- [ ] **Interactive Selection**: Replace typing names with arrow key navigation through the list (e.g., using `prompt_toolkit` or `curses` library).
- [ ] **Search/Filtering**: Add a search bar above the object list to easily find specific elements.
- [ ] **Pagination**: Handle display of very long object lists (currently the list might not fit on the screen).

## Technical
- [ ] **Logging (Auditing)**: Save operation history (who, what, when) to a log file.
- [ ] **Asynchrony**: Migrate to asynchronous Azure clients (`azure.keyvault.secrets.aio`, etc.) to improve interface performance.
- [ ] **Configuration**: Add a configuration file (e.g., `config.yaml`) for default settings (e.g., default key type, default tags).
