# Snowdoc – ServiceNow JSDoc generator

`Snowdoc` turns any ServiceNow-style Script Include (or plain JavaScript file) into a **well-structured and descriptive JSDoc signature** using an LLM (Anthropic Claude or Google Gemini).

---

## Installation

Clone the repository and install dependencies using Poetry:

```bash
git clone https://github.com/ServiceNow/snowdoc
cd snowdoc
poetry install
```

Make sure you have either

* AWS credentials + Bedrock access (for Claude 3 Sonnet) **or**
* `GEMINI_KEY` in your environment for Google Gemini

stored in a `.env` file or exported as environment variables.

---

## Configuration

Snowdoc needs credentials for one of the supported LLM back-ends.
Create a `.env` file **or** export the variables in your shell.

```env
# AWS Bedrock / Claude 3 Sonnet
CLAUDE_AWS_ACCESS_KEY_ID=...
CLAUDE_AWS_SECRET_ACCESS_KEY=...
CLAUDE_AWS_DEFAULT_REGION=...

# Google Gemini
GEMINI_KEY=...
```

---

## Command-line usage

### Single File Processing

```bash
poetry run snowdoc [OPTIONS] FILE
```

| Option | Description |
|--------|-------------|
| `-i`, `--in-place` | Overwrite *FILE* by merging JSDoc blocks into the code. |
| `-o`, `--output PATH` | Write result to *PATH*. If omitted the scaffold is printed to stdout. |
| `--inject-docs` | When used **together with** `--output`, merges JSDoc into the code but saves the merged version to *PATH* (leaving the original file untouched). |
| `--provider {claude,gemini}` | Choose the LLM backend (default `claude`). |

### Batch Processing

Process multiple rows of JavaScript code at once using a CSV or Excel file:

```bash
poetry run snowdoc --batch-file FILE.csv --code-column COLUMN1 --output-column COLUMN2 [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--batch-file PATH` | Path to a CSV or XLSX file containing code to process. |
| `--code-column NAME` | Column name in batch file containing JavaScript code content. |
| `--output-column NAME` | Column name in batch file to write generated JSDoc signatures. |
| `--output PATH` | Optional path to save the processed batch file (if not specified, updates the original file). |
| `--inject-docs` | Generate JSDoc blocks injected into the code rather than just signatures. |
| `--provider {claude,gemini}` | Choose the LLM backend (default `claude`). |

### Examples

Generate a signature scaffold only:

```bash
poetry run snowdoc test.js -o test_jsdoc_signature.js
```

In-place documentation:

```bash
poetry run snowdoc -i test.js
```

Create a *new* annotated copy while keeping the original code intact:

```bash
poetry run snowdoc test.js -o annotated.js --inject-docs
```

Process a batch from a CSV:

```bash
poetry run snowdoc --batch-file scripts.csv --code-column script_code --output-column jsdoc_result
```

## Verification

To verify a sample .JS file with generated JSDoc annotation in it, run eslint:

```bash
npm install --save-dev eslint eslint-plugin-jsdoc
npx eslint samples/annotated.js
```

---
