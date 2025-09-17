
PY?=python3.12

run:
	streamlit run app.py

venv:
	$(PY) -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
