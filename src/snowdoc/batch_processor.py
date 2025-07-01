import os
import pandas as pd
import click
import subprocess
import tempfile
from tqdm import tqdm
from .llm_jsdoc import generate_jsdoc_signature

def process_batch_file(batch_file, code_column, output_column, provider, inject_docs, output_file=None, eslint_check=False):
    """
    Process a CSV or XLSX file containing code to document.
    """
    # Determine file type and read accordingly
    file_ext = os.path.splitext(batch_file)[1].lower()
    if file_ext == '.csv':
        df = pd.read_csv(batch_file)
    elif file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(batch_file)
    else:
        raise click.UsageError(f"Unsupported batch file format: {file_ext}. Use CSV or XLSX.")
    
    # Validate column names
    if code_column not in df.columns:
        raise click.UsageError(f"Column '{code_column}' not found in {batch_file}")
    
    # Create output column if it doesn't exist
    if output_column not in df.columns:
        df[output_column] = ""
        
    # Create ESLint column if eslint_check is enabled
    eslint_column = "ESLint"
    if eslint_check and eslint_column not in df.columns:
        df[eslint_column] = ""
    
    total_rows = len(df)
    click.echo(f"Processing {total_rows} entries from {batch_file}...")
    
    # Create a progress bar
    progress_bar = tqdm(total=total_rows, desc="Generating JSDoc", unit="row")
    
    # Process each row
    success_count = 0
    error_count = 0
    
    for idx, row in df.iterrows():
        code_content = row[code_column]
        if not code_content or pd.isna(code_content):
            progress_bar.update(1)
            continue
        
        try:
            mode = "inject" if inject_docs else "signature"
            jsdoc = generate_jsdoc_signature(code_content, provider=provider, mode=mode)
            
            df.at[idx, output_column] = jsdoc
            success_count += 1
            
            # Run ESLint check if requested and inject_docs is enabled
            if eslint_check and inject_docs:
                try:
                    eslint_results, is_success = run_eslint_check(jsdoc)
                    if is_success:
                        # Add success message to ESLint column
                        df.at[idx, eslint_column] = "PASSED"
                        tqdm.write(f"Row {idx+1}: ESLint check passed")
                    else:
                        # Add ESLint issues to ESLint column
                        df.at[idx, eslint_column] = eslint_results
                        tqdm.write(f"Row {idx+1}: ESLint check found issues")
                except Exception as e:
                    # If ESLint fails, log the error in the ESLint column
                    df.at[idx, eslint_column] = f"Error: {str(e)}"
                    tqdm.write(f"Row {idx+1}: ESLint check failed: {str(e)}")
            
        except Exception as e:
            error_count += 1
            progress_bar.set_postfix_str(f"Errors: {error_count}")
            tqdm.write(f"Error processing row {idx+1}: {str(e)}")
        finally:
            progress_bar.update(1)
    
    progress_bar.close()
    
    click.echo(f"Completed: {success_count} successful, {error_count} errors")
    
    # Save the updated dataframe
    save_path = output_file if output_file else batch_file
    click.echo(f"Saving results to {save_path}...")
    
    # Determine output format based on the file extension
    out_ext = os.path.splitext(save_path)[1].lower()
    
    if out_ext == '.csv' or (not out_ext and file_ext == '.csv'):
        # If no extension and input was CSV, default to CSV
        if not out_ext:
            save_path += '.csv'
        df.to_csv(save_path, index=False)
    elif out_ext in ['.xlsx', '.xls'] or file_ext in ['.xlsx', '.xls']:
        # If extension is Excel or input was Excel, use Excel
        if not out_ext:
            save_path += '.xlsx'
        df.to_excel(save_path, index=False)
    else:
        # Default to CSV if no clear format is specified
        if not out_ext:
            save_path += '.csv'
        df.to_csv(save_path, index=False)
    
    click.echo(f"Batch processing complete. Saved to {save_path}")


def run_eslint_check(code):
    """
    Run ESLint check on the provided JavaScript code.
    
    Returns:
        tuple: (output_message, is_success) where output_message is the ESLint output 
               and is_success is a boolean indicating if ESLint passed
    """
    temp_path = None
    try:
        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(suffix='.js', delete=False) as temp_file:
            temp_path = temp_file.name
            temp_file.write(code.encode('utf-8'))
        
        # Run ESLint on the temporary file
        result = subprocess.run(
            ['npx', 'eslint', temp_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return result.stdout.strip() or "ESLint found issues but didn't provide details", False
        return "All JSDoc requirements passed", True
        
    except subprocess.TimeoutExpired:
        return "ESLint check timed out after 10 seconds. Use --skip-eslint flag to disable ESLint checks.", False
    except subprocess.CalledProcessError:
        return "ESLint check failed: ESLint is not installed or encountered an error", False
    except FileNotFoundError:
        return "ESLint check failed: npx command not found", False
    except Exception as e:
        return f"Unexpected error during ESLint check: {str(e)}", False
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)



