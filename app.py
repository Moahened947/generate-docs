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
        try:
            topic = request.form['topic']
            lang = request.form.get('lang', 'ar')  # Default to Arabic
            doc_type = request.form.get('doc_type', 'academic')  # Default to academic
            
            if not topic:
                return render_template('index.html', error="يرجى إدخال موضوع المستند")
            
            filename = f"{doc_type}_{topic.replace(' ', '_').lower()}_{lang}.docx"
            filepath = os.path.join(RESEARCH_DIR, filename)
            content = generate_research_content(topic, lang, doc_type)
            
            if content:
                create_document(content, filepath, lang)
                success_message = "تم إنشاء المستند بنجاح!"
                return render_template('index.html', 
                    success=success_message,
                    topic=topic,
                    lang=lang,
                    doc_type=doc_type,
                    download_file=filename)
            else:
                return render_template('index.html', 
                    error="عذراً، حدث خطأ أثناء إنشاء المحتوى. يرجى المحاولة مرة أخرى.",
                    topic=topic,
                    lang=lang,
                    doc_type=doc_type)
                
        except Exception as e:
            print(f"Error: {str(e)}")
            print(traceback.format_exc())
            return render_template('index.html', 
                error="عذراً، حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.",
                topic=topic if 'topic' in locals() else '',
                lang=lang if 'lang' in locals() else 'ar',
                doc_type=doc_type if 'doc_type' in locals() else 'academic')
    
    return render_template('index.html', lang='ar', doc_type='academic')

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
