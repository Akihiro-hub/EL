import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import PyPDF2
import re
import bleach

# Streamlit UIの設定
st.write("## :blue[Análisis de Texto o Documento]") 
st.write("Puede elaborar Nube de Palabras (WordCloud), figura visual donde las palabras frecuentes o importantes en un texto se presentan de manera destacada. Se usa en muchos proyectos de Inteligencia Artificial.")
st.write("##### :green[Paso 1: Pegue el texto para el análisis o suba un archivo PDF.]")

# テキストエリアとPDFファイルアップロードのオプション
col1, col2 = st.columns(2)
with col1:
    texto = st.text_area("Pegue aquí el texto a analizar", "")
with col2: 
    pdf_file = st.file_uploader("O, sube un archivo PDF a analizar, como segunda opción", type="pdf")

# 除外したい単語の入力
st.write("##### :green[Paso 2: Note abajo las palabras que deben excluirse del análisis, si las tiene.]")
col1, col2, col3 = st.columns(3)
with col1:
    exclude_word1 = bleach.clean(st.text_input("Palabra a excluir 1", ""))
    exclude_word2 = bleach.clean(st.text_input("Palabra a excluir 2", ""))
with col2:
    exclude_word3 = bleach.clean(st.text_input("Palabra a excluir 3", ""))
    exclude_word4 = bleach.clean(st.text_input("Palabra a excluir 4", ""))
with col3:
    exclude_word5 = bleach.clean(st.text_input("Palabra a excluir 5", ""))
    exclude_word6 = bleach.clean(st.text_input("Palabra a excluir 6", ""))
st.write("Esta aplicación se mantiene durante el período del Proyecto GuateCrece.")

# デフォルトで除外する単語のリスト
default_excluded_words = {
    "la", "el", "los", "las", "él", "ella", "en", "de", "del", "un", "que", "soy", "eres", "es", "somos", "son",
    "estoy", "estás", "le", "poder", "hace", "año", "mes", "he", "estado", "había", "años", "meses", "sobre", 
    "gusta", "me", "mi", "su", "opiniones", "sugerencias", "calificación", "respuesta", "propietario", "dueño", "negocio",
    "está", "estamos", "están", "este", "aquello", "aquella", "esta", "estas", "estos", "cual", "y", "ya", "hay", "a", "al",
    "lo", "desde", "hasta", "hacia", "usted", "tú", "yo", "compartir", "con", "para", "su", "nuestro", "sea", "sean", "esté", "estén", 
    "o", "u", "e", "por", "eso", "foto", "fotos", "local", "reseñas", "más", "mas", "nos", "os", "ser", "estar", "sí", "si", "estuviese", "estuviera",
    "no", "ni", "guide", "hay", "se", "una", "uno", "fuí", "fue", "fuera", "fuese", "hubiera", "estaba", "estaban", "estuve", "estuvo", "estuvieron"
}

# 入力された除外単語をセットに追加
user_excluded_words = {exclude_word1, exclude_word2, exclude_word3, exclude_word4, exclude_word5, exclude_word6}
excluded_words = default_excluded_words.union(user_excluded_words)

if pdf_file:
    # PDFからテキストを抽出
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    texto = ""
    for page in pdf_reader.pages:
        texto += page.extract_text()

# サニタイズされたテキスト
texto = bleach.clean(texto)

if texto:
    # テキストのトークン化と前処理
    words = re.findall(r'\b\w+\b', texto.lower())
    filtered_words = [word for word in words if word not in excluded_words]

    # Word Cloudの作成
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(filtered_words))

# 分析ボタンの表示
if st.button("Analizar"):

    # Word Cloudの表示
    st.subheader("Nube de Palabras (WordCloud)")
    st.write("WordCloud es útil para visualizar la importancia relativa de términos dentro de un texto de manera rápida y comprensible.")

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
    
    # 頻出する単語の組み合わせ
    st.subheader("Combinaciones de palabras observadas con cierta frecuencia")
    bigram_freq = Counter(list(zip(filtered_words[:-1], filtered_words[1:])))

    col1, col2 = st.columns(2)
    with col1:
        st.write("##### :blue[Bigrams observados:]")
        for bigram, freq in bigram_freq.most_common(3):
            st.write(f"{' '.join(bigram)}: {freq}")
