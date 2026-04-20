# smart_doc_sorter
Smart Doc Sorter is a multi-agent AI-based system that automatically classifies and processes documents .It identifies document type and routes it to specialized agents for structured data extraction. Smart Doc Sorter is a multi-agent AI-based system that automatically classifies and processes documents such as PDFs, JSON files.
# 📄 Smart Doc Sorter

## 🚀 Overview

Smart Doc Sorter is a multi-agent AI system designed to intelligently process and classify different types of documents. It accepts inputs such as PDFs, JSON files, and emails, identifies their type and intent, and routes them to specialized agents for further processing.

This project demonstrates real-world automation of document workflows using AI and shared memory systems.

---

## 🎯 Features

* 📂 Supports multiple formats: PDF, JSON, Email text
* 🤖 Automatic document classification (Invoice, RFQ, Complaint, etc.)
* 🔀 Intelligent routing to specialized agents
* 🧠 Shared memory using Redis
* ⚡ Scalable and modular architecture
* 📊 Extracts structured information from unstructured data

---

## 🏗️ Project Architecture

```
Input Document → Classifier Agent → Router → Specialized Agent → Output
```

### Components:

* **Input Handler** – Reads PDF/JSON/email
* **Classifier Agent** – Identifies document type
* **Router** – Sends to correct processing agent
* **Specialized Agents** – Extract structured data
* **Redis** – Stores shared context

---

## 🛠️ Technologies Used

* Python
* Redis
* pdfplumber (for PDF processing)
* JSON handling
* AI-based classification logic

---

## 📁 Folder Structure

```
smart-doc-sorter/
│
├── app/
│   ├── main.py
│   ├── classifier.py
│   ├── router.py
│   ├── agents/
│   │   ├── invoice_agent.py
│   │   ├── complaint_agent.py
│   │   └── rfq_agent.py
│
├── sample_inputs/
│   ├── sample_invoice.json
│   ├── sample_email.txt
│   └── sample_pdf.pdf
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/smart-doc-sorter.git
cd smart-doc-sorter
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install & Run Redis

#### Windows:

* Download Redis or use WSL
* Run:

```bash
redis-server
```

#### Linux/Mac:

```bash
sudo apt install redis
redis-server
```

---

## ▶️ How to Run

Run the main file with sample input:

```bash
python app/main.py sample_inputs/sample_invoice.json
```

---

## 🧪 Example Inputs

* Invoice JSON
* Email text
* PDF documents

---

## 📈 Output

* Classified document type
* Extracted structured data
* Routing logs (via Redis)

---

## 🌍 Real-World Applications

* 📊 Invoice processing automation
* 📩 Email classification systems
* 🏢 Enterprise document management
* 📦 Procurement systems (RFQ handling)

---

## 🔮 Future Enhancements

* Integrate Machine Learning/NLP models
* Add web interface
* Cloud deployment (AWS/GCP)
* OCR for scanned documents


## ⭐ Contribute

Feel free to fork this repository and contribute!
