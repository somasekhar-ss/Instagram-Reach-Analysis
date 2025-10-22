# DMDW Project: Instagram Reach Analysis

This is a project for the Data Mining and Data Warehousing (DMDW) course. It uses machine learning to predict the total reach (Impressions) of an Instagram post.

The main goal is to analyze which factors influence a post's reach and build a model that can predict performance before a post is published.

## Project Steps

1.  **Dataset:** The project uses a public dataset from Kaggle with 120 posts and 12 attributes. The target variable to predict is "Impressions".

2.  **Data Preprocessing:**
    * Filled missing numeric values with the median.
    * Removed duplicate posts.
    * Identified and **removed data leakage features** (like 'From Home', 'Hashtags', 'Explore') because they added up to the target variable, 'Impressions'.

3.  **Feature Engineering:**
    * Created new features like `Hashtag Count` and `Caption Length` from text.
    * Calculated an `Engagement Rate`.
    * Scaled features using StandardScaler for models like Linear Regression and SVR.

4.  **Models Tested:**
    Four different regression models were trained and compared:
    * Linear Regression
    * Random Forest
    * XGBoost
    * SVR (Support Vector Regression)

5.  **Evaluation:**
    Models were compared using **RMSE** (lower is better) and **R²** (higher is better).

## Results & Conclusion

The **XGBoost model performed the best**, with the lowest RMSE (2279) and the highest R² score (0.89).

After further tuning, the final XGBoost model achieved an **R² score of 0.93**, meaning it can explain 93% of the variance in post reach.

The most important features for predicting reach were **Likes**, **Followers**, and **Saves**.

## Files in this Repository

* `[Your-Notebook-Name.ipynb]`: The main Jupyter Notebook or code file with all analysis.
* `[Your-Dataset-Name.csv]`: The Kaggle dataset used for this project.
