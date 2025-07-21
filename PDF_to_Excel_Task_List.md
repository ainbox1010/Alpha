# 🛠️ PDF-to-Excel Automation Project – Task Breakdown

**⚠️ UPDATE (2024-07-12): This project is now focused solely on using LlamaParse as the universal PDF parser. All previous approaches (pdfplumber, OCR, ChatGPT, etc.) are deprecated and removed for clarity and maintainability. LlamaParse automatically handles both digital and scanned PDFs (with built-in OCR).**

---

## 📋 Project Overview

### Goal:
Build a universal PDF parser that extracts product data from supplier price lists and updates a master Excel file with proper data matching and validation.

### Excel Structure Analysis:
Based on the master Excel file, each row contains:
- **ID**: Unique identifier
- **Product Name**: e.g., "Grapefruits"
- **Product Variety**: e.g., "Rio Red", "Star Ruby"
- **Remarks**: Additional notes (e.g., "NL", "plastic box")
- **Size/Count**: Numerical values (e.g., 24, 28, 32)
- **kg**: Weight in kilograms (e.g., 15, 14, 14.5)
- **Box/pall**: Boxes per pallet (e.g., 60, 65)
- **Origin**: Country code (e.g., "TR", "USA", "MA")
- **BOX Price NL**: Box price in EUR (currently 0,00 € - to be populated from PDFs)
- **Eur/kg Klp**: Final price per kg in EUR (calculated from box price + logistics)
- **Supplier1-10**: Supplier-specific data columns

### Key Requirements (Iteration 1):
- Universal parser for different supplier PDF formats (**LlamaParse only**)
- Fuzzy matching for product names (multilingual support, fallback if LlamaParse is insufficient)
- Extract box prices and populate BOX Price NL column
- **Excel file handling:**
  - Overwrite the current Excel file and keep a backup before each update
  - Create a new sheet for each day; update the same sheet if the day is the same
- Maintain separate sheets by date
- Handle large PDFs (LlamaParse has no token limits)
- **LlamaParse automatically applies OCR for scanned/image-based PDFs**
- For now, just test LlamaParse output and print parsed data in a human-readable format (e.g., JSON)
- Update Excel immediately after parsing

---

## ✅ Iteration 1: Core Functionality

### 1. PDF Parser Module (`llama_parser.py`)

#### Goal:
Extract product data from PDFs using LlamaParse API (handles both digital and scanned PDFs).

#### Tasks:
- Upload PDF to hosted LlamaParse API
- Parse and normalize product data into standard schema
- Handle large PDFs without token limits
- No fallback or alternative parser needed unless LlamaParse is insufficient for fuzzy/multilingual matching (add fallback if needed)
- Print parsed data in a human-readable format for verification (e.g., JSON)

---

### 2. Excel Handler (`excel_handler.py`)

#### Goal:
Compare parsed product rows with master Excel file and update records.

#### Tasks:
- Load workbook from `OutputData/Full_Database.xlsx`
- Backup the original Excel file before each update
- Create or select sheet based on PDF date (format: "YYYY-MM-DD")
- For each parsed row:
  - **Fuzzy Matching**: Match product names (multilingual support, 80% similarity threshold)
  - **4-key Match**: product, origin, packaging, size (details to be discussed)
  - If match found: update missing fields (especially BOX Price NL)
  - If no match: insert new row
- Populate appropriate Supplier column based on PDF source
- Return list of all changes made

#### Matching Strategy:
- **Primary Key**: Combination of `product`, `origin`, `packaging`, `size`
- **Fuzzy Logic**: Handle "Tomatoes" vs "Tomaten" using translation dictionary and fallback matching
- **Multilingual Support**: Basic translation mapping for common products

#### Data Mapping:
```python
{
  "product": "Grapefruits",
  "variety": "Rio Red", 
  "size_count": 24,
  "weight_kg": 15.0,
  "boxes_per_pallet": 60,
  "origin": "TR",
  "box_price_eur": 32.50,
  "supplier": "Supplier Name",
  "date": "2025-07-11"
}
```

