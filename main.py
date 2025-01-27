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

def generate_research_content(topic, lang='ar', doc_type='academic'):
    """Generate research content using Google Gemini."""
    if lang == 'ar':
        if doc_type == 'academic':
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
"""
        else:  # report type
            prompt = f"""
قم بإعداد تقرير احترافي شامل باللغة العربية حول الموضوع: {topic}
يجب أن يتم تقديم المحتوى بتنسيق JSON منظم على النحو التالي:
{{
    "title": "عنوان التقرير الرئيسي",
    "sections": [
        {{
            "heading": "عنوان القسم",
            "content": "محتوى القسم"
        }}
    ]
}}

يجب أن يتضمن التقرير الأقسام التالية مرتبة بالترتيب:
1. **الملخص التنفيذي**:
    - نظرة عامة موجزة عن الموضوع.
    - أهم النتائج والتوصيات.
    - القيمة المضافة للتقرير.

2. **خلفية الموضوع**:
    - السياق العام للموضوع.
    - أهمية الموضوع وتأثيره.
    - الأهداف المرجوة من التقرير.

3. **تحليل الوضع الحالي**:
    - تحليل السوق أو المجال.
    - البيانات والإحصاءات ذات الصلة.
    - المؤشرات الرئيسية والاتجاهات.

4. **تحليل التحديات والفرص**:
    - تحديد أبرز التحديات.
    - تحليل الفرص المتاحة.
    - تقييم المخاطر المحتملة.

5. **الحلول والمقترحات**:
    - الحلول العملية للتحديات.
    - الخيارات المتاحة وتقييمها.
    - الموارد المطلوبة للتنفيذ.

6. **خطة العمل والتوصيات**:
    - خطوات التنفيذ المقترحة.
    - الجدول الزمني المتوقع.
    - مؤشرات قياس النجاح.

7. **الخاتمة والخطوات القادمة**:
    - ملخص النقاط الرئيسية.
    - التوصيات النهائية.
    - الخطوات المستقبلية المقترحة.

المتطلبات الخاصة بالمحتوى:
- أن يكون موجهاً نحو النتائج والحلول العملية.
- أن يستخدم لغة مهنية واضحة ومباشرة.
- أن يركز على الجوانب العملية والتنفيذية.
- أن يدعم التوصيات بالبيانات والأدلة.
"""
    else:  # English
        if doc_type == 'academic':
            prompt = f"""
Create a comprehensive academic research document on the topic: {topic}.
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

1. **General Introduction**:
    - Provide a general background on the topic.
    - Explain the significance and research motivation.
    - State research objectives and questions.

2. **Theoretical Framework and Key Concepts**:
    - Define critical terms and concepts.
    - Present relevant theories and principles.

3. **Research Methodology**:
    - Describe the research approach.
    - Outline information sources and methods.

4. **Current State and Recent Developments**:
    - Review latest studies and findings.
    - Analyze current trends with supporting data.

5. **Challenges and Key Issues**:
    - Discuss main challenges in the field.
    - Present different perspectives on issues.

6. **Practical Applications**:
    - Detail current applications.
    - Provide case studies and examples.

7. **Future Outlook and Recommendations**:
    - Project future developments.
    - Offer research-based recommendations.

8. **Conclusion**:
    - Summarize key findings.
    - Address research questions.
    - Suggest future research areas.

Content Requirements:
- Use academic language and style.
- Ensure comprehensive coverage.
- Maintain analytical approach.
- Follow academic writing standards.
"""
        else:  # report type
            prompt = f"""
Create a comprehensive professional report on the topic: {topic}.
The response must be in a JSON format structured as follows:
{{
    "title": "Report Title",
    "sections": [
        {{
            "heading": "Section Heading",
            "content": "Section content in plain text."
        }}
    ]
}}

Include the following sections in order:

1. **Executive Summary**:
    - Brief overview of the topic.
    - Key findings and recommendations.
    - Value proposition.

2. **Background**:
    - Context and scope.
    - Importance and impact.
    - Report objectives.

3. **Current Situation Analysis**:
    - Market/field analysis.
    - Relevant data and statistics.
    - Key indicators and trends.

4. **Challenges and Opportunities**:
    - Key challenges identification.
    - Available opportunities.
    - Risk assessment.

5. **Solutions and Proposals**:
    - Practical solutions to challenges.
    - Options evaluation.
    - Implementation requirements.

6. **Action Plan and Recommendations**:
    - Proposed implementation steps.
    - Expected timeline.
    - Success metrics.

7. **Conclusion and Next Steps**:
    - Key points summary.
    - Final recommendations.
    - Proposed next steps.

Content Requirements:
- Focus on results and practical solutions.
- Use clear, professional language.
- Emphasize actionable insights.
- Support recommendations with data.
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
    doc_type = input("Enter the document type (academic/report): ")
    filename = f"research_{topic.replace(' ', '_').lower()}_{lang}_{doc_type}.docx"
    
    print(f"\nGenerating research content about '{topic}' in {lang}...")
    content = generate_research_content(topic, lang, doc_type)
    
    if content:
        print("\nCreating Word document...")
        result = create_document(content, filename, lang)
        print(result)
    else:
        print("Failed to generate content. Please try again.")

if __name__ == "__main__":
    main()
