import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="OLC Dashboard",
    page_icon="📊",
    layout="wide"
)

# Backend URL
BACKEND_URL = "https://olc-backend.onrender.com/api/v1"

# Başlık
st.title("📊 OLC Dashboard")
st.markdown("**Haber Analiz Gösterge Paneli**")
st.divider()

# Veri çek
try:
    response = requests.get(f"{BACKEND_URL}/haberler", timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        haberler = data['haberler']
        
        # DataFrame oluştur
        df = pd.DataFrame(haberler)
        
        # Sadece AI işlenmiş haberleri al
        df_ai = df[df['flash_ozet'].notna() & (df['flash_ozet'] != '')]
        
        # --- ÜSTTE METRIKLER ---
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📰 Toplam Haber",
                len(df),
                delta=f"+{len(df_ai)} AI İşlenmiş"
            )
        
        with col2:
            sentiment_counts = df_ai['sentiment_label'].value_counts()
            most_common = sentiment_counts.index[0] if len(sentiment_counts) > 0 else "N/A"
            st.metric(
                "😊 En Çok Duygu",
                most_common.capitalize(),
                delta=f"{sentiment_counts.iloc[0]} haber"
            )
        
        with col3:
            category_counts = df['kategori'].value_counts()
            most_category = category_counts.index[0] if len(category_counts) > 0 else "N/A"
            st.metric(
                "📂 En Aktif Kategori",
                most_category.capitalize(),
                delta=f"{category_counts.iloc[0]} haber"
            )
        
        with col4:
            ai_percentage = (len(df_ai) / len(df) * 100) if len(df) > 0 else 0
            st.metric(
                "🤖 AI İşlenme Oranı",
                f"{ai_percentage:.1f}%",
                delta=f"{len(df_ai)}/{len(df)}"
            )
        
        st.divider()
        
        # --- GRAFİKLER ---
        col_left, col_right = st.columns(2)
        
        with col_left:
            # 1. SENTIMENT PIE CHART
            st.subheader("😊 Duygu Dağılımı")
            
            sentiment_data = df_ai['sentiment_label'].value_counts().reset_index()
            sentiment_data.columns = ['Duygu', 'Sayı']
            
            # Emoji ekle
            emoji_map = {'olumlu': '😊', 'nötr': '😐', 'olumsuz': '😔'}
            sentiment_data['Duygu'] = sentiment_data['Duygu'].map(
                lambda x: f"{emoji_map.get(x, '')} {x.capitalize()}"
            )
            
            fig_sentiment = px.pie(
                sentiment_data,
                values='Sayı',
                names='Duygu',
                color='Duygu',
                color_discrete_map={
                    '😊 Olumlu': '#2ecc71',
                    '😐 Nötr': '#95a5a6',
                    '😔 Olumsuz': '#e74c3c'
                },
                hole=0.4
            )
            
            fig_sentiment.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Sayı: %{value}<br>Oran: %{percent}<extra></extra>'
            )
            
            fig_sentiment.update_layout(
                showlegend=True,
                height=400
            )
            
            st.plotly_chart(fig_sentiment, use_container_width=True)
        
        with col_right:
            # 2. KATEGORI BAR CHART
            st.subheader("📂 Kategori Dağılımı")
            
            category_data = df['kategori'].value_counts().reset_index()
            category_data.columns = ['Kategori', 'Sayı']
            
            # Emoji ekle
            category_emoji = {'spor': '⚽', 'teknoloji': '💻', 'borsa': '💰', 'kitap': '📚'}
            category_data['Kategori'] = category_data['Kategori'].map(
                lambda x: f"{category_emoji.get(x, '📰')} {x.capitalize()}"
            )
            
            fig_category = px.bar(
                category_data,
                x='Kategori',
                y='Sayı',
                color='Sayı',
                color_continuous_scale='Blues',
                text='Sayı'
            )
            
            fig_category.update_traces(
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Haber Sayısı: %{y}<extra></extra>'
            )
            
            fig_category.update_layout(
                showlegend=False,
                xaxis_title="",
                yaxis_title="Haber Sayısı",
                height=400
            )
            
            st.plotly_chart(fig_category, use_container_width=True)
        
        st.divider()
        
        # --- KAYNAK ANALİZİ ---
        col_left2, col_right2 = st.columns(2)
        
        with col_left2:
            # 3. KAYNAK DAĞILIMI
            st.subheader("📰 Kaynak Dağılımı")
            
            source_data = df['kaynak_adi'].value_counts().head(10).reset_index()
            source_data.columns = ['Kaynak', 'Sayı']
            
            fig_source = px.bar(
                source_data,
                x='Sayı',
                y='Kaynak',
                orientation='h',
                color='Sayı',
                color_continuous_scale='Greens',
                text='Sayı'
            )
            
            fig_source.update_traces(
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Haber: %{x}<extra></extra>'
            )
            
            fig_source.update_layout(
                showlegend=False,
                xaxis_title="Haber Sayısı",
                yaxis_title="",
                height=400
            )
            
            st.plotly_chart(fig_source, use_container_width=True)
        
        with col_right2:
            # 4. SENTIMENT X CATEGORY
            st.subheader("🎯 Kategori-Duygu Matrisi")
            
            # Pivot table oluştur
            pivot_data = df_ai.groupby(['kategori', 'sentiment_label']).size().reset_index(name='count')
            
            fig_matrix = px.bar(
                pivot_data,
                x='kategori',
                y='count',
                color='sentiment_label',
                barmode='group',
                color_discrete_map={
                    'olumlu': '#2ecc71',
                    'nötr': '#95a5a6',
                    'olumsuz': '#e74c3c'
                },
                labels={'count': 'Haber Sayısı', 'kategori': 'Kategori', 'sentiment_label': 'Duygu'}
            )
            
            fig_matrix.update_layout(
                xaxis_title="",
                yaxis_title="Haber Sayısı",
                legend_title="Duygu",
                height=400
            )
            
            st.plotly_chart(fig_matrix, use_container_width=True)
        
        st.divider()
        
        # --- EN ÇOK KULLANILAN KELİMELER ---
        st.subheader("🔑 En Çok Kullanılan Anahtar Kelimeler (Top 20)")
        
        # Anahtar kelimeleri topla
        all_keywords = []
        for keywords in df_ai['anahtar_kelimeler'].dropna():
            if isinstance(keywords, list):
                all_keywords.extend(keywords)
        
        if all_keywords:
            keyword_series = pd.Series(all_keywords)
            keyword_counts = keyword_series.value_counts().head(20).reset_index()
            keyword_counts.columns = ['Kelime', 'Frekans']
            
            fig_keywords = px.bar(
                keyword_counts,
                x='Frekans',
                y='Kelime',
                orientation='h',
                color='Frekans',
                color_continuous_scale='Purples',
                text='Frekans'
            )
            
            fig_keywords.update_traces(
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Kullanım: %{x}<extra></extra>'
            )
            
            fig_keywords.update_layout(
                showlegend=False,
                xaxis_title="Kullanım Sayısı",
                yaxis_title="",
                height=600
            )
            
            st.plotly_chart(fig_keywords, use_container_width=True)
        else:
            st.info("Henüz anahtar kelime verisi yok.")
        
        # --- HAM VERİ ---
        with st.expander("📋 Ham Veri Tablosu"):
            st.dataframe(
                df[['id', 'baslik', 'kategori', 'sentiment_label', 'kaynak_adi', 'olusturma_tarihi']],
                use_container_width=True
            )
        
    else:
        st.error(f"❌ Backend hata: {response.status_code}")
        
except Exception as e:
    st.error(f"❌ Bağlantı hatası: {str(e)}")