---

### 3. Logger (`logger.py`)

#### Goal:
Record all changes (insertions or updates) to a log file (future iteration).

#### Tasks:
- Write logs as JSON in the `logs/` directory
- Include timestamp, filename, and list of changes
- Log parsing attempts and success/failure rates
- Track fuzzy matching decisions

---

### 4. Main Controller (`main.py`)

#### Goal:
Tie everything together with proper error handling.

#### Tasks:
- Loop through `InputData/` folder (for testing)
- Parse each file using `llama_parser.extract_data_from_pdf()`
- Print parsed data in a human-readable format for verification
- Update Excel using `excel_handler.update_excel()`
- (Future) Log all changes with `logger.log_changes()`
- **Error Handling**: Continue processing other files if one fails

---

### 5. Configuration File (`config.py`)

#### Tasks:
- Store LlamaParse API key (read from `.env`)
- Set paths: `INPUT_DIR`, `OUTPUT_DIR`, `LOG_DIR`
- Configure fuzzy matching dictionaries

---

### 6. Directory Structure

```
project/
├── main.py
├── llama_parser.py
├── excel_handler.py
├── logger.py
├── config.py
├── utils.py
├── InputData/
├── OutputData/
├── logs/
└── models.py
```

---

## 🧪 Output Schema (Parsed Row)

Each parsed product row should have this structure:

```python
{
  "product": "Grapefruits",
  "variety": "Rio Red",
  "size_count": 24,
  "weight_kg": 15.0,
  "boxes_per_pallet": 60,
  "origin": "TR",
  "box_price_eur": 32.50,
  "supplier": "P. Solleveld Export BV",
  "date": "2025-07-11",
  "remarks": "NL"
}
```

---

## 🚀 Iteration 2: Enhanced Features

- Error handling and retry mechanisms
- Data validation and cleaning
- Configuration for different supplier formats (if needed)
- Simple web interface for monitoring
- Backup and versioning for Excel file
- Currency and unit conversions

---

## 🔄 Future Enhancements (Django Migration)

- Replace Excel with PostgreSQL database
- Add Django admin interface for browsing and managing product records
- Add Django REST API for querying past data by date, product, or price
- Implement user authentication and role-based access
- Add real-time notifications via WebSockets
- Create supplier management interface
- Add data analytics and reporting dashboard

---

## 🏗️ Modular Project Structure (Agreed)

To maximize reusability, clarity, and future-proofing, the project is split into the following modules:

- **main.py**: Entry point; orchestrates the workflow and argument parsing.
- **llama_parser.py**: Handles all interaction with the LlamaParse API and PDF parsing.
- **excel_handler.py**: Manages Excel file loading, backup, sheet creation, and row updates.
- **fuzzy_matcher.py**: Contains all fuzzy matching and multilingual support logic.
- **config.py**: Loads configuration from `.env` and centralizes paths, API keys, and constants.
- **logger.py**: Handles logging of changes, errors, and decisions (to file and/or console).
- **models.py**: Contains data classes (e.g., `ParsedProduct`) and type definitions for structured data.
- **utils.py**: Miscellaneous helpers (e.g., date formatting, file utilities).
- **logs/**: Directory for log files (future use).

### Directory Layout

```
Alpha/
├── main.py
├── llama_parser.py
├── excel_handler.py
├── fuzzy_matcher.py
├── config.py
├── logger.py
├── models.py
├── utils.py
├── InputData/
├── OutputData/
├── logs/
├── PDF_to_Excel_Task_List.md
├── .env
```

### Rationale
- **Separation of concerns:** Each module has a clear, single responsibility.
- **Maximal modularity:** All logic is split into focused modules for easy reuse and testing.
- **Future-proof:** Ready for Django, database, email, or web interface integration.
- **Reusability:** Modules like `llama_parser.py` and `fuzzy_matcher.py` can be used in other projects.
- **Testability:** Each module can be tested independently.