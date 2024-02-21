import streamlit as st
import jdatetime 
from datetime import timedelta 
import datetime
import warnings 
import os 
import glob 
import pandas as pd




# ////////////////////////////// تابع های مورد نیاز
def convert_to_list(t):
    if isinstance(t, list):
        return t
    elif isinstance(t, tuple):
        return list(t)
    elif isinstance(t, pd.Series):
        return t.tolist()
    else :      # انگار این فقط میگه استرینگ باشه و دیکشنری باشه را اینجوری میده
        return [t]



def jalali_converter_lenmonth(input_month='اسفند',
                              value_want='the_number',
                             input_year=jdatetime.datetime.now().year,
                             ):
    
    the_month=jalali_converter(input_month) # اول تبدیل میکنیم اون ماهه را  به اینتیجر
    
    month_list=['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند' ]
    # لیست سالهای کبیسه جلالی که اسفندی کی اضافه بشه
    leap_years=[1346,1350,1354,1358,1362,1366,1370,1375,1379, 1383, 1387, 1391, 1395, 1399, 1403,1408,1412,1416,1420,1424,1428,1432,1436,1441,1445,1449,1453]
    # print(leap_years)
    month_days={}
    # بعد هر کدوم را میگیم اگه پیش از مهر بود بزار ماه را ۳۱ روزه 
    # اگه ماه ماه بین ۱۲ و ۷ بود ۳۰ روزه 
    # اگه ۱۲ هم بود ۲۹ روزه 
    # البته کبیسه ها را باید بعدا تبدیل کنم 
    for year in leap_years:   
        for month in month_list:
            if the_month<7  :
                day_list=list(range(1,32))
            elif 7< the_month<12:
                day_list=list( range(1,31))
            elif  the_month==12: 
                if input_year in leap_years:
                    day_list=list(range(1,31))
                else :
                    day_list=list(range(1,30))
            month_days[month] =day_list
        # حالا اگر لیست  روزها را خواست لیست را میده وگرنه که طول و تعداد را میده
        if value_want=='the_list':
            return month_days[input_month]
        elif value_want=='the_number':
            return len(month_days[input_month])



# تابعی که اگر هر چیزی بالاتر از ۶۰ بود ویا زیر صفر بود بزنه صفر 
# وگرنه همون مقدار را بزنه 
def setter_min_before_after(before_after,now_time=datetime.datetime.now().minute ): 
    new_minute=now_time+before_after  
    if new_minute <0 or new_minute>=60: 
        return 0  
    else: 
        return new_minute 

def setter_hour_before_after(before_after,now_time=datetime.datetime.now().hour ): 
    new_hour=now_time+before_after  
    if new_hour <0 or new_hour>=24: 
        return 0 
    else: 
        return new_hour 




# برای ورودی ها که به مرداد و تیر و.. میده باید برج را اورد
def jalali_converter(input_month=None):
    '''
    :param input_month:  اگر عدد را میدیم و ماه را میخوایم عدد را بصورت اینتیجر یعنی  2 میدیم واگر ماه را به حروف دادیم باید استرینگ باشه یعنی  'فروردین' '
    :return: خروجی عدد بود واژه میده و اگر واژه دادی عدد ماه را میده
    '''
    mah_be_borg={
        'فروردین': 1 ,
        'اردیبهشت':2 ,
        'خرداد':3 ,
        'تیر': 4,
        'مرداد': 5,
        'شهریور':6 ,
        'مهر': 7,
        'آبان':8 ,
        'آذر': 9,
        'دی': 10,
        'بهمن':11 ,
        'اسفند':12 ,
    }
    # اینم تبدیل برج به ماه
    borg_be_mah={ val:key for key , val in mah_be_borg.items()}
    if isinstance(input_month,str):
        return mah_be_borg[input_month]
    elif isinstance(input_month,int):
        return borg_be_mah[input_month]
# jalli_converter('مرداد')  #5
# jalli_converter(7) # 'مهر'



# ///////////



