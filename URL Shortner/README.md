**URL Shorter**
==========================

> **Prompt**
> Our product team think they have a revolutionary idea and they want the developers to implement it. After seeing the requirements, the developers told the product team that their idea is not unique and it already exists on the web. However, the product team is pretty adamant about the idea and want the developers to implement it anyway. They have the following requirements 
> As a user, I want to shorten a long url:
> 1) I can input my long url in a field and after submission it gives me a short url which I can share with others
> 2) When someone clicks on the short url, it redirects them to the long url
> 3) I can visit a page or call an api which gives me some information about people who clicked on my url. For example:
> a) The number of people clicked on it
> b) The type of device and IP address of each person
> c) When they clicked on it
> d) Include any other information that could be relevant
> Please create a small app that implements the requirements given by the product team. You can use any language, framework and data storage of your choice.

**************

**Solution** 
--------------
A stateless application that can generate *short urls* using indexes. 

The application will save the **long url** to the database. It will then return the **ID** for that record *base64* encoded. This will in turn act as the **short url**. This effectively removes the need for a **Shortening Algorithm** and all issues associated with one (i.e. checking for duplicates, issues with distributed deployments and so on). 

*API Endpoint*
It accepts a ```POST``` request on the ```/api/``` endpoint. The request must be json and contain an element called **url**. In turn, it will return a json element called **data** containing the field **url**, which is the path to the new shortened url.  
The front end then takes the url path, adds it to the ```ROOT_URL``` to generate the full short url and the link to the page with the visitor information for this url. 
A user can take the URL and distribute it. They can go to the ```Metrics``` url to see the relevant information. 

The short url ```/<shorturl>``` accepts a GET request for a shortened url. It decodes the base64 string and looks it up in the database. If found, it will save the visitor information and redirect the visitor to the URL. 

The ```Metrics``` page contains information regarding every visitor to the url. It will display the following: IP, Browser, Platform and the time at which the visitation occurred. 

**Scalability**
The front end is decoupled from the back end. This is to make it highly scalable. The front just needs to point to a backend server or a backend loadbalancer. The backend can be deployed to as many instances as needed. All you would need to do is plug it into a centralized loadbalancer (simple round-robin would be enough). 

Due to time limitations, I am using a Sqlite3 database attached to the application. Because of this, the current solution as is will not scale horizontally. This can be easily remedied by replacing the Sqlite3 database with something such as MySQL or any other relational database servers. 

**Instructions**
- The front-end page ```frontend/index.html``` can be deployed on to any http server that can serve simple html files. 
- Please be sure to update the ```ROOT_URL``` variable in the **index.html** to point at the appropriate endpoint for the back-end. 
- The back end can be deployed to IIS, Apache or ran directly (```python server/server.py```) for testing. *(Use the attacheed POSTMAN script to test the back end.)*
- The Application requires a Sqlite3 database to be in the same directory called ```url.db```
- A sample database is attached along with the **DDLs** to create a new one.  
