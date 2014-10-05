## Getting Started

* Install [pip](http://pip.readthedocs.org/en/latest/installing.html) package manager if you haven't yet:

        Linux: sudo apt-get install python-pip
        Mac: brew install python

* Install [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html#installation):

        sudo pip install virtualenv

* Clone this repo: 

        git clone git@github.com:YoApp/BarRecommendor.git
        cd BarRecommendor
        
* Create a virtualenv, enter it and install dependencies:

        virtualenv env
        . env/bin/activate
        pip install -r requirements.txt

* Get your [Yelp keys](http://www.yelp.com/developers/manage_api_keys) and edit [lines 30-33](https://github.com/YoApp/BarRecommendor/blob/master/main.py#L30)

* Get your [Yo API](http://dev.justyo.co/) token and edit [line 118](https://github.com/YoApp/BarRecommendor/blob/master/main.py#L118)

* Run the [Flask](http://flask.pocoo.org/) server to accept incoming requests on port 5000:

        python main.py
        
![alt tag](http://cl.ly/image/3v043Y2V2Q0K/Screen%20Shot%202014-10-05%20at%208.15.38%20AM.png)
        
* Download and run [ngrok](https://ngrok.com/download) to expose your local server to the interwebz:

        ./ngrok 5000
        
![alt tag](http://cl.ly/image/00143n1b2U05/Screen%20Shot%202014-10-05%20at%208.10.17%20AM.png)
        

* Copy the URL ngrok creates (i.e ```http://1fe8e9f.ngrok.com```)

* Create your Yo API account and use the ngrok URL as the callback URL but with the path "yo" (like it's defined for flask):

![alt tag](http://cl.ly/image/2D3E2r3S110F/Screen%20Shot%202014-10-05%20at%208.25.33%20AM.png)

* Yo your location (double tap) to the name you created (YOBARME in this example) and get a bar recommendation!
