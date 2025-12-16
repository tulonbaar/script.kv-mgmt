# Changelog

## [1.0.0] - 2025-12-16

### Added
- **Core Functionality**:
    - Complete CLI menu system for managing Azure Key Vault resources.
    - CRUD (Create, Read, Update, Delete) operations for Keys, Secrets, and Certificates.
    - Support for Basic and Advanced Key creation (RSA/EC, custom sizes/curves, activation/expiration dates).
- **Version Management**:
    - List all versions of Keys, Secrets, and Certificates.
    - Enable/Disable specific versions.
    - **New Feature**: "Disable all but newest version" option to quickly clean up old enabled versions.
- **UI/UX Improvements**:
    - **Sidebar View**: Displays a list of available items on the right side of the terminal during selection prompts.
    - **Navigation**: Added support for the `Esc` key to cancel operations and return to the previous menu.
    - Color-coded terminal output using `colorama`.
- **Error Handling**:
    - Graceful handling of `Forbidden` errors when attempting to delete or update resources managed by certificates (e.g., secrets backing a certificate).
    - User-friendly error messages guiding users to manage the parent certificate instead.
- **Testing**:
    - Comprehensive unit test suite covering:
        - Resource creation, deletion, and updates.
        - Version management logic.
        - Error handling scenarios.
        - UI input handling (Esc key).
- **Documentation**:
    - Added `README.md` with installation, configuration, and usage instructions.
    - Added `TODO.md` outlining the roadmap and future enhancements.

### Technical
- Implemented modular project structure (`src/` for logic, `tests/` for verification).
- Integrated Azure SDKs (`azure-identity`, `azure-keyvault-*`).
- Added `requirements.txt` and `.env` configuration support.
