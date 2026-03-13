.PHONY: all build clean help list verify lint test test-unit
.DEFAULT_GOAL := help
.SECONDEXPANSION:

# Variables
SKILLS := $(sort $(patsubst %/SKILL.md,%,$(wildcard */SKILL.md)))
BUILD_DIR := built
ZIP_FILES := $(addprefix $(BUILD_DIR)/,$(addsuffix -skill.zip,$(SKILLS)))
REPO_DIR := $(notdir $(CURDIR))
PARENT_DIR := $(dir $(CURDIR))

# Expand each skill target to every tracked file inside the skill directory so
# package rebuilds happen when assets, scripts, or agent metadata change.
skill_files = $(shell find $(1) -type f | sort)

# Default target
help:
	@echo "llm-doc-skills Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  make build             - Build all skill ZIPs and place in $(BUILD_DIR)/ folder"
	@echo "  make verify            - Verify that every built ZIP is present and readable"
	@echo "  make list              - List the ZIPs currently in $(BUILD_DIR)/"
	@echo "  make clean             - Remove $(BUILD_DIR)/ folder and all ZIP files"
	@echo "  make all               - Clean then build (fresh build)"
	@echo "  make lint              - Lint Markdown, Python, YAML, and skill structure"
	@echo "  make test              - Run lint + unit tests"
	@echo "  make test-unit         - Run Python unit tests only (stdlib, no external tools)"
	@echo "  make help              - Show this help message"
	@echo ""
	@echo "Skills ($(words $(SKILLS))): $(SKILLS)"

# Create build directory
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)
	@echo "Created $(BUILD_DIR)/ directory"

# Build individual ZIP files
$(BUILD_DIR)/%-skill.zip: $(BUILD_DIR) $$(call skill_files,$$*)
	@echo "Building $*-skill.zip..."
	@rm -f "$@"
	@cd "$(PARENT_DIR)" && zip -q -r "$(CURDIR)/$@" "$(REPO_DIR)/$*" -x "$(REPO_DIR)/$*/.DS_Store"
	@echo "  ✓ $@ created"

# Build all ZIPs
build: $(ZIP_FILES)
	@echo ""
	@echo "Build complete! ZIP files ready in $(BUILD_DIR)/:"
	@ls -lh $(BUILD_DIR)/*.zip

# Clean build artifacts
clean:
	@if [ -d "$(BUILD_DIR)" ]; then \
		echo "Removing $(BUILD_DIR)/ folder..."; \
		rm -rf "$(BUILD_DIR)"; \
		echo "  ✓ Cleanup complete"; \
	else \
		echo "Nothing to clean ($(BUILD_DIR)/ not found)"; \
	fi

# Full rebuild
all: clean build
	@echo ""
	@echo "Full rebuild complete!"
	@echo "Skills available in: $(BUILD_DIR)/"

# Verify build
verify:
	@if [ ! -d "$(BUILD_DIR)" ]; then \
		echo "Error: $(BUILD_DIR)/ does not exist. Run 'make build' first."; \
		exit 1; \
	fi
	@echo "Verifying ZIP files..."
	@for zip in $(ZIP_FILES); do \
		if [ -f "$$zip" ]; then \
			echo "  ✓ $$zip"; \
			unzip -t "$$zip" > /dev/null 2>&1 && echo "    └─ Valid ZIP"; \
		else \
			echo "  ✗ $$zip (missing)"; \
		fi; \
	done

# ---------------------------------------------------------------------------
# Linting
# ---------------------------------------------------------------------------

# Lint all content: Markdown, Python, YAML, and skill structure (L01–L12, V01–V08 pre-flight)
lint:
	@echo "==> Markdown (markdownlint-cli2)..."
	@markdownlint-cli2 "**/*.md" || exit 1
	@echo "==> YAML (yamllint)..."
	@find . -name "*.yaml" -o -name "*.yml" \
		| grep -v "^./.git/" | grep -v "^./built/" | grep -v "^./node_modules/" \
		| xargs yamllint -c .yamllint.yml || exit 1
	@echo "==> Python (ruff)..."
	@ruff check --select E,F,W,I --ignore E501 \
		$$(find . -name "*.py" -not -path "./built/*" -not -path "./.git/*") || exit 1
	@echo "==> Skill structure (L01–L11)..."
	@python3 scripts/lint_skills.py || exit 1
	@echo "==> Skill quality pre-flight (V01–V08)..."
	@python3 scripts/validate_skills.py || exit 1
	@echo ""
	@echo "Lint passed."

# ---------------------------------------------------------------------------
# Testing and validation
# ---------------------------------------------------------------------------

# Run Python unit tests (stdlib only — no LibreOffice, Poppler, or python-docx)
test-unit:
	@echo "Running unit tests..."
	@python3 -m unittest discover -s tests -v

# Main repo gate: lint + unit tests
test: lint test-unit
	@echo ""
	@echo "All checks passed."

# ---------------------------------------------------------------------------
# List built artifacts
# ---------------------------------------------------------------------------

# List built artifacts
list:
	@if [ -d "$(BUILD_DIR)" ]; then \
		echo "Built skill ZIPs:"; \
		ls -lh $(BUILD_DIR)/*.zip 2>/dev/null || echo "  (no ZIPs found)"; \
	else \
		echo "$(BUILD_DIR)/ folder not found. Run 'make build' first."; \
	fi
