import os
import json
import google.generativeai as genai
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

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

def set_rtl_font(run):
    """Set RTL font properties for Arabic text."""
    run.font.name = 'Arial'
    run._element.rPr.rFonts.set(qn('w:cs'), 'Arial')
    run._element.rPr.rFonts.set(qn('w:ascii'), 'Arial')
    run._element.rPr.rFonts.set(qn('w:hAnsi'), 'Arial')

def create_document(content, filename, lang='ar'):
    """Create and format a Word document with the given content."""
    doc = Document()
    
    # Set RTL direction for Arabic
    is_rtl = lang == 'ar'
    
    # Add title
    title = doc.add_heading(level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.RIGHT if is_rtl else WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.add_run(content['title'])
    title_run.font.size = Pt(16)
    if is_rtl:
        set_rtl_font(title_run)
    
    # Add content sections
    for section in content['sections']:
        # Add section heading
        heading = doc.add_heading(level=2)
        heading.alignment = WD_ALIGN_PARAGRAPH.RIGHT if is_rtl else WD_ALIGN_PARAGRAPH.LEFT
        heading_run = heading.add_run(section['heading'])
        heading_run.font.size = Pt(14)
        if is_rtl:
            set_rtl_font(heading_run)
        
        # Add section content
        paragraph = doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT if is_rtl else WD_ALIGN_PARAGRAPH.JUSTIFY
        
        # Clean the content text before adding it
        cleaned_content = clean_text(section['content'])
        content_run = paragraph.add_run(cleaned_content)
        content_run.font.size = Pt(12)
        if is_rtl:
            set_rtl_font(content_run)
    
    # Save document
    doc.save(filename)
    return f"Document saved successfully as {filename}"

def generate_research_content(topic, lang='ar'):
    """Generate research content using Google Gemini."""
    if lang == 'ar':
        prompt = f"""
        قم بإنشاء بحث شامل باللغة العربية حول موضوع: {topic}
        يجب أن يكون المحتوى بتنسيق JSON كما يلي:
        {{
            "title": "عنوان البحث الرئيسي",
            "sections": [
                {{
                    "heading": "عنوان القسم",
                    "content": "محتوى القسم"
                }}
            ]
        }}
        
        يجب أن يتضمن البحث الأقسام التالية بالترتيب:
        1. مقدمة
        2. المفاهيم والتعريفات الأساسية
        3. الوضع الحالي والتطورات
        4. التطبيقات وحالات الاستخدام
        5. الآفاق المستقبلية
        6. الخاتمة
        
        يجب أن يكون المحتوى:
        - باللغة العربية الفصحى
        - شاملاً ومفصلاً
        - مكتوباً بأسلوب علمي
        - خالياً من الأخطاء اللغوية
        - منظماً بشكل منطقي
        
        استخدم النقاط (-) للقوائم إذا لزم الأمر.
        تجنب استخدام الرموز الخاصة أو التنسيقات المعقدة.
        """
    else:
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
    lang = input("Enter the language (ar/en): ")
    filename = f"research_{topic.replace(' ', '_').lower()}_{lang}.docx"
    
    print(f"\nGenerating research content about '{topic}' in {lang}...")
    content = generate_research_content(topic, lang)
    
    if content:
        print("\nCreating Word document...")
        result = create_document(content, filename, lang)
        print(result)
    else:
        print("Failed to generate content. Please try again.")

if __name__ == "__main__":
    main()
