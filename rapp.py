
from flask import Flask , request, render_template, jsonify
import requests
from flask_cors import cross_origin
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as bs

app=Flask(__name__)


@app.route('/',methods=["GET"])
@cross_origin()
def homepage():
    return render_template('index.html')

@app.route("/scrap",methods=["POST"])
def index():
    if request.method=="POST":
        search=request.form["content"].replace(" ","")
        try:
            url="https://www.flipkart.com/search?q="+search
            uclient=ureq(url)
            # print(uclient)
            flipkartpage=uclient.read()
            uclient.close()
            flipkart_html=bs(flipkartpage,'html.parser')
            # print(flipkart_html)
            # _2pi5LC col-12-12 this class has been change with recent one
            bigbox=flipkart_html.findAll('div',{'class':'_1AtVbE col-12-12'})
            # print('bigbox',bigbox)
            del bigbox[0:3]
            box=bigbox[0]
            product_link="https://www.flipkart.com"+box.div.div.div.a['href']
            print('product link',product_link)
            popen=requests.get(product_link)
            p_html=bs(popen.text,'html.parser')
            commentsbox = p_html.find_all('div', {"class": "_16PBlm"})

            reviews = []

            for comment in commentsbox[:-1]:
                try:
                    name = comment.find_all('p', {"class": "_2sc7ZR _2V5EHH"})[0].text
                    # print("Name: ",name)
                except:
                    name = "No user name found !"

                try:
                    rating = comment.div.div.div.div.text

                except:
                    rating = 'There is no rating given by this user !'
                try:
                    heading = comment.div.div.div.p.text

                except:
                    heading = 'No Heading found for this review !'

                try:
                    comment_body = comment.find_all('', {"class": 't-ZTKy'})[0].text

                except:
                    comment_body="No comments given by user !"

                try:
                    buyed_on = comment.find_all('p', {'class': "_2sc7ZR"})[1].text

                except:
                    buyed_on = "No information present !"

                my_dict = {"Product": search,"Name":name,"Rating":rating,"CommentHead":heading,"Comment":comment_body}

                reviews.append(my_dict)
        
            return render_template("results.html",reviews=reviews)
        except :
            return "Something went wrong !"

    else:
        return render_template('index.html')


if __name__ =='__main__':
    app.run(debug=True)






