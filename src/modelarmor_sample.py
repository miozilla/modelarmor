# pip install google-cloud-modelarmor
from google.cloud import modelarmor_v1
import sys

# Create a client
client = modelarmor_v1.ModelArmorClient(transport="rest", client_options = {"api_endpoint" : "modelarmor.us-central1.rep.googleapis.com"})

# Initialize request argument(s)
user_prompt_data = modelarmor_v1.DataItem()

# Get the prompt from command line argument
if len(sys.argv) > 1: # Check if an argument is provided
    prompt = sys.argv[1] # Take the first argument as the prompt
else:
    # Fallback to a default prompt if no argument is provided
    prompt = "Placeholder prompt."

# Set prompt data for model armor call
user_prompt_data.text = prompt
ma_request = modelarmor_v1.SanitizeUserPromptRequest(
    name="projects/csa-model-armor-demo-012346/locations/us-central1/templates/pijb-only", # name contains the project and template
    user_prompt_data=user_prompt_data,
)

# Make the MA request
ma_response = client.sanitize_user_prompt(request=ma_request)

# Take action based on Model Armor's result
if ma_response.sanitization_result.filter_results["pi_and_jailbreak"].pi_and_jailbreak_filter_result.match_state == modelarmor_v1.FilterMatchState.MATCH_FOUND: # A PIJB match was found
    print("Query failed security check. Error.")
else:
    print("Query passed security check. Sending prompt to LLM.")