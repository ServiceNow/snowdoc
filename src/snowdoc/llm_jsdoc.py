import os
import re
import subprocess
import os
from dotenv import load_dotenv, find_dotenv
import boto3
from google import genai
from google.genai import types

load_dotenv(find_dotenv(), override=False)

CODE_RE = re.compile(r"```javascript\s+([\s\S]*?)```", re.IGNORECASE)

def extract_js(markdown_resp: str) -> str:
    m = CODE_RE.search(markdown_resp or "")
    return m.group(1).strip() if m else (markdown_resp or "").strip()

def _ensure_credentials(provider: str):
    """
    Ensure that the environment variables required by the selected LLM provider
    are present. Raise a clear error guiding the user if anything is missing.
    """
    if provider == "gemini":
        if not os.getenv("GEMINI_KEY"):
            raise RuntimeError(
                "Snowdoc: missing GEMINI_KEY environment variable. "
                "Set it in your shell or a .env file (see README)."
            )
    else:
        required = (
            "CLAUDE_AWS_ACCESS_KEY_ID",
            "CLAUDE_AWS_SECRET_ACCESS_KEY",
            "CLAUDE_AWS_DEFAULT_REGION",
        )
        missing = [v for v in required if not os.getenv(v)]
        if missing:
            raise RuntimeError(
                f"Snowdoc: missing AWS credentials: {', '.join(missing)}. "
                "Set them in your shell or a .env file (see README)."
            )

def run_claude(system_prompt: str, user_prompt: str) -> str:
    _ensure_credentials("claude")
    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("CLAUDE_AWS_DEFAULT_REGION"),
        aws_access_key_id=os.getenv("CLAUDE_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("CLAUDE_AWS_SECRET_ACCESS_KEY")
    )
    model_name = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    messages = [{
        "role": "user",
        "content": [{"text": f"{system_prompt}\n\n{user_prompt}"}]
    }]
    inference_config = {"maxTokens": 2048, "temperature": 0.8}
    resp = bedrock_runtime.converse(
        modelId=model_name,
        messages=messages,
        inferenceConfig=inference_config
    )
    for blk in resp["output"]["message"]["content"]:
        if "text" in blk:
            return blk["text"]
    return ""

def inject_jsdoc_with_llm(jsdoc: str, code_sample: str, provider: str) -> str:
    """
    Use the selected LLM provider to inject the given JSDoc into the code sample.
    """
    system_prompt = (
        "You receive: (1) a JavaScript file and (2) one or more JSDoc blocks.\n"
        "Insert each JSDoc block directly at the place it would be if a programmer wrote JSDoc for that JavaScript file.\n"
        "If no reasonable match exists, drop that JSDoc block, do not insert it anywhere.\n"
        "Do not alter, move, or reformat existing code in any other way.\n"
        "Return the full JavaScript file—nothing more."
    )


    user_prompt = f"""
JSDoc to inject:
{jsdoc}

JavaScript code:
{code_sample}
"""
    if provider == "gemini":
        raw_resp = run_gemini(system_prompt, user_prompt)
    else:
        raw_resp = run_claude(system_prompt, user_prompt)
    return extract_js(raw_resp)

def run_gemini(system_prompt, user_prompt):
    """Run a query through Gemini API"""
    _ensure_credentials("gemini")
    client = genai.Client(api_key=os.getenv('GEMINI_KEY'))
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.8,
        max_output_tokens=2048,
    )
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-preview-04-17",
            contents=user_prompt,
            config=config
        )
        return response.text or ""
    except Exception as e:
        print("Gemini error:", e)
        return ""

SYSTEM_PROMPT = """
You are *ServiceNowDocBot*, an expert ServiceNow architect and technical writer.
Your job is to generate complete JSDoc documentation for ServiceNow Script Includes.

======== Operating Modes ========

The user prompt may specify a mode using the token `mode: <value>` where `<value>` is:

1. signature  (default)
   • Produce ONLY a JSDoc-only signature—no method bodies—following the Signature Skeleton below.
   • Wrap the entire result in **one** markdown ```javascript``` code fence and nothing else.

2. inject
   • Return the FULL JavaScript file with the generated JSDoc blocks inserted in the correct places above each class / function declaration.
   • Do **not** otherwise modify, move, or re-format the existing code.
   • Wrap the entire result in one ```javascript``` code fence.

If the prompt omits `mode`, assume `signature`.

======== Signature Skeleton (used ONLY in signature mode) ========

/**
 * @class <API Name>
 * @classdesc <One-sentence summary>
 *
 * <In-depth, 2–4 sentence explanation so any reader instantly knows what
 * the Script Include is for and when to use it.>
 *
 * @author Auto-Generated
 * @version 1.0.0
 */
var <API Name> = Class.create();
<API Name>.prototype = {
    /**
     * @constructor
     * @description Initialise the <API Name> class
     */
    initialize: function() {},

    …one docblock + empty stub for each public method found in the input code sample…

    type: '<API Name>'
};

======== Shared Guidelines ========

• Infer missing param / return types (string, number, boolean, GlideRecord, Array<Object>, Object, Date).
• Any function whose name starts with “_” is private (`@private`).
• Include an `@example` usage block demonstrating how to instantiate and use the Script Include.
• Never include method bodies when operating in `signature` mode."""

USER_PROMPT_TEMPLATE = """
Generate a fresh JSDoc signature for the following metadata.

###
Code:
{code_sample}
###
"""

def generate_jsdoc_signature(code_content, provider="claude", mode="signature"):
    """
    Generate JSDoc signature directly from code content.
    
    Args:
        code_content (str): JavaScript code content to document
        provider (str): LLM provider to use (claude or gemini)
        mode (str): Mode to use (signature or inject)
        
    Returns:
        str: Generated JSDoc signature
    """
    user_prompt = USER_PROMPT_TEMPLATE.format(
        code_sample=code_content,
    )
    # Prepend the mode directive
    user_prompt = f"mode: {mode}\n\n" + user_prompt
    
    if provider == "gemini":
        raw_resp = run_gemini(SYSTEM_PROMPT, user_prompt)
    else:
        raw_resp = run_claude(SYSTEM_PROMPT, user_prompt)
    
    return extract_js(raw_resp)


def generate_jsdoc_for_file(js_path, definition=None, api_name=None, output_path=None, provider="claude", inject_docs=False, eslint_check=False):
    """
    Given a JS file, generate a JSDoc signature using Claude or Gemini and save or print it.
    """
    with open(js_path, "r") as f:
        code_sample = f.read()
    if api_name is None:
        api_name = os.path.splitext(os.path.basename(js_path))[0]
    if definition is None:
        definition = ""
    
    # Determine the mode
    mode = "inject" if inject_docs or os.path.abspath(output_path or "") == os.path.abspath(js_path) else "signature"
    
    # Generate JSDoc signature
    jsdoc = generate_jsdoc_signature(code_sample, provider=provider, mode=mode)
    
    # Run ESLint check if requested and inject_docs is enabled
    if eslint_check and mode == "inject":
        from .batch_processor import run_eslint_check
        try:
            eslint_results, is_success = run_eslint_check(jsdoc)
            if is_success:
                print(f"ESLint check passed for {js_path}")
            else:
                print(f"ESLint check found issues for {js_path}:")
                print(f"\n{eslint_results}\n")
        except Exception as e:
            print(f"ESLint check failed: {str(e)}")
    
    if output_path:
        with open(output_path, "w") as out:
            out.write(jsdoc)
    else:
        print(jsdoc)