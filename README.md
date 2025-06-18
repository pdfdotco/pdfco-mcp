# PDF.co MCP

PDF.co MCP Server provides [PDF.co API](https://pdf.co) functionality through the Model Context Protocol (MCP), enabling AI assistants to easily perform various PDF processing tasks.

## 🚀 Key Features

### 📄 PDF Conversion Tools
- **PDF → Various Formats**: Convert PDFs to JSON, CSV, Text, Excel (XLS/XLSX), XML, HTML, Images (JPG/PNG/WebP/TIFF)
- **Various Formats → PDF**: Convert documents (DOC/DOCX/RTF/TXT), spreadsheets (CSV/XLS/XLSX), images, web pages, HTML, emails (MSG/EML) to PDF
- **Excel Conversions**: Convert Excel files to CSV, JSON, HTML, TXT, XML, PDF

### 🛠️ PDF Editing & Modification
- **PDF Merging**: Combine multiple PDF files into one
- **PDF Splitting**: Split PDFs by specific pages or page ranges
- **Add Annotations & Images**: Add text, links, images, shapes to PDFs
- **Form Operations**: Read PDF form field information, fill forms, create new form elements

### 🔍 PDF Search & Analysis
- **Text Search**: Search text in PDFs (supports regular expressions)
- **Table Detection**: Find table locations and coordinates in PDFs
- **AI Invoice Parser**: Extract invoice data using AI
- **PDF Information**: Get detailed information including metadata, page count, security info

### 🔒 Security & Accessibility
- **Password Protection**: Add/remove password protection to PDFs
- **Searchability**: Make PDFs searchable via OCR or remove text layers
- **Attachment Extraction**: Extract attachments from PDFs

### 💼 File Management
- **File Upload**: Upload local files to PDF.co servers
- **Job Status Tracking**: Monitor progress and results of asynchronous operations

## ⚙️ Configuration

### 🔑 Get API Key
1. Sign up at [PDF.co website](https://pdf.co)
2. Get your API key from the dashboard

### 📦 Install UV
You need to install UV (a fast Python packaging tool) to use this MCP server:

#### macOS and Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Alternative Installation Methods
- **Homebrew**: `brew install uv`
- **PyPI with pipx**: `pipx install uv`
- **PyPI with pip**: `pip install uv`

For more installation options and details, see the [UV installation guide](https://docs.astral.sh/uv/getting-started/installation/).

### MCP Server Setup

#### Cursor IDE Configuration
Add the following to your `.cursor/mcp.json` file:

```json
{
  "mcpServers": {
    "pdfco": {
      "command": "uvx",
      "args": ["pdfco-mcp"],
      "env": {
        "X_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

#### Claude Desktop Configuration
Add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "pdfco": {
      "command": "uvx",
      "args": ["pdfco-mcp"],
      "env": {
        "X_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

## 🔧 Available Tools

### PDF Conversion Tools
- `pdf_to_json`: Convert PDF and scanned images into JSON representation with text, fonts, images, vectors, and formatting preserved
- `pdf_to_csv`: Convert PDF and scanned images into CSV representation with layout, columns, rows, and tables
- `pdf_to_text`: Convert PDF and scanned images to text with layout preserved
- `pdf_to_xls`: Convert PDF and scanned images to XLS (Excel 97-2003) format
- `pdf_to_xlsx`: Convert PDF and scanned images to XLSX (Excel 2007+) format
- `pdf_to_xml`: Convert PDF and scanned images to XML format
- `pdf_to_html`: Convert PDF and scanned images to HTML format
- `pdf_to_image`: Convert PDF and scanned images to various image formats (JPG, PNG, WebP, TIFF)

### Document to PDF Conversion Tools
- `document_to_pdf`: Convert various document types (DOC, DOCX, RTF, TXT, XLS, XLSX, CSV, HTML, JPG, PNG, TIFF, WEBP) into PDF
- `csv_to_pdf`: Convert CSV or spreadsheet files (XLS, XLSX) to PDF
- `image_to_pdf`: Convert various image formats (JPG, PNG, TIFF) to PDF
- `webpage_to_pdf`: Convert external webpage URL to PDF
- `html_to_pdf`: Convert HTML to PDF
- `email_to_pdf`: Convert email to PDF

### Excel Conversion Tools
- `excel_to_csv`: Convert Excel(XLS, XLSX) to CSV
- `excel_to_json`: Convert Excel(XLS, XLSX) to JSON
- `excel_to_html`: Convert Excel(XLS, XLSX) to HTML
- `excel_to_txt`: Convert Excel(XLS, XLSX) to TXT
- `excel_to_xml`: Convert Excel(XLS, XLSX) to XML
- `excel_to_pdf`: Convert Excel(XLS, XLSX) to PDF

### PDF Editing Tools
- `pdf_add_annotations_images_fields`: Add text, images, forms, other PDFs, fill forms, links to external sites and external PDF files. You can update or modify PDF and scanned PDF files
- `pdf_merge`: Merge PDF from two or more PDF, DOC, XLS, images, even ZIP with documents and images into a new PDF
- `pdf_split`: Split a PDF into multiple PDF files using page indexes or page ranges

### PDF Form Tools
- `read_pdf_forms_info`: Extracts information about fillable PDF fields from an input PDF file
- `fill_pdf_forms`: Fill existing form fields in a PDF document
- `create_fillable_forms`: Create new fillable form elements in a PDF document

### PDF Search Tools
- `find_text`: Find text in PDF and get coordinates. Supports regular expressions
- `find_table`: Find tables in PDF and get their coordinates

### PDF Analysis Tools
- `ai_invoice_parser`: AI Invoice Parser: Extracts data from invoices using AI
- `extract_attachments`: Extracts attachments from a source PDF file
- `pdf_info_reader`: Get detailed information about a PDF document - number of pages, metadata, security, form fields, and more

### PDF Security Tools
- `pdf_add_password`: Add password protection to a PDF file
- `pdf_remove_password`: Remove password protection from a PDF file

### PDF Searchability Tools
- `pdf_make_searchable`: Convert scanned PDF documents or image files into a text-searchable PDF. Runs OCR and adds an invisible text layer that can be used for text search
- `pdf_make_unsearchable`: Make existing PDF document non-searchable by removing the text layer from it

### File Management Tools
- `upload_file`: Upload a file to the PDF.co API
- `get_job_check`: Check the status and results of a job. Status can be: working, success, failed, aborted, or unknown
- `wait_job_completion`: Wait for a job to complete

## 📖 Usage Examples

### Convert PDF to Text
```
Convert this PDF file to text: https://example.com/document.pdf
```

### Merge Multiple Images into PDF
```
Create a PDF from these images: image1.jpg, image2.png, image3.jpg
```

### Search for Specific Text in PDF
```
Find the word "contract" in this PDF document
```

### Fill PDF Form Fields
```
Fill the name field in this PDF form with "John Doe"
```

### Convert Web Page to PDF
```
Convert https://example.com webpage to PDF
```

### Extract Invoice Data
```
Extract invoice information from this PDF using AI
```

### Add Password Protection
```
Add password protection to this PDF file
```


## 📞 Support & Contact

- **PDF.co**: https://pdf.co
- **PDF.co API Documentation**: https://developer.pdf.co
- **Issue Reports**: Please report issues through GitHub Issues

## 📄 License

This project is distributed under the MIT License.

---

**Note**: A valid PDF.co API key is required to use this tool. Create a free account at [PDF.co](https://pdf.co) to get your API key.