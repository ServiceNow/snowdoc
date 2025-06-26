import click
from .llm_jsdoc import generate_jsdoc_for_file
from .batch_processor import process_batch_file

@click.command()
@click.argument("file", type=click.Path(exists=True), required=False)
@click.option("-o", "--output", type=click.Path(), help="Output file (default: stdout)")
@click.option("-i", "--in-place", is_flag=True, help="Overwrite the input file")
@click.option("--inject-docs", is_flag=True, help="Inject docs into code even when writing to a separate output file")
@click.option("--provider", type=click.Choice(["claude", "gemini"]), default="claude", help="LLM provider to use (claude or gemini)")
@click.option("--batch-file", type=click.Path(exists=True), help="CSV or XLSX file containing code files to process")
@click.option("--code-column", help="Column name in batch file containing code content or file paths")
@click.option("--output-column", help="Column name in batch file to write generated JSDoc signatures")
def main(file, output, in_place, inject_docs, provider, batch_file, code_column, output_column):
    # Handle batch processing if a batch file is provided
    if batch_file:
        if not code_column:
            raise click.UsageError("--code-column is required when using --batch-file")
        if not output_column:
            raise click.UsageError("--output-column is required when using --batch-file")
        
        process_batch_file(batch_file, code_column, output_column, provider, inject_docs, output_file=output)
    else:
        # Process a single file as before
        if not file:
            raise click.UsageError("FILE argument is required when not using --batch-file")
            
        out_path = file if in_place else output
        merge = in_place or inject_docs
        generate_jsdoc_for_file(file, output_path=out_path, provider=provider, inject_docs=merge)

if __name__ == "__main__":
    main()