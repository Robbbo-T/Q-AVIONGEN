# Makefile for Q-AVIOGEN
# Automatización de tareas comunes para Q-AVIOGEN

.PHONY: help install test clean run dev format lint docs

# Default target
help:
	@echo "Q-AVIOGEN - Makefile Commands"
	@echo "============================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install      - Setup environment and install dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linting"
	@echo "  make format       - Format code"
	@echo "  make dev          - Run in development mode"
	@echo ""
	@echo "Execution:"
	@echo "  make run          - Run with example file"
	@echo "  make batch        - Run batch processing"
	@echo "  make demo         - Generate demo video"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean        - Clean generated files"
	@echo "  make docs         - Generate documentation"
	@echo "  make package      - Create distribution package"

# Setup and installation
install:
	@echo "🚀 Setting up Q-AVIOGEN..."
	python setup.py

install-dev: install
	@echo "📦 Installing development dependencies..."
	pip install pytest black flake8 mypy

# Development
test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v

lint:
	@echo "🔍 Running linting..."
	flake8 parser/ tts/ blender/ *.py
	@echo "✅ Linting complete"

format:
	@echo "🎨 Formatting code..."
	black parser/ tts/ blender/ *.py
	@echo "✅ Code formatted"

dev:
	@echo "🔧 Starting development mode..."
	python main.py --input input/markdown/00-30-10-01-TowbarAttachment.md --debug --verbose

# Execution
run:
	@echo "▶️ Running Q-AVIOGEN with example..."
	python main.py --input input/markdown/00-30-10-01-TowbarAttachment.md --output output/videos/

run-yaml:
	@echo "▶️ Running Q-AVIOGEN with YAML example..."
	python main.py --yaml input/yaml/towbar_procedure.yaml --output output/videos/

batch:
	@echo "🎬 Running batch processing..."
	python batch_render.py --input-dir input/ --output-dir output/batch/

demo:
	@echo "🎥 Generating demo video..."
	python main.py --input input/markdown/00-30-10-01-TowbarAttachment.md --output output/demo/ --resolution 720p --verbose

# Utilities
clean:
	@echo "🧹 Cleaning generated files..."
	rm -rf output/videos/*
	rm -rf output/frames/*
	rm -rf output/audio/*
	rm -rf output/batch/*
	rm -rf temp/*
	rm -rf cache/*
	rm -rf __pycache__/
	rm -rf */__pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -name "*.pyc" -delete
	find . -name "test_scene_*.json" -delete
	@echo "✅ Cleanup complete"

clean-all: clean
	@echo "🧹 Deep cleaning..."
	rm -rf venv/
	rm -rf .coverage
	rm -rf htmlcov/
	@echo "✅ Deep cleanup complete"

docs:
	@echo "📚 Generating documentation..."
	mkdir -p docs/
	@echo "# Q-AVIOGEN Documentation" > docs/README.md
	@echo "Documentation generated in docs/"

package:
	@echo "📦 Creating distribution package..."
	python -m build
	@echo "✅ Package created in dist/"

# Quality checks
check: test lint
	@echo "✅ All quality checks passed"

# Installation verification
verify:
	@echo "✔️ Verifying installation..."
	python -c "from parser.md_parser import MarkdownParser; print('✅ MD Parser OK')"
	python -c "from parser.yaml_parser import YAMLParser; print('✅ YAML Parser OK')"
	python -c "from parser.scene_builder import SceneBuilder; print('✅ Scene Builder OK')"
	python -c "from tts.narration import NarrationGenerator; print('✅ TTS Generator OK')"
	@echo "✅ Verification complete"

# Development shortcuts
md:
	python main.py --input input/markdown/00-30-10-01-TowbarAttachment.md --dry-run --verbose

yaml:
	python main.py --yaml input/yaml/towbar_procedure.yaml --dry-run --verbose

# Asset management
assets-check:
	@echo "📋 Checking assets..."
	@ls -la assets/models/ 2>/dev/null || echo "⚠️ No models found in assets/models/"
	@ls -la assets/textures/ 2>/dev/null || echo "⚠️ No textures found in assets/textures/"
	@ls -la assets/audio/ 2>/dev/null || echo "⚠️ No audio found in assets/audio/"

# Performance testing
perf-test:
	@echo "⚡ Running performance tests..."
	time python main.py --input input/markdown/00-30-10-01-TowbarAttachment.md --dry-run

# Environment information
info:
	@echo "📊 Q-AVIOGEN Environment Information"
	@echo "==================================="
	@echo "Python version: $(shell python --version)"
	@echo "Pip version: $(shell pip --version)"
	@echo "Platform: $(shell python -c 'import platform; print(platform.platform())')"
	@echo "Project root: $(shell pwd)"
	@echo "Git branch: $(shell git branch --show-current 2>/dev/null || echo 'Not a git repository')"
	@echo "Git commit: $(shell git rev-parse HEAD 2>/dev/null || echo 'Not a git repository')"
