1. **Clone repositori**
   ```bash
   git clone https://github.com/username/crypto_insight.git
   cd crypto_insight
2. **Siapkan virtual environment & install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # atau .venv\Scripts\activate (Windows)
   pip install -r requirements.txt

3. **Jalankan Flask API**
   ```bash
   python -m api.app
4. **Jalankan Streamlit**
   ```bash
   streamlit run streamlit_app/dashboard.py
