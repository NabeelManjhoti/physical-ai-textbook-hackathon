# Physical AI Textbook Backend

This is the FastAPI backend for the Physical AI Interactive Textbook project.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`