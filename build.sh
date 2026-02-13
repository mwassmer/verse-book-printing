#!/bin/bash
# Build script for Book of Verse PDF
# Unix/Linux/macOS build script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$SCRIPT_DIR/../verse-book-source/docs"
BUILD_DIR="$SCRIPT_DIR/build"
TEMPLATE_DIR="$SCRIPT_DIR/templates"
OUTPUT_DIR="$SCRIPT_DIR/output"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"
OUTPUT_FILE="${1:-output/BookOfVerse.pdf}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Create directories
mkdir -p "$BUILD_DIR" "$OUTPUT_DIR"

echo -e "${CYAN}========================================"
echo "  Building Book of Verse PDF"
echo -e "========================================${NC}"

# Step 1: Check prerequisites
echo -e "\n${YELLOW}[1/4] Checking prerequisites...${NC}"

MISSING_TOOLS=()

if ! command -v python3 &> /dev/null; then
    MISSING_TOOLS+=("Python 3")
fi

if ! command -v pandoc &> /dev/null; then
    MISSING_TOOLS+=("Pandoc")
fi

if ! command -v xelatex &> /dev/null; then
    MISSING_TOOLS+=("XeLaTeX (TeX Live)")
fi

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo -e "\n${RED}Missing required tools:${NC}"
    for tool in "${MISSING_TOOLS[@]}"; do
        echo -e "${RED}  - $tool${NC}"
    done
    echo -e "\n${YELLOW}Please install the missing tools and try again."
    echo -e "See README.md for installation instructions.${NC}"
    exit 1
fi

echo -e "${GREEN}All prerequisites found.${NC}"

# Step 2: Preprocess markdown
echo -e "\n${YELLOW}[2/4] Preprocessing markdown files...${NC}"

COMBINED_MD="$BUILD_DIR/combined.md"

python3 "$SCRIPTS_DIR/preprocess.py" "$DOCS_DIR" "$COMBINED_MD"

echo -e "${GREEN}Preprocessing complete: $COMBINED_MD${NC}"

# Step 3: Convert to PDF with Pandoc
echo -e "\n${YELLOW}[3/4] Converting to PDF with Pandoc...${NC}"

TEMPLATE="$TEMPLATE_DIR/pandoc-template.tex"
OUTPUT_PDF="$SCRIPT_DIR/$OUTPUT_FILE"

pandoc "$COMBINED_MD" \
    -o "$OUTPUT_PDF" \
    --template="$TEMPLATE" \
    --pdf-engine=xelatex \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --top-level-division=chapter \
    --highlight-style=tango \
    --variable="date:$(date +'%B %Y')" \
    --metadata=title:"Book of Verse" \
    --metadata=author:"Jan Vitek and the Verse Team" \
    -V documentclass=book \
    -V papersize=letter \
    -V fontsize=11pt

# Step 4: Verify output
echo -e "\n${YELLOW}[4/4] Verifying output...${NC}"

if [ -f "$OUTPUT_PDF" ]; then
    SIZE=$(du -h "$OUTPUT_PDF" | cut -f1)
    echo -e "\n${GREEN}========================================"
    echo "  Build Successful!"
    echo -e "========================================${NC}"
    echo "Output: $OUTPUT_PDF"
    echo "Size: $SIZE"
else
    echo -e "${RED}Output file not found!${NC}"
    exit 1
fi
