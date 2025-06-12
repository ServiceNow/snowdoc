import click
from .llm_jsdoc import generate_jsdoc_for_file

@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Output file (default: stdout)")
@click.option("-i", "--in-place", is_flag=True, help="Overwrite the input file")
@click.option("--inject-docs", is_flag=True, help="Inject docs into code even when writing to a separate output file")
@click.option("--provider", type=click.Choice(["claude", "gemini"]), default="claude", help="LLM provider to use (claude or gemini)")
def main(file, output, in_place, inject_docs, provider):
    out_path = file if in_place else output
    merge = in_place or inject_docs
    generate_jsdoc_for_file(file, output_path=out_path, provider=provider, inject_docs=merge)

if __name__ == "__main__":
    main()