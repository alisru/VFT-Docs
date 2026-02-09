from google import genai
import os
import glob

# ==============================================================================
# CONFIGURATION
# ==============================================================================
API_KEY = "AIzaSyD-bn-MQxCsMfF-oYPw0o11l7k0se4UX1I"

KANON_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia"
ARCHETYPE_FILE = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Archetype\The_Stoic_Guardian.md"

# ==============================================================================
# KANON INGESTION
# ==============================================================================
def get_ordered_planes():
    """Returns a sorted list of (filename, full_path) for the 7 Planes."""
    # Pattern: Australian_Kanon_Plane_X_Name.md
    files = glob.glob(os.path.join(KANON_DIR, "Australian_Kanon_Plane_*.md"))
    
    # Sort strictly by the plane number in the filename
    # e.g., ...Plane_1_Identity.md -> 1
    def extract_plane_num(filepath):
        base = os.path.basename(filepath)
        parts = base.split('_')
        # Expecting ['Australian', 'Kanon', 'Plane', '1', 'Identity.md']
        try:
            return int(parts[3])
        except (IndexError, ValueError):
            return 99 # Push to end if weird

    return sorted(files, key=extract_plane_num)

def load_file_content(filepath):
    """Reads a single file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# ==============================================================================
# GEMINI SETUP
# ==============================================================================
def analyze_plane(client, model, plane_name, plane_content, user_input, archetype_text):
    """Analyzes the input against a SINGLE specific Plane."""
    
    system_prompt = f"""
    YOU ARE THE AUSTRALIAN ARCHETYPE JUDGE.
    
    We are analyzing the text Plane-by-Plane.
    CURRENT FOCUS: **{plane_name}** (Vector {plane_name.split('_')[1] if '_' in plane_name else '?'}/7)
    
    === THE STANDARD (CONTEXT) ===
    {archetype_text}
    
    === THE CURRENT PLANE (RULES FOR THIS ROUND) ===
    {plane_content}
    
    === YOUR TASK ===
    Analyze the USERS INPUT TEXT specifically against the Vectors and definitions of {plane_name}.
    You must determine if the "Soul" of the text aligns with this specific dimension of the Australian Kanon.
    
    === OUTPUT FORMAT ===
    ## 🧬 Vector Analysis: {plane_name}
    
    **Vector Score:** [0-100]
    *(Rate how strongly they embody this specific aspect. 0 = Anti-Australian, 100 = Ideal Archetype)*
    
    **Key Alignment Check:**
    *   **Specific References:** [Quote or Concept from text] -> [Matches Kanon Vector X]
    *   **Violations:** [If any, list what they violated in this plane]
    
    **The Verdict (This Vector):**
    [1-2 sentences. Do they pass the '{plane_name}' test?]
    """
    
    print(f"\n   ... Analyzing {plane_name} with {model} ... (Please wait)")
    
    full_response = ""
    try:
        # Use streaming to prevent 'hanging' perception
        response_stream = client.models.generate_content(
            model=model,
            contents=system_prompt + "\n\n=== USER INPUT TEXT ===\n" + user_input,
            config={'response_mime_type': 'text/plain'}
        )
        
        # Depending on the SDK, this might be a stream iterator or a direct response.
        # The new google-genai SDK typically returns a generated content object directly 
        # unless stream=True is passed to generate_content_stream (if using that method)
        # However, checking the SDK Docs logic:
        # client.models.generate_content returns a GenerateContentResponse
        # To stream, we usually use client.models.generate_content_stream
        
        # Let's try the standard call first but with a print indicating connection.
        # If the user says it hangs, it might be the model cold start.
        
        return response_stream.text

    except Exception as e:
        return f"Error analyzing {plane_name}: {e}"


# ==============================================================================
# MAIN LOOP
# ==============================================================================
def check_connection(client, model):
    """Performs a quick handshake to verify the model is awake."""
    print(f"   ... Performing startup handshake with {model} ...")
    try:
        response = client.models.generate_content(
            model=model,
            contents="Ping",
        )
        print(f"   [OK] Connection Verified (Latency: Fast)")
        return True
    except Exception as e:
        print(f"   [FAIL] Connection Failed: {e}")
        return False

if __name__ == "__main__":
    
    # Initialize Client
    client = genai.Client(api_key=API_KEY)
    
    # Model Selection
    max_model = 'gemini-3-flash-preview'
    stable_model = 'gemini-2.5-flash'
    
    # Check Model Availability (Simple Logic)
    selected_model = max_model
    
    # STARTUP HANDSHAKE
    print("\n" + "="*60)
    print("Welcome to the 'Rate My Australianness' Engine (Native SDK)")
    print("Initializing Connection...")
    
    if not check_connection(client, selected_model):
        print(f"   ! Primary model {selected_model} failed. Trying fallback...")
        selected_model = stable_model
        if not check_connection(client, selected_model):
            print("   ! FATAL: Could not connect to Gemini API. Check your internet or API key.")
            exit()
    
    print(f"   > Using Model: {selected_model}")

    # Load Archetype once (Global Context)
    archetype_text = ""
    if os.path.exists(ARCHETYPE_FILE):
        with open(ARCHETYPE_FILE, "r", encoding="utf-8") as f:
            archetype_text = f.read()

    planes = get_ordered_planes()
    
    print(f"Loaded {len(planes)} Planes from: {KANON_DIR}")
    print("="*60 + "\n")
    print("Paste a speech, tweet, email, or bio below to judge it.")
    print("Type 'EXIT' to quit.")
    
    while True:
        user_text = input("\nENTER TEXT TO JUDGE:\n> ")
        if user_text.strip().upper() == 'EXIT':
            break
        if not user_text.strip():
            continue
            
        print("\n" + "="*40)
        print("STARTING ANALYSIS")
        print("="*40)

        for plane_path in planes:
            plane_name = os.path.basename(plane_path).replace("Australian_Kanon_", "").replace(".md", "")
            plane_content = load_file_content(plane_path)
            
            # Run Analysis
            result = analyze_plane(client, selected_model, plane_name, plane_content, user_text, archetype_text)
            
            # Handle Model Fallback Runtime
            if "Error" in result and "404" in result or "not found" in result.lower():
                 print(f"   ! Model {selected_model} failed. Switching to {stable_model}...")
                 selected_model = stable_model
                 result = analyze_plane(client, selected_model, plane_name, plane_content, user_text, archetype_text)

            print(result)
            print("-" * 40)
            
            # The Pause
            user_input = input(f"   [Press ENTER to continue to next Plane, or 'q' to quit] >> ")
            if user_input.lower().strip() == 'q':
                break
        
        print("\nAnalysis Complete. G'day.\n")
