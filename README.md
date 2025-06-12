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

```bash
poetry run snowdoc [OPTIONS] FILE
```

| Option | Description |
|--------|-------------|
| `-i`, `--in-place` | Overwrite *FILE* by merging JSDoc blocks into the code. |
| `-o`, `--output PATH` | Write result to *PATH*. If omitted the scaffold is printed to stdout. |
| `--inject-docs` | When used **together with** `--output`, merges JSDoc into the code but saves the merged version to *PATH* (leaving the original file untouched). |
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

## Setting up ESLint for Snowdoc Output

To ensure your generated JavaScript files are properly formatted and conform to best practices, Snowdoc can automatically run ESLint with the --fix flag on output files (if ESLint is installed and configured in your project).

### Install ESLint and JSDoc plugin

```bash
npm install --save-dev eslint eslint-plugin-jsdoc
```

---

## Verification

After setup, you can verify a sample .JS file with generated JSDoc annotation by running ESLint:

```bash
npx eslint samples/annotated.js
```

If you use Snowdoc to generate or update files, ESLint will be run automatically on the output file (if available).
---