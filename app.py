from flask import Flask, render_template
import pandas as pd
import requests
import re
import matplotlib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import pandas as pd
from cgitb import text
import string
import matplotlib.pyplot as plt
import numpy as np
from cProfile import label
import calendar
from io import BytesIO
import base64
import requests


# #don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here

def findAll(page_no) :
    url = "https://www.kalibrr.id/job-board/te/data/co/Indonesia/"
    pageFilter = "?sort=Freshness"

    url_get = requests.get(url+str(page_no))

    soup = BeautifulSoup(url_get.content,"html.parser")

    findAll = soup.find_all('div', attrs={'class':'k-grid k-border-tertiary-ghost-color k-text-sm k-p-4 md:k-p-6 css-1b4vug6'})
    #print(len(findAll))
    return findAll

def pre_text(pretext):

    pretext = pretext.lower()
    pretext = pretext.translate(str.maketrans('', '', string.punctuation))
    pretext = ' '.join(pretext.split())
    pretext = pretext.strip()
    return pretext
def find(job) :

    job_company = job.select_one('div.k-col-start-3.k-row-start-3 a')
    if job_company is not None :
        # print('Company :',job_company.text.strip())
        job_company = pre_text(job_company.text)

    # for job_titles :
    job_title = job.select_one('div.k-col-start-3.k-row-start-1 h2 a')
    if job_title is not None:
        # print('Position :',job_title.text.strip())
        job_title = pre_text(job_title.text)

    # for job_locations :
    job_location = job.select_one('div.k-col-start-3.k-row-start-3 a.k-text-subdued.k-block')
    if job_location is not None :
        job_location = job_location.text.replace('\n', "").replace(',', '').strip()
        
        job_location = re.sub(r"\b(?:Indonesia|City|Kota|Kabupaten|Regency)\b", "", job_location, flags=re.IGNORECASE).strip()
        # print('Location :',job_location)
    
    # for date info     
    posted_info = job.select_one('div.k-col-start-5.k-row-start-1 span:first-of-type')
    if posted_info is not None :
        posted_info = posted_info.text.strip()
        published_at, application_deadline = posted_info.split("• Apply before")
        published_at = published_at.replace('ago', '').replace('Posted', '').strip()
        application_deadline = application_deadline.strip()

    job_data = [job_company, job_title, job_location, published_at, application_deadline]
    return job_data

def save_file() :
    i = 0

    job_desc = findAll(page_no=page)
    # print("Total Save :",len(job_desc))

    for job in job_desc :
        i = i + 1
        job_info = find(job)
        csv.write(job_info[0]+ ',' + job_info[1] + ',' + job_info[2] + ',' + job_info[3] + "," + job_info[4]+ '\n')
        # print("save",i)

csv=open("db_kalibrr.csv", 'w')
headers = "Company,Title,Location,Published_At,Application_Deadline\n"
csv.write(headers)


for page in range(1,29):

    print('Page :',page)

    save_file()

print('Scraping is successful !!')

csv.close()

#change into dataframe
df = pd.read_csv('db_kalibrr.csv')

#insert data wrangling here
df.drop_duplicates(inplace=True)
df.duplicated().value_counts()
df = df[~df['Location'].str.contains('Philippines')]

from cProfile import label

df_1 = df.copy()

# Replace values in 'Location' column with 'Jakarta' if they match any value in 'kota_ubah' for Jakarta
kota_ubah_jkt = df_1[df_1['Location'].str.contains('jakarta', case=False)]
replace_dict_jkt = {k: 'Jakarta' for k in kota_ubah_jkt['Location'].unique()}
df_1['Location'] = df_1['Location'].replace(replace_dict_jkt)

# Replace values in 'Location' column with 'Tangerang' if they match any value in 'kota_ubah' for Tangerang
kota_ubah_tgr = df_1[df_1['Location'].str.contains('tangerang', case=False)]
replace_dict_tgr = {k: 'Tangerang' for k in kota_ubah_tgr['Location'].unique()}
df_1['Location'] = df_1['Location'].replace(replace_dict_tgr)

# Replace values in 'Location' column with 'Tangerang' if they match any value in 'kota_ubah' for Tangerang
kota_ubah_tgr = df_1[df_1['Location'].str.contains('Lampung', case=False)]
replace_dict_tgr = {k: 'Lampung' for k in kota_ubah_tgr['Location'].unique()}
df_1['Location'] = df_1['Location'].replace(replace_dict_tgr)

# Sort and count the values in the 'Location' column
city_dict = df_1['Location'].sort_values(ascending=False).value_counts()
city_dict = city_dict.head()

df_1['Location'] = df_1['Location'].astype('category')

