import os
import re
import subprocess
from dotenv import load_dotenv, find_dotenv
import boto3
from google import genai
from google.genai import types


# Load environment variables from .env automatically
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
Turn the incoming API metadata into a single **JSDoc signature**, wrapped in a
markdown ```javascript``` fence so downstream code can extract it easily.

**Output rules (MUST follow exactly)**
1. Respond with **one** markdown code fence only:  
   ```javascript
   // …code here…
````

No prose or extra lines before/after it.
2. Inside the fence, follow this skeleton:

```
/**
 * @class <API Name>
 * @classdesc <One-sentence summary>
 *
 * <In-depth, 2-to-4-sentence explanation so any reader instantly knows what
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

    …one docblock + empty stub for each public method found in Code Sample…

    type: '<API Name>'
};
```

3. Infer missing param / return types (string, number, boolean, GlideRecord,
Array<Object>, Object, Date).
4. Any function whose name starts with “_” is private (`@private`).
5. **Never** include method bodies—just the JSDoc and empty stubs.
"""

USER_PROMPT_TEMPLATE = """
Generate a fresh JSDoc signature for the following metadata.

###
Code:
{code_sample}
###
"""

def generate_jsdoc_for_file(js_path, definition=None, api_name=None, output_path=None, provider="claude", inject_docs=False):
    """
    Given a JS file, generate a JSDoc signature using Claude or Gemini and save or print it.
    """
    with open(js_path, "r") as f:
        code_sample = f.read()
    if api_name is None:
        api_name = os.path.splitext(os.path.basename(js_path))[0]
    if definition is None:
        definition = ""
    user_prompt = USER_PROMPT_TEMPLATE.format(
        code_sample=code_sample,
    )
    if provider == "gemini":
        raw_resp = run_gemini(SYSTEM_PROMPT, user_prompt)
    else:
        raw_resp = run_claude(SYSTEM_PROMPT, user_prompt)
    jsdoc = extract_js(raw_resp)
    if output_path:
        if inject_docs or os.path.abspath(output_path) == os.path.abspath(js_path):
            # LLM-based injection
            injected_code = inject_jsdoc_with_llm(jsdoc, code_sample, provider)
            new_contents = injected_code
        else:
            new_contents = jsdoc
        with open(output_path, "w") as out:
            out.write(new_contents)
    else:
        print(jsdoc)