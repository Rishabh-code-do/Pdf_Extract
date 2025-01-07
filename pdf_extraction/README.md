# PDF Reasoning Extraction and Query Application

This Django application allows users to upload PDF files, extract reasoning and associated metadata, store them in a database, and query the data based on specific criteria.

## Prerequisites
- Python >= 3.8
- Django >= 4.0
- pdfplumber
- A supported database (e.g., SQLite, PostgreSQL)

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate    # Linux/MacOS
    venv\Scripts\activate       # Windows
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the server**:
    ```bash
    python manage.py runserver
    ```

Access the app at `http://127.0.0.1:8000`.

---

## Endpoints

### 1. **Upload PDF**
**URL:** `/app/upload/`  
**Method:** `POST`  
**Description:** Uploads a PDF and extracts reasoning data.  
**Payload:**
- `pdf_file`: The PDF file to upload.
- `access_tag`: Tag for access control.  

---

### 2. **Uploaded PDF Page**
**URL:** `/app/uploaded_pdf_page/`  
**Method:** `GET`  
**Description:** Confirms successful upload.

---

### 3. **Query Reasoning**
**URL:** `/app/query/`  
**Method:** `GET`  
**Description:** Fetch reasoning data with optional filters.  
**Query Parameters:**
- `date`: (Optional) Find reasoning closest to this date. Format: `YYYY-MM-DD`.
- `security_tag`: (Optional) Filter by security tag.
- `access_tag`: (Optional) Filter by access tag.

**Example Request:**
```bash
http://127.0.0.1:8000/query/?date=2025-01-01&security_tag=confidential