# fungsi untuk mengubah nilai menjadi timedelta jika dapat diubah
def to_timedelta(val):
    try:
        return pd.Timedelta(val)
    except:
        pass
    try:
        if 'years' in val:
            val = val.replace('years', '').strip()
            return int(val) * pd.Timedelta(days=365)
        if 'year' in val:
            val = val.replace('year', '').strip()
            return int(val) * pd.Timedelta(days=365)
        if 'months' in val:
            val = val.replace('months', '').strip()
            return int(val) * pd.Timedelta(days=30)
        if 'days' in val:
            val = val.replace('days', '').strip()
            return pd.Timedelta(days=int(val))
        if 'month' in val:
            return pd.Timedelta(days=30)
        if 'day' in val:
            return pd.Timedelta(days=1)
        # if 'hours' in val:
        #     return pd.Timedelta(days=1)
        if 'minute' in val:
            val = val.replace('minute', '').strip()
            return pd.Timedelta(minutes=int(val))
        if 'minutes' in val:
            val = val.replace('minutes', '').strip()
            return pd.Timedelta(minutes=int(val))
        if 'hour' in val:
            val = val.replace('an', '1').replace('hour', '').strip()
            return pd.Timedelta(minutes=int(val))
        if 'hours' in val:
            val = val.replace('hours', '').strip()
            return pd.Timedelta(minutes=int(val))
    except:
        pass
    return np.nan

now = pd.Timestamp.now()
# konversi kolom posted_date menjadi timedelta
df_1['Posted_Date'] = df_1['Published_At'].apply(to_timedelta)
df_1['Posted_Date'] = now - df_1['Posted_Date']
df_1['Posted_Date'] = df_1['Posted_Date'].apply(lambda x: x.strftime('%d-%m-%Y'))
df_1['Posted_Date'] = pd.to_datetime(df_1['Posted_Date'], format='%d-%m-%Y')

df_1['publish_month'] = df_1['Posted_Date'].dt.month_name()
df_1['publish_month'].value_counts().sort_index(level=['publish_month'], ascending=True)

df_1 = df_1[df_1['Posted_Date'].dt.year == 2023]
df_1['Posted_Date'].value_counts().sort_index(level=['Posted_Date'], ascending=True)
post_month = df_1['publish_month'].value_counts().sort_index()
post_month = post_month.sort_values(key=lambda x: [list(calendar.month_name).index(i) for i in x.index])
month_dict = {
    'Jan': 'January',
    'Feb': 'February',
    'Mar': 'March',
    'Apr': 'April',
    'May': 'May',
    'Jun': 'June',
    'Jul': 'July',
    'Aug': 'August',
    'Sep': 'September',
    'Oct': 'October',
    'Nov': 'November',
    'Dec': 'December'
}
df_1['Application_Deadline'] = df_1['Application_Deadline'].apply(lambda x: ' '.join([month_dict[i] if i in month_dict else i for i in x.split()]))
df_1['Deadline_Date'] = df_1['Application_Deadline'].apply(lambda x: x + ' 2023')
df_1['Deadline_Date'] = pd.to_datetime(df_1['Deadline_Date'], format='%d %B %Y')

df_1['deadline_month'] = df_1['Deadline_Date'].dt.month_name()
df_1['deadline_month'].value_counts().sort_index(level=['deadline_month'], ascending=True)

deadline_month = df_1['deadline_month'].value_counts().sort_index()
deadline_month = deadline_month.sort_values(key=lambda x: [list(calendar.month_name).index(i) for i in x.index])
# Menambahkan bulan Januari, Februari, dan Maret dengan nilai 0
deadline_month = deadline_month.reindex(calendar.month_name[1:], fill_value=0)
deadline_month = deadline_month.sort_values(key=lambda x: [list(calendar.month_name).index(i) for i in x.index])

#Data Objek Series yang ditampilkan di web
city_dict
post_month
deadline_month
#end of data wranggling 

#Setting Bar
colors = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']



@app.route("/")
def index(): 
	
	card_data = f'{city_dict}'
	card_data1 = f'{post_month}'
	card_data2 = f'{deadline_month}'#be careful with the " and ' 

	# generate plot
	fig, ax = plt.subplots(figsize=(15, 9))
	ax.bar(city_dict.index, city_dict.values, color=colors)
	# plt.bar(city_dict.index, city_dict.values, color='#2a9d8f')
    # menambahkan angka hasil data ke diagram
	for x, y in zip(city_dict.index, city_dict.values):
		plt.text(x, y, str(y), ha='center', va='bottom')
	
	
	# Rendering plot
    
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True, dpi=100, width=500)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]
        
	fig, ax = plt.subplots(figsize=(15, 9))
	ax.bar(post_month.index,post_month.values, color=colors)
	# plt.bar(post_month.index, post_month.values, color='#2a9d8f')
	# menambahkan angka hasil data ke diagram
	for x, y in zip(post_month.index, post_month.values):
		plt.text(x, y, str(y), ha='center', va='bottom')
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True, dpi=100, width=500)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result1 = str(figdata_png)[2:-1]


	fig, ax = plt.subplots(figsize=(15, 9))
	# ax.bar(deadline_month.index, deadline_month.values, color=colors)
	plt.plot(deadline_month.index, deadline_month.values, color='#2a9d8f')
    # menambahkan angka hasil data ke diagram
	for x, y in zip(deadline_month.index, deadline_month.values):
		plt.text(x, y, str(y), ha='center', va='bottom')
                
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True, dpi=100, width=500)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result2 = str(figdata_png)[2:-1]
        
	# render to html
	return render_template('index.html',
		card_data = card_data,
        card_data1 = card_data1, 
        card_data2 = card_data2, 
		plot_result=plot_result,
        plot_result1=plot_result1,
        plot_result2=plot_result2
		)


if __name__ == "__main__": 
    app.run(debug=True)