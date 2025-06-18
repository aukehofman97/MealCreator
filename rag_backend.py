import openai
import os
from retriever import get_macro_info
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def build_prompt(ingredients: list, meal_type: str, meal_targets: dict):
    found = []
    missing = []

    for ing in ingredients:
        row, macro, source = get_macro_info(ing)
        if row:
            found.append((ing, row, source))
        else:
            missing.append((ing, source))

    prompt = f"""You are a nutrition assistant. The user wants to create a {meal_type.lower()}.
This meal should contain around {meal_targets['kcals']} kcal, with macros:
- Protein: {meal_targets['protein']}g
- Carbs: {meal_targets['carbs']}g
- Fat: {meal_targets['fat']}g

These are the ingredients the user wants to use: {', '.join(ingredients)}.

Nutritional data:
"""
    for ing, row, source in found:
        prompt += f"- {ing.title()} ({source}): " + ", ".join([f"{k}: {v}" for k, v in row.items() if k != "Ingredient"]) + "\n"

    if missing:
        prompt += "\nIngredients not found in context: " + ", ".join([i[0] for i in missing]) + "\n"

    prompt += "\nSuggest a meal composition using the ingredients, in exact quantities to meet the macro goals.\n"
    return prompt

def call_llm(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful meal planner."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']
