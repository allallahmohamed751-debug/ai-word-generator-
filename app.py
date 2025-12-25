import streamlit as st
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import google.generativeai as genai
import io

st.set_page_config(page_title="FormatFixer Gemini", page_icon="✨")
st.title("FormatFixer AI ✨")

with st.sidebar:
    st.header("الإعدادات ⚙️")
    gemini_api_key = st.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")
    st.info("احصل على مفتاحك من: aistudio.google.com")

topic = st.text_input("عن ماذا تريدني أن أكتب اليوم؟")

if st.button("توليد وتنسيق الملف 🪄"):
    if not gemini_api_key:
        st.error("الرجاء إدخال المفتاح أولاً!")
    elif topic:
        try:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"اكتب مقالاً منسقاً بالعربية عن: {topic}")
            
            doc = Document()
            for line in response.text.split('\n'):
                p = doc.add_paragraph(line)
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT # تنسيق للعربية
            
            bio = io.BytesIO()
            doc.save(bio)
            st.success("تم التوليد!")
            st.download_button("تحميل ملف Word 📥", data=bio.getvalue(), file_name=f"{topic}.docx")
        except Exception as e:
            st.error(f"خطأ: {e}")
