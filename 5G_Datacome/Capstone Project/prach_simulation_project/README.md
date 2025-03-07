# PRACH Simulation Project

This project simulates PRACH performance with CFBRA under different loads, providing a browser-based interface for non-technical users.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Install ChromeDriver for Selenium (ensure it's in your PATH).
3. Run the server: `python src/server.py`
4. Run tests: 
   - Unit tests: `pytest tests/test_prach_simulation.py`
   - Automation: `robot --pythonpath src tests/prach_tests.robot`
5. View results: Open `http://localhost:5000` in a browser or run `python scripts/selenium_display.py`.

## Folder Structure
- `src/`: Simulation and server code
- `tests/`: Test scripts
- `static/`: Web interface files
- `output/`: Generated results and reports
- `scripts/`: Automation scripts