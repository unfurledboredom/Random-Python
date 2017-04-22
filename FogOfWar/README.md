FogOfWeb is a nifty little python script that I wrote. This was created with the intention to throw up a smoke screen of bad browsing data for anyone monitoring. It is intended to be used as a form of protest. 

This script does a few things. It generates random internet browsing traffic. It imitates a browser and can go to HTTP and HTTPS sites. It preserves Sessions, so anyone looking for Session Cookies will find them.  

The list of URLs can be changed to anything you like. 

When at a site, it will randomly go to a link and repeat the process. 

It will keep going down the rabbit hole unless it encounters an error then it will try to go down a different hole. 

It works out of the box, but you can also customize it to your liking. 

It is recommended you put URLs you are never likely to visit.

Counter Intelligence 101: Put HTTP URLs because your ISPs can see ALL the data transmitted using HTTP. They are more likely to use this data than HTTPS data. With HTTPS, they can only see where you are going(i.e Google, Facebook and so on) not what you are doing. 

Running it is simple. Install Python, download the script, run the script with a # indicating where you would like it to start. 

Now, sit back, and watch it go around the internet. It will run as long as you let it run. 
