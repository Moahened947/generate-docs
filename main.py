import os
import json
import google.generativeai as genai
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Configure Google Gemini API
GOOGLE_API_KEY = "AIzaSyAOdKEsip0P1DkWvC6tMO4hl3jG0rwZc7Y"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

def clean_text(text):
    """Clean text by removing markdown symbols and normalizing line breaks."""
    # Remove markdown bold symbols
    text = text.replace('**', '')
    # Normalize line breaks and indentation
    lines = [line.strip() for line in text.split('\n')]
    return ' '.join(lines)

def create_document(content, filename):
    """Create and format a Word document with the given content."""
    doc = Document()
    
    # Add title (16pt)
    title = doc.add_heading(level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.add_run(content['title'])
    title_run.font.size = Pt(16)
    
    # Add content sections
    for section in content['sections']:
        # Add section heading (14pt)
        heading = doc.add_heading(level=2)
        heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
        heading_run = heading.add_run(section['heading'])
        heading_run.font.size = Pt(14)
        
        # Add section content (12pt)
        paragraph = doc.add_paragraph()
        # Clean the content text before adding it
        cleaned_content = clean_text(section['content'])
        content_run = paragraph.add_run(cleaned_content)
        content_run.font.size = Pt(12)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    # Save document
    doc.save(filename)
    return f"Document saved successfully as {filename}"

def generate_research_content(topic):
    """Generate research content using Google Gemini."""
    prompt = f"""
    Create a comprehensive research document about {topic}.
    Respond with a JSON object containing a title and sections.
    Keep the JSON structure simple and avoid special characters or complex formatting.
    
    Example format:
    {{
        "title": "Your Title Here",
        "sections": [
            {{
                "heading": "Section Heading",
                "content": "Section content in plain text."
            }}
        ]
    }}
    
    Include these sections in order:
    1. Introduction
    2. Main concepts and definitions
    3. Current state and developments
    4. Applications and use cases
    5. Future prospects
    6. Conclusion
    
    Make sure each section is detailed and informative.
    Use simple bullet points with hyphens (-) if needed.
    Avoid using special characters or complex formatting.
    """
    
    response_text = ""
    try:
        # Generate content
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove any markdown code block indicators if present
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        # First attempt to parse JSON
        try:
            content = json.loads(response_text)
            return content
        except json.JSONDecodeError:
            # If direct parsing fails, try to clean the response further
            print("Initial JSON parsing failed, attempting to clean the response...")
            
            # Replace problematic characters
            cleaned_text = response_text.replace('\n', ' ').replace('\r', ' ')
            cleaned_text = ' '.join(cleaned_text.split())
            
            # Try parsing again
            try:
                content = json.loads(cleaned_text)
                return content
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON after cleaning: {e}")
                print("Cleaned response:", cleaned_text)
                return None
            
    except Exception as e:
        print(f"Error generating content: {e}")
        if response_text:
            print("Raw response:", response_text)
        return None

def main():
    topic = input("Enter the research topic: ")
    filename = f"research_{topic.replace(' ', '_').lower()}.docx"
    
    print(f"\nGenerating research content about '{topic}'...")
    content = generate_research_content(topic)
    
    if content:
        print("\nCreating Word document...")
        result = create_document(content, filename)
        print(result)
    else:
        print("Failed to generate content. Please try again.")

if __name__ == "__main__":
    main()
