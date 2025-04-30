# Personalized Community Resource Navigator

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.25.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Workshop](https://img.shields.io/badge/Workshop-Healthcare_Access_2025-blueviolet.svg)

The **Personalized Community Resource Navigator** is a Streamlit-based web application designed to connect uninsured patients in Austin, TX, to tailored healthcare resources. It addresses the challenge of fragmented resource information by providing personalized clinic recommendations based on ZIP code, medical needs, insurance status, language, and gender-specific services. The system uses fuzzy matching for rapid searches and OpenAI’s `gpt-3.5-turbo` for advanced filtering and recommendations.

**[Report](https://drive.google.com/file/d/1pLamwVPSfO-5hFkN3VEdp_4A3K4S0Hw8/view)** | **[Presentation](https://docs.google.com/presentation/d/1BnSVydFdBEBJJyUr9QxwNaIlHUA0WR3QXsuFypzm_7w/edit#slide=id.p)**

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
- **User-Friendly Interface**: Streamlit app with input form for ZIP code, medical needs, insurance, language, and gender.
- **Dual Search Modes**:
  - Fuzzy matching (`fuzzywuzzy`) for quick, local searches (>80% match score).
  - LLM-based search (`gpt-3.5-turbo`) for nuanced filtering and recommendations.
- **Data Pipeline**: Scrapes clinic data from FreeClinics.com and Central Health, processes into `resources.csv`.
- **Performance**: LLM-3.2s response time; fuzzy-0.8s.
- **Impact**: Potential to reduce emergency visits by 10–15%, saving $5–10M annually.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hbk008/personalized-resource-navigator.git
   cd personalized-resource-navigator
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up OpenAI API Key**:
   - Create a `.env` file:
     ```bash
     echo "OPENAI_API_KEY=your-api-key" > .env
     ```
   - Install `python-dotenv`:
     ```bash
     pip install python-dotenv
     ```

5. **Download Sample Data**:
   - `resources.csv` is included. To regenerate, run:
     ```bash
     python generate_data.py
     ```

## Usage
1. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```
   - Access at `http://localhost:8501`.

2. **Interact**:
   - Enter ZIP code (e.g., 78701), select medical needs (e.g., mental health), insurance (Uninsured), language (English), and gender (All).
   - Choose “Traditional” (fuzzy) or “AI-Powered” (LLM) search.
   - View results (e.g., Austin Center for Homeless).

To run the app locally for your own demo:
1. Follow [Installation](#installation) and [Usage](#usage).
2. Take a screenshot of the app interface for presentations.

## Project Structure
```
personalized-resource-navigator/
├── app.py               # Streamlit web app
├── generate_data.py     # Data scraping and processing
├── resources.csv        # Sample clinic dataset
├── requirements.txt     # Python dependencies
├── .gitignore           # Git exclusions
└── README.md            # Project documentation
```

## Contributing
We welcome contributions to enhance the Navigator! To contribute:
1. Fork the repository.
2. Create a branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push: `git push origin feature/your-feature`.
5. Open a Pull Request with a clear description.

**Ideas**:
- Add geospatial visualization (`streamlit-folio`).
- Support multilingual inputs (Spanish, Vietnamese).
- Integrate real-time clinic data via APIs.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
