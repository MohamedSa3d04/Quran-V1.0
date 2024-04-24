import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout='wide')
df = pd.read_csv('hafs_smart_v8.csv', low_memory=False, index_col='id', usecols=['id','aya_text_emlaey','sura_name_ar','aya_no','jozz','sura_no'])
df['aya_text'] = pd.read_csv('./quran_emlay')['text'].values
df = df[['sura_name_ar','aya_text','aya_text_emlaey','aya_no','jozz','sura_no']]

def t():
    if 'counter' in st.session_state:
     st.session_state.clear()
sb = st.sidebar
sb.markdown("<p style='font-size:30px; font-family : Arabic Typesetting;'>قراءة القرءان</p>", unsafe_allow_html=True)
suraname = sb.selectbox('Enter Sura Name - أدخل اسم السورة:',df['sura_name_ar'].unique(), on_change=t)

ExamOrNot = sb.selectbox('الإختبار في السورة ؟ ',['لا','نعم'], on_change=t)
ExamOrNot = True if ExamOrNot =='نعم' else False
if ExamOrNot:
    Easy = sb.selectbox('حدد نوع الإختبار : ',['سهل','صعب'], on_change=t)
    Easy = True if Easy == 'سهل' else False

sb.markdown("Made with [Eng/Mohamed Saad](https://www.facebook.com/profile.php?id=61557483869983):heart_eyes:")

st.markdown(f"<p style='margin : -38px 0px; font-size:50px; font-family : Arabic Typesetting; color:#86EE7C;  direction: rtl;'>اسم السورة : {suraname}</p>", unsafe_allow_html=True)
suraNumber = df[df['sura_name_ar'] == suraname]['sura_no'].values[0]
st.markdown(f"<p style='font-size:50px; font-family : Arabic Typesetting; color:#86EE7C;  direction: rtl;'>رقم السورة : {suraNumber}</p>", unsafe_allow_html=True)


sura_ayat = df[df['sura_name_ar'] == f'{suraname}']['aya_text'].values
ayat_numbers = len(sura_ayat)
st.markdown(f"<p style='margin : -38px 0px -20px 0; font-size:50px; font-family : Arabic Typesetting; color:#86EE7C;  direction: rtl;'>عدد الآيات: {ayat_numbers}</p>", unsafe_allow_html=True)
aya_no = 0

if ExamOrNot:
    rand_aya = np.random.choice(sura_ayat)
    if 'rand_aya' not in st.session_state or 'counter' not in st.session_state or 'ques_num' not in st.session_state:
      st.session_state['rand_aya'] = rand_aya
      st.session_state['counter'] = 0
      st.session_state['ques_num'] = 0

    st.markdown(f"<p style='margin : 0px 0px -38px 0px; font-size:50px; font-family : Arabic Typesetting; color:red;  direction: rtl;'>السؤال رقم : {st.session_state['ques_num']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin : 0px 0px -38px 0px; font-size:50px; font-family : Arabic Typesetting; color:red;  direction: rtl;'>أكمل من قوله تعالى : </p>", unsafe_allow_html=True)
    
        
    def next_aya():
        global rand_aya
        rand_aya = st.session_state['rand_aya']
        index = df[df['aya_text'] == rand_aya].index[0]
        rand_aya = df.iloc[index]['aya_text']
        st.session_state['rand_aya'] = rand_aya
        if not Easy:
            st.session_state['counter'] += 1
        
        
    def prev_aya():
        global rand_aya
        rand_aya = st.session_state['rand_aya']
        index = df[df['aya_text'] == rand_aya].index[0]
        rand_aya = df.iloc[index-2]['aya_text']
        st.session_state['rand_aya'] = rand_aya
        if not Easy:
            st.session_state['counter'] -= 1

    def next_ques():
        global rand_aya
        st.session_state['rand_aya'] = np.random.choice(sura_ayat)
        st.session_state['ques_num'] += 1
        st.session_state['counter'] = 0

    def skip_ques():
        global rand_aya
        st.session_state['rand_aya'] = np.random.choice(sura_ayat)
        st.session_state['counter'] = 0
        
    if Easy:
      s = f"<p style='font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{st.session_state['rand_aya']}</p>"
      st.markdown(s, unsafe_allow_html=True)
    else:
        if st.session_state['counter'] == 0:
            aya = st.session_state['rand_aya'].split(" ")
            aya = aya[:2] if len(aya) < 5 else aya[:5]
            aya = " ".join(aya) 
            aya += '...'
            s = f"<p style='font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{aya}</p>"
            st.markdown(s, unsafe_allow_html=True)
        else:
            s = f"<p style='font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{st.session_state['rand_aya']}</p>"
            st.markdown(s, unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns((20,20,20,10))
    c1.button('الآية التالية', on_click=next_aya)   
    c2.button('الآية السابقة', on_click=prev_aya)   
    c3.button('السؤال التالي', on_click=next_ques)   
    c4.button('تخطي السؤال', on_click=skip_ques)   
    

              


else:
    for aya in sura_ayat:
        aya_no += 1
        s = f"<p style='font-size:50px; font-family : Arabic Typesetting;  direction: rtl;'>{aya} ({aya_no})</p>"
        st.markdown(s, unsafe_allow_html=True)    
        st.divider()

