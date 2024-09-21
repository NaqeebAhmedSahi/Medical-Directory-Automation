# Define variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
REQUIREMENTS = requirements.txt
SCRIPT = scrap.py  # Replace with the name of your Python script
EXE_NAME = my_script  # Replace with the desired name for your executable

# Create virtual environment
$(VENV_DIR)/bin/activate: 
	python3 -m venv $(VENV_DIR)
	@echo "Virtual environment created."

# Install required libraries
install: $(VENV_DIR)/bin/activate $(REQUIREMENTS)
	$(PIP) install -r $(REQUIREMENTS)
	@echo "Dependencies installed."

# Generate the requirements.txt file
$(REQUIREMENTS): 
	@echo "undetected-chromedriver" > $(REQUIREMENTS)
	@echo "selenium" >> $(REQUIREMENTS)
	@echo "beautifulsoup4" >> $(REQUIREMENTS)
	@echo "lxml" >> $(REQUIREMENTS)  # Optional, faster parser for BeautifulSoup
	@echo "PyInstaller" >> $(REQUIREMENTS)
	@echo "Requirements file generated."

# Create executable with PyInstaller
build: $(VENV_DIR)/bin/activate install
	$(PYTHON) -m PyInstaller --onefile --name $(EXE_NAME) $(SCRIPT)
	@echo "Executable created."

# Clean the build and dist directories created by PyInstaller
clean:
	rm -rf build dist $(EXE_NAME).spec
	@echo "Cleaned up build files."

# Full setup and build process
all: install build
	@echo "Setup and build complete."

# Phony targets to avoid conflicts with files of the same name
.PHONY: install build clean all
