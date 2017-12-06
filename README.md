## MetaSearch Engine with Feedback ##


----------
**The idea**

The main idea of this project is to build a metasearch engine, that can be used to search for an item across various e-commerce websites. The application will gather information like product name, description, reviews, the website were you can buy the product and the corresponding link to that particular product.  With these information, the app will also add an overall sentiment analysis scores. The user can then review all the information, along with the sentiment quotient of each product and will click on one or more product links potentially to buy them online. 
 
Another most important feature is that once the users starts clicking on the links of the products, the app uses those clicks as an implicit feedback and will offer the user with an option to refine the results. If he clicks a button, the list will be re-ordered using Rocchio feedback mechanism and he will be rendered with more relevant results based on his clicks. 

**Implementation**

To implement the whole solution, we needed to do the following

 1. Build a web crawler, that would query the websites based on user's search condition and would parse the html pages to extract the information like product name, description, review etc.
 2. Use vadersentiment library to process the reviews and generate an overall sentiment scores for each products.
 3. Use metapy library to create a python module with utility functions, to create inverted and forward index, rank documents (BM25) and create rocchio feedback ranked results.
 3. Built a flask web application, that would act as a user interface, which would get the results from the crawler and use the utility functions to build the index for the search condition, and display the ranked results on a web page.  Also to enable to user to buy the product on the corresponding website or to refine the results or go back to the search screen.
 
**How to use**

To start the application, please download the entire contents of the below repository.

>  [Project Repository](https://gitlab.textdata.org/deepakn2/cs410proj.git).

Once you have all the files and folders copied to your workspace. Please open up any python editor and execute the python file ***app.py***

Once the app is executed, please open up your favorite browser and navigate to the url [http://localhost:5000/](http://localhost:5000/) or [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

You should now see a search screen. In the search box, entire your product of interest. for example, "baseball gloves" or "women's running shoes" etc. and click submit.
The app will run behind the scene and query the websites (Walmart.com and Kohls.com) get the corresponding results and will display it as per our ranking method, which is BM25. If you wish to buy any product you can go ahead and click the corresponding link, if not, you can navigate back to the page and browse through the rest of the items. If you are not satisfied with the search results, click on the refine results given at the bottom of the page. That should use you previous clicks on the products and use the rocchio feedback mechanism to re-order the list and render it to you. if you are finished or perform a new search, please click on that says back to search.

**Extensions**


Extensions to this app can be done seemless-ly. The webcrawler and flask applications are developed in such a way that the framework is generalized and any additional inclusions like including an additional website like amazon.com or target.com or including additional UI screens like drill-down on the sentiment analysis or applying sort on sentiment analysis scores etc can be easily done. The webcrawler can be extended to other websites as well as additional templates can be created in the flask app.