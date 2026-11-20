# create an environment variable
python -m venv .venv                                                                        
.venv\Scripts\Activate 

# Install the requirements
python -m pip install -r requirements.txt 

# Run the backend
python -m uvicorn app.main:app --reload  