# NLP Project - Predicting Visits from topics of Digital Newspaper Articles

## Abstract
The goal of this project was to combine topic modeling and regression approaches to forecast visits for newspaper articles published online to support editors in choosing which articles to publish. Additionally, the model may provide evidence for journalists which article topics and characteristics may be important for attracting readership. My analysis was based on articles of German publisher Frankfurter Allgemeine Zeitung published online 01/01/22 - 20/06/22 and their corresponding visit figures. In feature engineering, I leveraged article text data and meta information of articles itself to create a set of categorical and numerical features. In terms of topic modeling, I used LDA to feed linear regression, lasso, ridge, random forest regressor and gradient boosting regressor. Finally, model was integrated within a web app on streamlit enabling to pass article characteristics to generate visit predictions.

## Design
The project topic constitutes a central question of current (data-driven) journalism. Feature data was scraped from a publically available newsticker website listing all historically published articles and from each articles’ corresponding URL. The paywall was circumvented using cookie data of a digital subscription. Target data on article visits was provided from within the company. Extracting insights on article properties (such as topic, author, paid/free status or publication time) contributing to high reader numbers via machine learning models may support journalists and editors to reach larger audiences. It may help to evaluate article popularity ex-ante their publication online and thus assist in the choice of articles to be provided for-free or paid.

![image](https://user-images.githubusercontent.com/98846184/178575216-6ab54dda-e6fe-4747-bd45-39a4b17e6942.png)

## Data
The original dataset contains 26,538 articles with 106 features for each, 77 of which are categorical. A few feature highlights include “topics probabilities” derived from LDA, “free/paid”, “author”, “source weekday print”, “publishing-time of day”, “day of week” and “previous day visits”. Approx. 75% of these features were created from specifications of more narrow categories (such as “author”). The feature set was refined by removing collinear and insignificant features with the final dataset consisting of 85 variables feeding the baseline model.

**Topic Development at faz.net in H1/2022**
![image](https://user-images.githubusercontent.com/98846184/178576201-571344c8-40f3-40f9-8b84-3868be70dcab.png)

## Algorithms
### Feature Engineering
    1. Create one-hot features for 15 authors with most and least visits and orders per article
    2. Preprocess article texts (punctuation, lowering, stemming, stopwords), vectorize via TFIDF, fit an LDA model and choose number of topics 
    3. Creating bins reflecting time series features (such as time of day or day of week)
    4. Creating bins reflecting article source (such as print weekday or news agency)
    5. Converting categorical features to binary dummy variables (such as authors or department)
    6. Log-transform count-data such as article visits to fulfill regression requirements of normal distribution of errors

**Correlation Matrix**
![image](https://user-images.githubusercontent.com/98846184/178576568-c21fa656-2dd5-4ec7-9fcb-a381d4e4d118.png)

**Distribution of Visits vs. Log-Transformed Visits**
![image](https://user-images.githubusercontent.com/98846184/178576415-530da3cd-50a7-4cdc-b90e-89b164795ded.png)

**Residual-Plot after Log-Transformation**

![image](https://user-images.githubusercontent.com/98846184/178576476-68e42f12-e77b-467b-8102-418be31d1ee8.png)

**QQ-Plot**

![image](https://user-images.githubusercontent.com/98846184/178576763-f5bdd4cd-1beb-4b68-beeb-e88a85dea751.png)

### Models
Linear regression, lasso, ridge, random forest regressor and gradient boosting regressor were used before settling on gradient boosting regressor as the model with strongest performance. Throughout, collinear and insignificant features were removed from the feature space.

### Model Evaluation and Selection
The entire training dataset was split by publication date into individual months to conduct forward time series cross validation on individual months. As a result, all scores reported below were calculated with 4-fold cross validation. Predictions on articles with publication date in June were limited to the very end, so this split was only used and scores seen just once. Models were evaluated based on their generalization performance using R², Mean Absolute Error (MAE) and Root Mean Square Error (RMSE). The gradient boosting regressor had a R² of 0.61 on the test sample versus a mean R² of 0.60 on the 4-fold CV sample.

**Performance of different Models
![image](https://user-images.githubusercontent.com/98846184/178576711-99314d78-8d84-44ba-9f1f-5d42a6a929e6.png)

**Gradient Boosting Regressor - Prediction vs. Test Values (Log-Transformed)
![image](https://user-images.githubusercontent.com/98846184/178576670-91831017-8a3c-4ddc-b460-54b683f6788b.png)

## Tools
    • BeautifulSoup and Selenium for webscraping
    • NumPy and pandas for data manipulation
    • NLTK and genism for text processing and topic modeling
    • Pillow for image feature generation
    • Statsmodels and scikit-learn for modeling
    • Matplotlib and Seaborn for plotting
    • Streamlit for creating a web application

## Web App
In addition to the slides and visuals presented, the model is embedded in a dedicated streamlit app: https://fabian2964-nlp-app-shxtrh.streamlitapp.com/
