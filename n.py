from urllib.request import urlopen as uopen
from bs4 import BeautifulSoup as bs
import requests
# search=input(": ").replace(" ","")
search ='iphone11'
url="https://www.flipkart.com/search?q="+search
uclient=uopen(url)
flipkartpage = uclient.read()
uclient.close()
flipkart_html=bs(flipkartpage,'html.parser')
bigbox=flipkart_html.find_all("div",{"class":"_2pi5LC col-12-12"})
del bigbox[0:3]
box=bigbox[0]
# print(box)

product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
popen = requests.get(product_link)
p_html=bs(popen.text,'html.parser')
commentsbox=p_html.find_all('div',{"class":"_16PBlm"})
# print(commentsbox)


review=[]

for comment in commentsbox[:-1]:
    try:
        name=comment.find_all('p',{"class":"_2sc7ZR _2V5EHH"})[0].text
        # print("Name: ",name)
    except:
        name="No user name found !"

    try:
        rating=comment.div.div.div.div.text

    except :
        rating='There is no rating given by this user !'
    try:
        heading=comment.div.div.div.p.text

    except :
        heading='No Heading found for this review !'

    try:
        comment_body=comment.find_all('',{"class":'t-ZTKy'})[0].text

    except:
        comment_body"No comments given by user !"

    try:
        buyed_on=comment.find_all('p',{'class':"_2sc7ZR"})[1].text

    except :
        buyed_on="No information present !"

    my_dict={"Product":search}


