# 🧠 Item-Based Recommendation System

This project implements an **item-based collaborative filtering** system. Unlike content-based systems, this approach leverages user behavior to find similar items based on **user-item interaction patterns**.

## 🔍 How it works
- Calculates item-item similarity using user ratings or purchase history
- Recommends items that were liked by users who liked the same item
- Ideal for marketplaces, e-commerce, or movie/music recommendation

## 📁 Files
- `item_based_recommender.py`: The core script for building and testing the recommender

## 🛠️ Requirements
- `pandas`
- `scikit-learn`
- `numpy`

Install with:

```bash
pip install pandas scikit-learn numpy
