from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests
from cgitb import text
import string
import re



# #don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here

# #Find All
# def divElement(page_no) :
#     url = "https://www.kalibrr.id/job-board/te/data/co/Indonesia/"
#     pageFilter = "?sort=Freshness"

#     url_get = requests.get(url+str(page_no)+pageFilter)

#     soup = BeautifulSoup(url_get.content,"html.parser")

#     div_elements = soup.find_all('div', attrs={'class':'k-grid k-border-tertiary-ghost-color k-text-sm k-p-4 md:k-p-6 css-1b4vug6'})
#     # print(len(div_elements))
#     return div_elements

#Pre-text
def pre_text(pretext):

    pretext = pretext.lower()
    pretext = pretext.translate(str.maketrans('', '', string.punctuation))
    pretext = ' '.join(pretext.split())
    pretext = pretext.strip()
    return pretext

# #Find
# def getJobInfo(job) :

#     job_company = job.select_one('div.k-col-start-3.k-row-start-3 a')
#     if job_company is not None :
#         # print('Company :',job_company.text.strip())
#         job_company = pre_text(job_company.text)

#     # for job_titles :
#     job_title = job.select_one('div.k-col-start-3.k-row-start-1 h2 a')
#     if job_title is not None:
#         # print('Position :',job_title.text.strip())
#         job_title = pre_text(job_title.text)

#     # for job_locations :
#     job_location = job.select_one('div.k-col-start-3.k-row-start-3 a.k-text-subdued.k-block')
#     if job_location is not None :
#         job_location = job_location.text.replace('\n', "").replace(',', '').strip()
        
#         job_location = re.sub(r"\b(?:Indonesia|City|Kota|Kabupaten)\b", "", job_location, flags=re.IGNORECASE).strip()
#         # print('Location :',job_location)
    
#     # for date info     
#     posted_info = job.select_one('div.k-col-start-5.k-row-start-1 span:first-of-type')
#     if posted_info is not None :
#         posted_info = posted_info.text.strip()
#         published_at, application_deadline = posted_info.split("• Apply before")
#         published_at = published_at.replace('ago', '').replace('Posted', '').strip()
#         application_deadline = application_deadline.strip()

#     job_data = [job_company, job_title, job_location, published_at, application_deadline]
#     return job_data

# def save_file() :
#     i = 0

#     job_desc = divElement(page_no=page)
#     # print("Total Save :",len(job_desc))

#     for job in job_desc :
#         i = i + 1
#         job_info = getJobInfo(job)
#         csv.write(job_info[0]+ ',' + job_info[1] + ',' + job_info[2] + ',' + job_info[3] + "," + job_info[4]+ '\n')
#         # print("save",i)

# csv=open("db_kalibrr.csv", 'w')
# headers = "Company,Title,Location,Published_At,Application_Deadline\n"
# csv.write(headers)


# for page in range(1,16):

#     print('Page from :',page)

#     save_file()

# print('Scraping is successful !!')

# csv.close() 

#change into dataframe
df = pd.read_csv('db_kalibrr.csv')

#insert data wrangling here
kota_ubah = df[df['Location'].str.contains('jakarta', case=False)]

# Ubah nilai kolom 'Location' menjadi 'jakarta' jika nilainya terdapat pada kota_ubah
replace_dict = {k: 'Jakarta' for k in kota_ubah['Location'].unique()}
city_dict = df['Location'].replace(replace_dict)

city_dict = city_dict.sort_values(ascending=False).value_counts().head()

# # Ubah nilai pada kolom tertentu
df['Location'] = df['Location'].apply(pre_text)
df['Location'] = df['Location'].replace(['central jakarta','south jakarta','east jakarta', 'west jakarta', 'north jakarta'], \
                                          ['jakarta pusat','jakarta selatan','jakarta timur', 'jakarta barat', 'jakarta utara'])
# Ubah nilai kolom 'Location' menjadi 'tanggerang' jika nilainya terdapat pada kota_ubah
kota_ubah = df[df['Location'].str.contains('tangerang', case=False)]
replace_dict = {k: 'tangerang' for k in kota_ubah['Location'].unique()}
df['Location'] = df['Location'].replace(replace_dict).str.title()


top_city_dict = df['Location'].sort_values(ascending=False)
top_city_dict = top_city_dict.value_counts(normalize=True).head(10)
top_city_dict = top_city_dict.apply(lambda x: round(x * 100, 2))

#end of data wranggling 

#Setting Bar
colors = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']

@app.route("/")
def index(): 
	
	card_data = f'{top_city_dict}' #be careful with the " and ' 

	# generate plot
	fig, ax = plt.subplots(figsize=(15, 9))
	ax.bar(top_city_dict.index, top_city_dict.values, color=colors)
	
	# Rendering plot
    
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True, dpi=100, width=500)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)