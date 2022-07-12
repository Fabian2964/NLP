# NLP Project Description - Predicting Visits from topics of Digital Newspaper Articles

## Abstract
The goal of this project was to combine topic modeling and regression approaches to forecast visits for newspaper articles published online to support editors in choosing which articles to publish. Additionally, the model may provide evidence for journalists which article topics and characteristics may be important for attracting readership. My analysis was based on articles of German publisher Frankfurter Allgemeine Zeitung published online 01/01/22 - 20/06/22 and their corresponding visit figures. In feature engineering, I leveraged article text data and meta information of articles itself to create a set of categorical and numerical features. In terms of topic modeling, I used LDA to feed linear regression, lasso, ridge, random forest regressor and gradient boosting regressor. Finally, model was integrated within a web app on streamlit enabling to pass article characteristics to generate visit predictions.

## Design
The project topic constitutes a central question of current (data-driven) journalism. Feature data was scraped from a publically available newsticker website listing all historically published articles and from each articles’ corresponding URL. The paywall was circumvented using cookie data of a digital subscription. Target data on article visits was provided from within the company. Extracting insights on article properties (such as topic, author, paid/free status or publication time) contributing to high reader numbers via machine learning models may support journalists and editors to reach larger audiences. It may help to evaluate article popularity ex-ante their publication online and thus assist in the choice of articles to be provided for-free or paid.

![image](https://user-images.githubusercontent.com/98846184/178575216-6ab54dda-e6fe-4747-bd45-39a4b17e6942.png)

