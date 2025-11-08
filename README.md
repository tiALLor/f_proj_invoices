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
python -m src.main
```

Follow the on-screen prompts to:

- Add entities (individual or legal entities)
- Add items (products/services)
- Create purchase orders (POs)
- Generate and send invoices (the app creates a PDF and calls the email routine)

Generated PDF invoices are saved to `PDF_invoice/` (the folder is created automatically by `pdf_creator.py`). The application reads and writes JSON files stored in the `databases/` folder.

## Project layout

- `main.py` — CLI entry point and application flow.
- `class_Database.py` — Database wrapper and load/store helpers.
- `class_Entity.py` — Entity classes (individual/legal) and helpers.
- `class_Item.py` — Item representation and pricing helpers.
- `class_PurchaseOrder.py` — PurchaseOrder class and invoice creation metadata.
- `pdf_creator.py` — Creates PDF invoices (uses `fpdf`).
- `email_service.py` — Email sending helper (reads `.env`/config; ensure SMTP configured).
- `prompts.py` — Interactive prompts & input validation for the CLI.
- `functions.py` — Utility functions used to assemble invoice data.
- `parsers.py` — Input parsing helpers.
- `validators.py` — Additional validation routines.
- `visualization.py` — Simple table display helpers.
- `test_main.py` — Basic tests (run with `pytest`).
- `databases/` — JSON files that store Entities, Items and PurchaseOrders.
- `Fonts/` — Fonts used by the PDF generator (DejaVu fonts included).
- `PDF_invoice/` — Output folder for generated invoice PDFs (created at runtime).

## Databases & sample files

The following JSON files are used to persist data (stored in `databases/`):

- `database_entities.json` — entities/customers/sellers
- `database_items.json` — items/products/services
- `database_POs.json` — purchase orders

These files are read and written by the `Database` class. If files are missing on first run, the application tries to create or initialize them.

## Running tests

Run the test suite with pytest:

```bash
pytest -q
```

There is a `test_main.py` in the repo. Tests are lightweight and expect the project to run in a virtual env with the dependencies installed.

## Notes & known issues

- Some paths in the code use Windows-style backslashes (e.g. `Fonts\\...` and `PDF_invoice\\...`). On Linux these should still generally work with Python (OS path handling), but you may want to change them to use `os.path.join()` or forward slashes for better portability.
- The email sending routine requires SMTP configuration (check `.env.example` and set real credentials in a `.env` file if you intend to use the email feature).
- The `pyproject.toml` lists dependencies

## License

This project does not specify a license in the repository. Add a `LICENSE` file if you plan to share the code publicly.
