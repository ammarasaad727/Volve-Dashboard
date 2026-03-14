import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px

# --- إعدادات الصفحة (يفضل وضعها أولاً) ---
st.set_page_config(page_title="Volve Field Analytics", page_icon="🛢️", layout="wide")


# ==========================================
# --- قسم الشعارات والصور الشخصية (sidebar) ---
# ==========================================

# 1. لوغو منصة PetroScience في الأعلى
# ملاحظة: استبدل 'url_to_petroscience_logo.png' برابط مباشر للصورة (PNG or JPG)
petroscience_logo_url = "https://media.licdn.com/dms/image/v2/D5603AQGFR4yZ0Xbu8g/profile-displayphoto-crop_800_800/B56Zxrp.xPKgAI-/0/1771332696686?e=1775088000&v=beta&t=d08ng5-dwtD7Q6PF_QoYD8l5u9aDtzW0qTdUojcj7_E" # <--- ضع الرابط هنا
st.sidebar.image(petroscience_logo_url, use_container_width=True)

st.sidebar.markdown("---") # خط فاصل

# 2. صورتك الشخصية والاسم
# ملاحظة: استبدل 'url_to_your_photo.jpg' برابط مباشر لصورتك
my_photo_url = "https://media.licdn.com/dms/image/v2/D4D03AQH_gUWhtKDArA/profile-displayphoto-crop_800_800/B4DZxtywF.HwAI-/0/1771368594658?e=1775088000&v=beta&t=t9DpZwE5y5X6nx_u2Atyrb1h9DSUaftqn6AtSMEmT7s" # <--- ضع الرابط هنا
col1, col2 = st.sidebar.columns([1, 3]) # تقسيم السطر لصورة صغيرة واسم
with col1:
    st.image(my_photo_url, width=60) # عرض الصورة بعرض 60 بكسل
with col2:
    st.write("### المهندس عمار أسعد")
    st.write("مطور التطبيق")

st.sidebar.markdown("---") # 

st.header("Ammar Asaad")
st.caption("📊 التحليل الذكي لأداء آبار حقل Volve")
st.sidebar.info("""
هذا التطبيق يحلل بيانات حقل Volve (بحر الشمال). 
تم تطويره بواسطة المهندس عمار أسعد لتمكين المهندسين 
من مراقبة أداء الآبار لحظياً.
""")
# إضافة معلومات التواصل في القائمة الجانبية
st.sidebar.markdown("---") # خط فاصل
st.sidebar.title("📩 تواصل معي")

# رابط لينكد إن
linkedin_url = "https://www.linkedin.com/in/ammar-asaad/" # تأكد من وضع رابط حسابك الصحيح هنا
st.sidebar.markdown(f'[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin)]({linkedin_url})')

# البريد الإلكتروني
email = "ammarasaad727@gmail.com" # ضع إيميلك هنا
st.sidebar.write(f"📧: {email}")

st.sidebar.markdown("---")
st.sidebar.info("تم تطوير هذا التطبيق بواسطة المهندس عمار أسعد")


#st.dataframe(df)

# 1. قراءة البيانات
df = pd.read_excel('Volve production data.xlsx')

# 2. تحويل عمود التاريخ لتنسيق صحيح (مهم جداً للرسم)
df['DATEPRD'] = pd.to_datetime(df['DATEPRD'])

# 3. إضافة قائمة لاختيار البئر (تفاعلية)
well_names = df['NPD_WELL_BORE_NAME'].unique() # الحصول على أسماء الآبار بدون تكرار
selected_well = st.selectbox("اختر البئر المراد عرضه:", well_names)

# 4. تصفية البيانات بناءً على البئر المختار
df_filtered = df[df['NPD_WELL_BORE_NAME'] == selected_well]

# 5. ترتيب البيانات حسب التاريخ لضمان انسيابية الخط
df_filtered = df_filtered.sort_values('DATEPRD')

# 6. رسم البيانات المصفاة فقط
st.subheader(f"Pressure over Time for Well: {selected_well}")
# رسم ضغط البئر باستخدام Plotly
fig_pressure = px.line(df_filtered, x='DATEPRD', y='AVG_DOWNHOLE_PRESSURE', 
                       title=f'Pressure over Time for Well: {selected_well}')
