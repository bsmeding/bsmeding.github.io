VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
REQUIREMENTS_FILE := requirements.txt

.PHONY: all install serve build clean freeze copy-footer

all: install

install:
	@echo "🔧 Creating virtualenv..."
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	@$(PIP) install --upgrade pip
	@echo "📦 Installing requirements from $(REQUIREMENTS_FILE)..."
	@$(PIP) install -r $(REQUIREMENTS_FILE)
	@$(MAKE) copy-footer

serve:
	@echo "🌐 Starting MkDocs development server..."
	@$(VENV_DIR)/bin/mkdocs serve

build:
	@echo "📦 Building static site..."
	@$(VENV_DIR)/bin/mkdocs build

freeze:
	@echo "📋 Freezing current dependencies to $(REQUIREMENTS_FILE)..."
	@$(PIP) freeze > $(REQUIREMENTS_FILE)

clean:
	@echo "🧹 Cleaning up..."
	rm -rf $(VENV_DIR)
	rm -rf site

copy-footer:
	@echo "📄 Copying footer.html from mkdocs_material..."
	@$(PYTHON) -c "\
try: \
  import mkdocs_material, shutil, os; \
  path = os.path.join(mkdocs_material.__path__[0], 'templates', 'partials'); \
  os.makedirs('overrides/partials', exist_ok=True); \
  shutil.copy(os.path.join(path, 'footer.html'), 'overrides/partials/footer.html'); \
  print('✅ footer.html copied to overrides/partials/'); \
except ModuleNotFoundError: \
  print('❌ mkdocs_material not found. Run `make install` first.'); \
  exit(1)"
