from flask import Flask, render_template, request, send_file, url_for
import os
from main import generate_research_content, create_document
import traceback

app = Flask(__name__)

# Ensure the Researchs directory exists
RESEARCH_DIR = os.path.join(os.path.dirname(__file__), 'Researchs')
os.makedirs(RESEARCH_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form.get('topic', '')
        doc_type = request.form.get('doc_type', 'academic')
        lang = request.form.get('lang', 'ar')
        instructions = request.form.get('instructions', '')
        
        if not topic:
            return render_template('index.html', error="يرجى إدخال الموضوع")
        
        try:
            content = generate_research_content(topic, lang, doc_type, instructions)
            if not content:
                return render_template('index.html', error="حدث خطأ في إنشاء المحتوى")
                
            filename = f"{doc_type}_{topic.replace(' ', '_').lower()}_{lang}.docx"
            filepath = os.path.join(RESEARCH_DIR, filename)
            create_document(content, filepath, lang)
            return render_template('index.html', success=f"تم إنشاء المستند بنجاح: {filename}")
            
        except Exception as e:
            return render_template('index.html', error=f"حدث خطأ: {str(e)}")
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join(RESEARCH_DIR, filename)
        if not os.path.exists(filepath):
            return render_template('index.html', 
                error="عذراً، الملف غير موجود. يرجى إعادة إنشاء المستند.")
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return render_template('index.html', 
            error="عذراً، حدث خطأ أثناء تحميل الملف. يرجى المحاولة مرة أخرى.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
