import os
import base64
import requests
from dotenv import load_dotenv

def image_to_markdown(image_path, api_key):
    # Encode image to base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Prepare the API request for GPT-4 Vision
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all text from this image and format it as markdown. Use appropriate markdown syntax for headings, lists, emphasis, and other formatting elements that match the visual hierarchy and styling in the image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4096,
        "temperature": 0.7
    }

    # Make the API request
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    # Add error handling and response validation
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    response_data = response.json()
    
    # Extract the markdown text from response
    markdown_text = response_data['choices'][0]['message']['content']
    
    return markdown_text

# Usage example
if __name__ == "__main__":
    load_dotenv()  # Load environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    
    # Make sure API key is available
    if not api_key:
        raise Exception("OPENAI_API_KEY not found in environment variables")
    
    image_path = "./ss.jpg"  # Replace with your actual image path
    
    try:
        markdown_result = image_to_markdown(image_path, api_key)
        print("\nMarkdown output:")
        print(markdown_result)
        
        # Save markdown to file
        with open("output.md", "w", encoding="utf-8") as f:
            f.write(markdown_result)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")