# # تابعی که تاریخ جلالی را با سلکت میسازه و خروجی را میده تاریخ انتخاب شده را میده به صورت جلالی یا میلادی
def Jalali_Streamlit_calendar(
    st_col=None,
    title='از چه بازه زمانی',
    frmt='gr',
    identifier='' ,# کلید های مختلفی از یک تابع با این میشه ساخت
    the_size=18,
    
    alignment = 'center',
    color='blue',
    default_day='today',
    format_datetime='datetime',
    
    step_min=1,
    default_min='sefr' ,
    # default_min='aknun' 
    # default_min=('before_after',-2) ,
    
    
    default_hour='aknun_h' ,
    # default_hour='sefr_h' 
    # default_hour=('before_after_h',-2) 
    step_hour=1
                               ):
    

        
    
    # این کلیدو میاریم که این ارور DuplicateWidgetID را نخوریم و یگانه باشند هر کلید
    year_widget_id = f"{title}_year_{identifier}"
    month_widget_id = f"{title}_month_{identifier}"
    day_widget_id = f"{title}_day_{identifier}"
    hour_wifget_id=f"{title}_hour_{identifier}"
    minute_wifget_id=f"{title}_minute_{identifier}"
    
    default_min_list=convert_to_list(default_min) 

    default_min_dict={ 
                'sefr':datetime.datetime.now().minute*0,
                 'aknun':datetime.datetime.now().minute,
                'before_after':setter_min_before_after(default_min_list[1] if default_min_list[0]=='before_after'  else 0  , now_time= datetime.datetime.now().minute) 
    }
    
    
    
    st_col.markdown(f"<h2 style='font-size:{the_size}px; text-align:{alignment}; color:{color};'>{title}:</h2>",
                  unsafe_allow_html=True) 
    
    now_time=jdatetime.datetime.now() 
    year_list=list(range(1380,1420)) 
    month_list=['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند' ]
    #  اینجا هم کلید را میاره که یگانه باشه
    year=st_col.selectbox('برگزیدن سال',year_list,index=year_list.index(now_time.year),key=year_widget_id) # تعین دیفالت
    month=st_col.selectbox( 'برگزیدن ماه' ,month_list,index=month_list.index(jalali_converter(now_time.month)),key=month_widget_id)
    # اون روزی که انتخاب میشه . اون بازه زمانی میاد بر اساس ماه
    
    day_list=jalali_converter_lenmonth(input_month=month,
                                       input_year=year,
                                       
                                       value_want='the_list')
    # اینو میزنیم که ماه ها که پیشفرضشون روی روزی است و عوض بشن دیگه مشکل نداشته باشن و امتحان کنه و نشد خودش بزاره روی اخری
    

    
    # زمان اکنون را برمیگزینیم
    if default_day=='today':
        try:
            day=st_col.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( now_time.day),key=day_widget_id)
        except:
            day=st_col.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( day_list[-1]),key=day_widget_id )
            
    elif default_day=='yesterday':
        try:
            day=st_col.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( (now_time.day)-1),key=day_widget_id)
        except:
            day=st_col.selectbox( 'برگزیدن روز' ,day_list,index=day_list.index( (day_list[-1])-1),key=day_widget_id )
    

    
    def setter_hour_before_after(before_after,now_time=datetime.datetime.now().hour ): 
        new_hour=now_time+before_after  
        if new_hour <0 or new_hour>=24: 
            return 0 
        else: 
            return new_hour 

    
    default_hour_list=convert_to_list(default_hour)
    default_hour_dict={ 
                'sefr_h':datetime.datetime.now().hour*0,
                 'aknun_h':datetime.datetime.now().hour,
                'before_after_h':setter_hour_before_after(default_hour_list[1] if default_hour_list[0]=='before_after_h'  else 0  ,now_time= datetime.datetime.now().hour) 
    } 
    # اگه فقط تاریخ و روز باشه اینو میاریم 
    if format_datetime=='date': 
        # تبدیل چیزی که اانتخاب شده به فرمت ها
        selected_date_jl=jdatetime.datetime.strptime(f"{year}/{jalali_converter(month)}/{day}","%Y/%m/%d" )
        selected_date_gr=pd.to_datetime(selected_date_jl.togregorian()).date()
        selected_date_jl=selected_date_jl.date()
    # اگه بخوایم ساعت هم باشه و دقیقه اینو میاریم
    if format_datetime=='datetime':
        the_hour = st_col.time_input('برگزیدن ساعت',
                  value=datetime.time(default_hour_dict[default_hour_list[0]]),
                  step=(timedelta(hours=step_hour)),
                  key=hour_wifget_id )
        
        minute_list=list(range(0,60,step_min))
        minute=st_col.selectbox( 'برگزیدن دقیقه' ,minute_list,index=minute_list.index(default_min_dict[default_min_list[0]]),key=minute_wifget_id)
    
        # چون فرمت خروجی تایم اینپوت دیت تایم هستش پس ما میایم بهش میگیم فقط ساعتو بده که اینتیجر هم هست
        selected_date_jl=jdatetime.datetime.strptime(f"{year}/{jalali_converter(month)}/{day} {the_hour.hour}:{minute}","%Y/%m/%d %H:%M" )  #1402-11-28 20:15:00 
        selected_date_gr=pd.to_datetime(selected_date_jl.togregorian()) #2024-02-17 20:00:00 
        
    #st_col.write(selected_date_jl)
    #st_col.write(selected_date_gr)
    # اگر فرمت گریگوری باشه
    if frmt=='gr':
        return selected_date_gr # هم میسازه و هم برمیگردونه موقع فراخوانی
    # اگه فرمتی که میخوایم جلالی باشه  
    elif frmt=='jl':
        return selected_date_jl
            








