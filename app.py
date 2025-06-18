import streamlit as st
from rag_backend import build_prompt, call_llm

MEAL_TARGETS = {
    "Breakfast": {"kcals": 537, "protein": 35, "carbs": 66, "fat": 15},
    "Snack 1": {"kcals": 403, "protein": 26, "carbs": 49, "fat": 11},
    "Lunch": {"kcals": 805, "protein": 53, "carbs": 99, "fat": 22},
    "Snack 2": {"kcals": 403, "protein": 26, "carbs": 49, "fat": 11},
    "Dinner": {"kcals": 537, "protein": 35, "carbs": 66, "fat": 15},
}

st.title("🔬 AI Meal Creator")
meal_type = st.selectbox("Choose a meal", list(MEAL_TARGETS.keys()))
ingredients = st.text_area("What ingredients do you want to use? (comma-separated)")

if st.button("Generate Meal Suggestion"):
    ingredient_list = [i.strip() for i in ingredients.split(",")]
    prompt = build_prompt(ingredient_list, meal_type, MEAL_TARGETS[meal_type])
    suggestion = call_llm(prompt)
    st.markdown("### 🍽 Suggested Meal")
    st.write(suggestion)
