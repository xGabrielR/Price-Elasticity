# Olist Price Elasticity

--- 

<img src="assets/logo.png">

---

### Summary

- [1.0. Business Problem](#10-bussiness-problem)
- [2.0. Solution Strategy](#20-solution-strategy)
  - [2.1. Problem Solving Methodology](#21-problem-solving-methodology)
- [3.0. Price Elasticity Exploration](#30-price-elasticity-exploration)
  - [3.1. EDA and Product Checkout](#31-eda-and-product-checkout)
  - [3.2. Week over Week Scenario](32-week-over-week-scenario)
- [4.0. Data Infrastructure](#40-data-infrastructure)
  - [4.1. OLTP and ETL](#41-olt-and-etl)
  - [4.2. Data Science](#42-data-science)
  - [4.3. Weekly Orchestration](#43-weekly-orchestration)
- [5.0. Business Results](#50-business-results)
- [6.0. Next Steps](#60-next-steps)

---

## 1.0. Business Problem

---

**Business Overview**: Olist is a Brazilian startup that operates in the retail technology segment. The company has solutions that facilitate the management of offline and online stores (e-commerce) and also a solution for increasing sales within marketplaces. On the one hand, Olist concentrates sellers who want to advertise on marketplaces such as Mercado Livre, Americanas and Amazon. On the other hand, concentrate products from all sellers in a single store that is visible to the end consumer. Olist was founded in February 2015 by Tiago Dalvi, as a spin-off from Solidarium, a company created in 2007 as a shopping store that later became a marketplace for the sale of artisanal products.

Source: Wikipedia.

Business Problem: In Olist, products is selled by a people called `seller` and exists some key products to drive sales, such as top 10% or top 20% most selled products, this products can have unique pattern and some mining can be done with this orders data. Based on this context, olist receive a fee (Seller sell products and olist receive mayme 10% ~ 25% of product price), a fee is how a marketplace receive money for joining sellers and customers. The products can have promo, discount, inflation adjust and other random events that change product price, this change can affect demand, people cannot buy more this product because is very expensive or people will buy a LOT of this product because have a very low price, this phenomenon can be easily seen in traditional grocery, older products have a very low price (in may cases) in promo or with discount to sell very fast because new and fresh products is available on warehouse just waiting to have space in product shelf to be placed and price up again.

"A good's price elasticity of demand (PED) is a measure of how sensitive the quantity demanded is to its price. When the price rises, quantity demanded falls for almost any good (law of demand), but it falls more for some than for others. The price elasticity gives the percentage change in quantity demanded when there is a one percent increase in price, holding everything else constant. If the elasticity is −2, that means a one percent price rise leads to a two percent decline in quantity demanded. Other elasticities measure how the quantity demanded changes with other variables (e.g. the income elasticity of demand for consumer income changes)".   

Source: Wikipedia.

Now, you need to build a infrastructure and a solution in weekly basis scenario to follow price elasticity of top olist products, with this solution some business people of different segments of Olist can track this elasticity for better decision taking.

- Revenue management teams to optimize their pricing & promotional strategy in actions to segment marketing, campains and products.
- Finance team can do a practical what-if scenario analyses of key price changes or discount actions. 
- Supply chain team can have a visibility into how specific promotional actions would impact inventory levels or how deep clearance price discounts need to be deplete over-bought inventory that's not selling. 


## 2.0. Solution Strategy

---

The solution strategy is to build a most simple data infrastructure to solution this problem, i using AWS products and Open Source tools to design a infrastructure for: data engineering (collect, conform and prepare data), data science (collect clean and complete data to build price elasticity solution) and mlops (re-train and versioning price elasticity solutions).

### 2.1. Problem Solving Methodology

---

I have CRISP in my toolkit for rapid development of solutions and problem solving techniques, based on this, the author "Eric Ries" has a phrase in the book lean startup, "Vision leads to direction" and shows a cyclical process for startup fast projects solutions and can be applied to data science projects too!!!


## 3.0. Price Elasticity Exploration

---

Exists some solutions for Price Elasticity in marketing today.

- Linear Regression (Additive): Is the most easy and simple, i just need Price and Units selled to build a linear model to estimate elasticity using midpoint formula [ (avg price / avg unit) * slope ], this is a simple and very fast approach because exists some "pocket equations" to solve that.
- Linear Regression with Exog features (Additive): This requires feature engineering and "exog" / extra features to build a simple linear regression, now with extra features, price and demand.
- Log Log Regression: This is alterantive to use Log of price and Log of demand, using this solution the slope of linear regression is percentage changes a.k.a elasticity, you can use extra features (exog features or not) for add more coeficients to linear regression estimation of PE.
- Linear Regression with Regularization + Exog Features: Is possible to apply regularization to reduce multi-colinearity when you using exog features.
- Machine Learning: Is possible to compute price elasticity with traditional Sklearn estimators (Decision Tree, Random Forest...).

I will follow using Log Log Regression without extra exog features, with this solution first, because is a great solution and easy to estimate (slope is elasticity), i w8ill follow this approach because I do not need to deep dive in feature engineering in this first CRISP solution. With CRISP i need to delivery a very fast MVP solution to validate project and next CRISP iterations i deep dive into other steps of the solution (Data Engineering, Data Science and Mlops), but for my first delivery i will follow a very simple scenario. 

The second reason i will use a simple log log linear regression is because the dataset have very low samples, is very hard to fit a random forest with small sample, but is possible. 


### 3.1. EDA and Product Checkout

---




### 3.2. Week over Week Scenario

---

## 4.0. Data Infrastructure

---

### 4.1. OLTP and ETL

---

### 4.2. Data Science

---

### 4.3. Weekly Orchestration

---



## 5.0. Business Results

---

The main objective is to build a end-to-end re-train price elasticity solution to follow price variation over multiple weeks and give a business user a tool to compare price elasticity between weeks and products.

<img src="assets/price_x_demand.gif">


## 6.0. Next Steps

---

I have build a base project, is possible to deep dive in every step of this project, for example, going deep into `OLTP sistems` and build a real time orders generator based on simulations from Olist Dataset to create a Real Time Source System or Deep Dive into Price Elasticity modeling techniques to develop more robust and complete price elasticity solution using feature engineering (seasonality and time series features like lag units, price, differences, product behavior such as category, subcategory, type, warehouse quantity... and much other features), apply other techniques (Sklearn, Decision Tree, feature importance), is possible to deep dive in some of the steps in this project. 
