# Invoice App

This project is a comprehensive system for managing customers, items, purchase orders, and invoices. It includes functionalities for adding entities and items, creating purchase orders, issuing invoices, and visualizing data.

# Invoice App

This is a small command-line invoice / purchase-order manager that stores simple JSON databases, allows adding entities (customers/sellers), items, and purchase orders, and can generate PDF invoices. It was implemented as a capstone-style project.

## Quick summary

- Main entry point: `main.py` — interactive prompt-driven CLI.
- PDF generation: `pdf_creator.py` (uses `fpdf2`).
- Data is persisted as JSON files in the `databases/` folder.
- Fonts are in the `Fonts/` folder and generated PDFs are written to `PDF_invoice/`.

## Table of contents

- [Requirements](#requirements)
- [Installation (Linux)](#installation-linux)
- [Usage](#usage)
- [Project layout](#project-layout)
- [Databases & files](#databases--files)
- [Running tests](#running-tests)
- [Notes & known issues](#notes--known-issues)

## Requirements

- Python 3.12+ (pyproject.tomal specifies 3.12+)
- Recommended packages (see `pyproject.toml`):
  - fpdf2
  - inquirer
  - python-dotenv
  - validator-collection
  - pytest (for tests)

You can install these with pip (example below).

## Installation (Linux)

1. Clone the repository:

```bash
git clone <your-repo-url> f_proj_invoices
cd f_proj_invoices
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies (using pip):

```bash
pip install --upgrade pip
pip install fpdf2 inquirer python-dotenv validator-collection pytest
```

If you prefer a single command using the `pyproject.toml` you can run (requires pip 23+):

```bash
pip install -e .
```

## Usage

Start the interactive CLI:

```bash
# If you installed with pip install -e .
python -m src.main

# Or run it directly from the src directory
cd src && python main.py
```

Follow the on-screen prompts to:

- Add entities (individual or legal entities)
- Add items (products/services)
- Create purchase orders (POs)
- Generate and send invoices (the app creates a PDF and calls the email routine)

Generated PDF invoices are saved to `src/PDF_invoice/` (the folder is created automatically by `pdf_creator.py`). The application reads and writes JSON files stored in the `src/databases/` folder.

## Project layout

The project uses a src-layout with all Python modules under the `src/` directory:

- `src/main.py` — CLI entry point and application flow.
- `src/class_Database.py` — Database wrapper and load/store helpers.
- `src/class_Entity.py` — Entity classes (individual/legal) and helpers.
- `src/class_Item.py` — Item representation and pricing helpers.
- `src/class_PurchaseOrder.py` — PurchaseOrder class and invoice creation metadata.
- `src/pdf_creator.py` — Creates PDF invoices (uses `fpdf2`).
- `src/email_service.py` — Email sending helper (reads `.env`/config; ensure SMTP configured).
- `src/cli_prompts.py` — Interactive CLI prompts and global state.
- `src/functions.py` — Utility functions used to assemble invoice data.
- `src/parsers.py` — Input parsing helpers.
- `src/visualization.py` — Simple table display helpers.
- `src/test_main.py` — Basic tests (run with `pytest`).

Prompts package (input validation and prompt definitions):

- `src/prompts/` — Package containing prompt-related modules
  - `validators.py` — Input validation functions
  - `prompt_data.py` — Question type definitions and data
  - `query_builder.py` — Helpers to construct inquirer prompts

Data directories:

- `src/databases/` — JSON files that store Entities, Items and PurchaseOrders.
- `src/Fonts/` — Fonts used by the PDF generator (DejaVu fonts included).
- `src/PDF_invoice/` — Output folder for generated invoice PDFs (created at runtime).

## Databases & configuration

The following JSON files are used to persist data (stored in `src/databases/`):

- `database_entities.json` — entities/customers/sellers
- `database_items.json` — items/products/services
- `database_POs.json` — purchase orders

These files are read and written by the `Database` class. If files are missing on first run, the application tries to create or initialize them.

### Email configuration

To use the email feature (sending invoices), copy `.env.example` to `.env` and configure your SMTP settings:

```bash
cp .env.example .env
# Edit .env with your email configuration
```

Required settings in `.env`:

- `SMTP_SERVER` - Your SMTP server address
- `SMTP_PORT` - SMTP port (usually 587 for TLS)
- `SMTP_USERNAME` - Your email username/address
- `SMTP_PASSWORD` - Your email password or app-specific password

## Running tests

Run the test suite with pytest (make sure you're in the project root):

```bash
# Run all tests
python -m pytest src/test_main.py -v

# Run specific test
python -m pytest src/test_main.py -v -k "test_get_invoice_price"
```

Tests are lightweight and expect the project to run in a virtual environment with the dependencies installed. The test file `src/test_main.py` includes basic functionality tests for invoices, items, and purchase orders.

## Notes & known issues

### Path handling

- Some paths in the code use Windows-style backslashes (e.g. `Fonts\\...` and `PDF_invoice\\...`). On Linux these should still generally work with Python (OS path handling), but you may want to change them to use `os.path.join()` or forward slashes for better portability.
- The project uses a src-layout, so all Python modules and data files are under the `src/` directory.

### Dependencies & configuration

- Dependencies are managed through `pyproject.toml`. Use `pip install -e .` to install in development mode.
- The email sending routine requires SMTP configuration in `.env` (see [Email configuration](#email-configuration)).

### Code organization

- CLI prompts and interactions are handled by `src/cli_prompts.py`.
- The `src/prompts/` package contains reusable prompt components:
  - Type definitions (`prompt_data.py`)
  - Input validation (`validators.py`)
  - Prompt construction helpers (`query_builder.py`)
- Use absolute imports from the src root (e.g. `from cli_prompts import ...`).

## License

This project does not specify a license in the repository. Add a `LICENSE` file if you plan to share the code publicly.
