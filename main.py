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
قم بإعداد بحث علمي شامل باللغة العربية حول الموضوع: {topic}
يجب أن يتم تقديم المحتوى بتنسيق JSON منظم على النحو التالي:
{{
    "title": "عنوان البحث الرئيسي",
    "sections": [
        {{
            "heading": "عنوان القسم",
            "content": "محتوى القسم"
        }}
    ]
}}

يجب أن يتضمن البحث الأقسام الأكاديمية التالية مرتبة بالترتيب:
1. **مقدمة عامة**:
    - تقديم خلفية عامة عن الموضوع.
    - توضيح أهمية الموضوع ودوافع البحث فيه.
    - صياغة أهداف البحث والأسئلة التي يحاول الإجابة عليها.

2. **الإطار النظري والمفاهيم الأساسية**:
    - تعريف المصطلحات والمفاهيم الرئيسية.
    - عرض النظريات والمبادئ ذات الصلة بالموضوع.

3. **منهجية البحث**:
    - شرح المنهجية المستخدمة (تحليلية، وصفية، مقارنة، إلخ).
    - توضيح مصادر المعلومات (كتب، مقالات، بيانات، إلخ).

4. **الوضع الراهن والتطورات الحديثة**:
    - استعراض أبرز الأبحاث والدراسات السابقة في المجال.
    - تحليل الوضع الحالي وتقديم إحصاءات أو بيانات تدعم الفهم.

5. **التحديات والقضايا المطروحة**:
    - مناقشة التحديات أو المشكلات التي تواجه المجال.
    - استعراض وجهات النظر المختلفة حول القضايا المطروحة.

6. **التطبيقات العملية وحالات الاستخدام**:
    - شرح التطبيقات الحالية للموضوع.
    - تقديم أمثلة عملية ودراسات حالة.

7. **الرؤى المستقبلية والتوصيات**:
    - استشراف المستقبل بناءً على المعطيات الحالية.
    - تقديم توصيات مبنية على التحليل.

8. **الخاتمة**:
    - تلخيص أهم النقاط والنتائج.
    - الإجابة على أسئلة البحث المطروحة.
    - اقتراح مجالات للبحث المستقبلي.

المتطلبات الخاصة بالمحتوى:
- أن يكون مكتوبًا باللغة العربية الفصحى.
- أن يغطي الموضوع بشكل شامل ومتكامل.
- أن يُكتب بأسلوب أكاديمي يعتمد التحليل والاستدلال.
- أن يكون منظمًا ومترابطًا وخاليًا من الأخطاء اللغوية.

تعليمات إضافية:
- استخدم النقاط (-) لتنسيق القوائم عند الحاجة.
- تجنب استخدام الرموز الخاصة أو التنسيقات المعقدة.
- احرص على الالتزام بمنهجية الكتابة العلمية.
"""

    else:
        prompt = f"""
Create a comprehensive research document on the topic: {topic}.
The response must be in a JSON format structured as follows:
{{
    "title": "Research Title",
    "sections": [
        {{
            "heading": "Section Heading",
            "content": "Section content in plain text."
        }}
    ]
}}

Ensure the research includes the following academically structured sections in order:

1. **Introduction**:
    - Provide an overview of the topic.
    - Explain the significance of the topic and the rationale for studying it.
    - State the research objectives and the key questions it aims to address.

2. **Theoretical Framework and Key Concepts**:
    - Define critical terms and concepts related to the topic.
    - Present relevant theories and foundational principles.

3. **Research Methodology**:
    - Describe the research approach (e.g., analytical, descriptive, comparative, etc.).
    - Outline the sources of information (e.g., books, articles, datasets).

4. **Current State and Recent Developments**:
    - Review the latest studies and findings in the field.
    - Analyze the current trends and provide relevant data or statistics.

5. **Challenges and Key Issues**:
    - Highlight the main challenges or problems in the field.
    - Discuss varying perspectives and debates surrounding these issues.

6. **Applications and Use Cases**:
    - Detail practical applications of the topic.
    - Provide specific examples or case studies.

7. **Future Outlook and Recommendations**:
    - Forecast future trends based on current developments.
    - Offer recommendations or actionable insights derived from the research.

8. **Conclusion**:
    - Summarize the main points and findings.
    - Address the initial research questions.
    - Suggest areas for further research.

Content Requirements:
- Use clear and concise language.
- Ensure the writing is thorough and academically sound.
- Avoid errors in grammar and spelling.
- Present the content logically and cohesively.

Additional Instructions:
- Use hyphens (-) for bullet points when necessary.
- Avoid using special characters or overly complex formatting.
- Adhere to academic writing standards and maintain a formal tone.
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