# ///////////////////// بکار بستن تابع -نمونه ---------------------------------------


warnings.filterwarnings('ignore')
st.set_page_config(page_title=' jalali calander streamlit ',
                  page_icon=':bar_chart',)

title_page='jalali calendar streamlit  '
alignment='center'
# ;color:{color};
color='white'
font_size=30
st.markdown(f"<h1 style='font-size:{font_size};text-align:{alignment};'>{title_page}</h1>",
           unsafe_allow_html=True
           )



col1,col2,col3,col4=st.columns(4)
# اینجا میگیم از در کجا باشه 
the_from=Jalali_Streamlit_calendar(
    st_col=col4,   # در چه ستونی از صفحه اصلی جابگیره
    title='از چه بازه زمانی',
    frmt='jl',
    identifier='' ,#  - اگه اینو نزاریم خطا میده چون باید  از  یک دکمه چند نمونه بداریم  - کلید های مختلفی از یک تابع با این میشه ساخت
    the_size=18,
    
    alignment = 'center',
    color='cyan',
    default_day='today',
    format_datetime='datetime',
    
    step_min=1,
    default_min='sefr' ,
    # default_min='aknun' 
    # default_min=('before_after',-2) ,
    
    
    default_hour='aknun_h' ,
    # default_hour='sefr_h' 
    # default_hour=('before_after_h',-2) 
    step_hour=1)

# اینجا هم مشخصات تا را میدیم. که یعنی تا چه بازه زملنی باشه
the_to=Jalali_Streamlit_calendar(
    st_col=col3,
    title='تا چه بازه زمانی',
    frmt='jl',
    identifier='' ,#  کلید های مختلفی از یک تابع با این میشه ساخت
    the_size=18,
    
    alignment = 'center',
    color='red',
    default_day='today',
    format_datetime='datetime',
    
    step_min=1,
    default_min='sefr' ,
    # default_min='aknun' 
    # default_min=('before_after',-2) ,
    
    
    default_hour='aknun_h' ,
    # default_hour='sefr_h' 
    # default_hour=('before_after_h',-2) 
    step_hour=1)



# حالا فقط نمایش در صفحه میدیم و هیچ ارزش دیگه نداره
st.write(the_from)
st.write(the_to)

#  توجه شود که استریم لیت در پانداس تاریخ جلالی را نمیشمارد و برای آن باید  ستون گریگوری معادل ساخت و ستون ها را تبدیل به گریگوری کرد و بعد با آن تاریخ را 
# فیلتر کرد و برای نمایش از جلالی استفاده کرد 

# کلک رشتی میزنیم  !!!!