st.plotly_chart(fig_pressure)

# رسم إنتاج النفط باستخدام Plotly
fig_oil = px.line(df_filtered, x='DATEPRD', y='BORE_OIL_VOL', 
                  title=f'Oil Production over Time for Well: {selected_well}')
fig_oil.update_traces(line_color='green') # تغيير لون خط النفط للأخضر
st.plotly_chart(fig_oil)

import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة لتكون واسعة (Wide Mode) لتناسب البيانات الضخمة
st.set_page_config(page_title="Volve Field Analytics", layout="wide")

st.title("📊 Volve Field Production Dashboard")
st.markdown("---")

# 1. قراءة البيانات (تأكد من وجود الملف في نفس المجلد)
@st.cache_data # هذه الخاصية تجعل الموقع سريعاً جداً عند تحميل البيانات الضخمة
def load_data():
    df = pd.read_excel('Volve production data.xlsx')
    df['DATEPRD'] = pd.to_datetime(df['DATEPRD'])
    return df

df = load_data()

# --- القائمة الجانبية (Sidebar) للتصفية ---
st.sidebar.header("لوحة التحكم")
well_names = df['NPD_WELL_BORE_NAME'].unique()
selected_well = st.sidebar.selectbox("اختر البئر:", well_names)

# تصفية البيانات بناءً على الاختيار
df_filtered = df[df['NPD_WELL_BORE_NAME'] == selected_well].sort_values('DATEPRD')

# --- القسم الأول: مؤشرات الأداء الرئيسية (KPIs) ---
st.subheader(f"📍 ملخص أداء البئر: {selected_well}")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_oil = df_filtered['BORE_OIL_VOL'].sum()
    st.metric("إجمالي إنتاج النفط (Sm3)", f"{total_oil:,.0f}")
with col2:
    avg_pressure = df_filtered['AVG_DOWNHOLE_PRESSURE'].mean()
    st.metric("متوسط الضغط (psig)", f"{avg_pressure:,.1f}")
with col3:
    max_gas = df_filtered['BORE_GAS_VOL'].max()
    st.metric("أعلى إنتاج غاز يومي", f"{max_gas:,.0f}")
with col4:
    days_on_stream = len(df_filtered[df_filtered['ON_STREAM_HRS'] > 0])
    st.metric("عدد أيام الإنتاج", days_on_stream)

st.markdown("---")

# --- القسم الثاني: الرسوم البيانية التفاعلية (Tabs) ---
tab1, tab2, tab3 = st.tabs(["📈 منحنيات الإنتاج", "🌡️ الضغط والحرارة", "💾 البيانات الكاملة"])

with tab1:
    st.subheader("تحليل حجم الإنتاج (نفط، غاز، ماء)")
    fig_prod = px.line(df_filtered, x='DATEPRD', y=['BORE_OIL_VOL', 'BORE_GAS_VOL', 'BORE_WAT_VOL'],
                      labels={'value': 'Volume', 'DATEPRD': 'Date'},
                      title=f"Production Profile - {selected_well}")
    st.plotly_chart(fig_prod, use_container_width=True)

with tab2:
    st.subheader("تحليل الضغط والحرارة في قاع البئر")
    fig_press = px.scatter(df_filtered, x='DATEPRD', y='AVG_DOWNHOLE_PRESSURE', 
                           color='AVG_DOWNHOLE_TEMPERATURE',
                           title=f"Pressure vs Temperature - {selected_well}")
    st.plotly_chart(fig_press, use_container_width=True)

with tab3:
    st.subheader("جدول البيانات الخام المستخرجة")
    st.write(f"يعرض هذا الجدول جميع السجلات لعام {df_filtered['DATEPRD'].dt.year.min()} إلى {df_filtered['DATEPRD'].dt.year.max()}")
    st.dataframe(df_filtered) # عرض الجدول بشكل تفاعلي يمكن البحث فيه

# إضافة زر لتحميل البيانات المصفاة كملف CSV
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button("تحميل بيانات هذا البئر (CSV)", data=csv, file_name=f"{selected_well}_data.csv")
