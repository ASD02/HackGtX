import os
from dotenv.main import load_dotenv
from langchain.llms import OpenAI
#from langchain.chat_models import ChatOpenAI
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import easyocr
import cv2
from streamlit_option_menu import option_menu


load_dotenv()
llm = OpenAI(openai_api_key=os.environ["KEY"])

def read_img(img):
    try:
        image = Image.open(img)
        reader = easyocr.Reader(['en']) 
        text = reader.readtext(image, detail=0)
        return(str(text))
    except Exception as e:
        return "An error has occurred."
    
def macro(macronutrient):
    if macronutrient == "Fats":
        macronutrient = 'Lipid'
    temp = """Answer the question based on the context below. You are a helpful health and cooking assistant. Based on the Macronutrient given, create a recipe centered around that macronutrient.
    
    macronutrient: protein

    Answer: Grilled Chicken Quinoa Bowl

    Ingredients:

    Chicken breasts
    Olive oil, garlic powder, paprika
    Quinoa, broth, lemon, parsley
    Mixed greens, cherry tomatoes, cucumber, red onion
    Feta (optional), hummus, lemon wedges
    Instructions:

    Marinate and grill chicken.
    Cook quinoa, add lemon, parsley.
    Assemble bowls with quinoa, grilled chicken, greens, tomatoes, cucumber, onion. Add feta if desired.
    Serve with hummus and lemon wedges.
    This protein-packed Grilled Chicken Quinoa Bowl makes a balanced, flavorful meal. Enjoy!


    macronutrient: carbohydrates

    Answer: Mediterranean Quinoa Salad

    Ingredients:

    1 cup quinoa, cooked and cooled
    1 cup cherry tomatoes, halved
    1 cucumber, diced
    1/2 red onion, finely chopped
    1/4 cup Kalamata olives, pitted and sliced
    1/4 cup crumbled feta cheese
    1/4 cup fresh parsley, chopped
    For the Dressing:

    3 tablespoons extra-virgin olive oil
    2 tablespoons lemon juice
    1 garlic clove, minced
    Salt and pepper to taste
    Instructions:

    Combine all salad ingredients in a bowl.
    In a separate bowl, whisk together the dressing ingredients.
    Drizzle the dressing over the salad, toss, and serve. Enjoy!


    macronutrient: lipid

    Answer: Avocado and Smoked Salmon Toast

    Ingredients:

    2 slices whole-grain bread
    1 ripe avocado
    4 oz smoked salmon
    1 small red onion, thinly sliced
    1 lemon, sliced into wedges
    Fresh dill for garnish
    Salt and pepper to taste
    Instructions:

    Toast the bread.
    Mash the avocado and spread it on the toasted slices.
    Top with smoked salmon, red onion slices, and a squeeze of lemon juice.
    Season with salt and pepper, garnish with fresh dill, and enjoy this lipid-rich, omega-3-packed meal!

    
    macronutrient: {macro}

    Answer: """
    prompt_template = PromptTemplate(
        input_variables=["macro"],
        template= temp
    )
    return llm(prompt_template.format(macro = macronutrient))

def allergy(allergy, text):
    temp = """Answer the question based on the context below. If there are no matches between allergies and allergens in the food, write "No restrictions were detected.".

    Context: Food allergies are hard to maintain and find, based on the user given allergies, see if there are any in the food. 


    Allergies: Eggs

    Food: ['Ingredients: Enriched Corn', 'Meal (Corn Meal,', 'Ferrous Sulfate_', 'Niacin,  Thiamin', 'Mononitrate', 'Riboflavin; Folic Acid) , Vegetable Oil (Corn, Canola;', 'and/or Sunflower Oil) , Cheese Seasoning (Whey,', 'Cheddar Cheese [Milk; Cheese Cultures, Salt,', 'Enzymes]', 'Canola Oil,', 'Maltodextrin [Made from', 'Corn],', 'Natural and Artificial Flavors,', 'Salt; Whey', 'Protein  Concentrate ,', 'Monosodium', 'Glutamate', '1', 'Lactic Acid, Citric Acid, Artificial Color [Yellow 6]) ,', 'and Salt ']

    Answer: No restrictions were detected.


    Allergies: Milk

    Food: ['Ingredients: Enriched Corn', 'Meal (Corn Meal,', 'Ferrous Sulfate_', 'Niacin, Thiamin', 'Mononitrate', 'Riboflavin; Folic Acid) , Vegetable Oil (Corn, Canola;', 'and/or Sunflower Oil) , Cheese Seasoning (Whey,', 'Cheddar Cheese [Milk; Cheese Cultures, Salt,', 'Enzymes]', 'Canola Oil,', 'Maltodextrin [Made from', 'Corn],', 'Natural and Artificial Flavors,', 'Salt; Whey', 'Protein Concentrate ,', 'Monosodium', 'Glutamate', '1', 'Lactic Acid, Citric Acid, Artificial Color [Yellow 6]) ,', 'and Salt ']

    Answer: This contains Milk, which was listed in your allergies.


    Allergies: Milk

    Food: ['Ingredients: Enriched Corn', 'Meal (Corn Meal,', 'Ferrous Sulfate_', 'Niacin, Thiamin', 'Mononitrate', 'Riboflavin; Folic Acid) , Vegetable Oil (Corn, Canola;', 'and/or Sunflower Oil) , Cheese Seasoning (Whey,', 'Cheddar Cheese [Milk; Cheese Cultures, Salt,', 'Enzymes]', 'Canola Oil,', 'Maltodextrin [Made from', 'Corn],', 'Natural and Artificial Flavors,', 'Salt; Whey', 'Protein Concentrate ,', 'Monosodium', 'Glutamate', '1', 'Lactic Acid, Citric Acid, Artificial Color [Yellow 6]) ,', 'and Salt ']

    Answer: This contains Milk, which was listed in your allergies.


    Allergies: None

    Food: ['Ingredients: Enriched Corn', 'Meal (Corn Meal,', 'Ferrous Sulfate_', 'Niacin,  Thiamin', 'Mononitrate', 'Riboflavin; Folic Acid) , Vegetable Oil (Corn, Canola;', 'and/or Sunflower Oil) , Cheese Seasoning (Whey,', 'Cheddar Cheese [Milk; Cheese Cultures, Salt,', 'Enzymes]', 'Canola Oil,', 'Maltodextrin [Made from', 'Corn],', 'Natural and Artificial Flavors,', 'Salt; Whey', 'Protein  Concentrate ,', 'Monosodium', 'Glutamate', '1', 'Lactic Acid, Citric Acid, Artificial Color [Yellow 6]) ,', 'and Salt ']

    Answer: No restrictions were detected.


    Allergies: Soybeans, Eggs

    Food: ['Ingredients: Enriched Corn', 'Meal (Corn Meal,', 'Ferrous Sulfate_', 'Niacin,  Thiamin', 'Mononitrate', 'Riboflavin; Folic Acid) , Vegetable Oil (Corn, Canola;', 'and/or Sunflower Oil) , Cheese Seasoning (Whey,', 'Cheddar Cheese [Milk; Cheese Cultures, Salt,', 'Enzymes]', 'Canola Oil,', 'Maltodextrin [Made from', 'Corn],', 'Natural and Artificial Flavors,', 'Salt; Whey', 'Protein  Concentrate ,', 'Monosodium', 'Glutamate', '1', 'Lactic Acid, Citric Acid, Artificial Color [Yellow 6]) ,', 'and Salt ']

    Answer: No restrictions were detected.


    Allergies: Eggs

    Food: ['INGREDIENTS:', 'Enriched', 'unbleached', 'flour', '(wheat   flour,  malted', 'flour;', "ascorbic acid [dough conditioner] ' niacin;", 'reduced', 'mononitrate ,', 'riboflavin,   folic , acid],   sugar, , degermed', 'vellow cornmeal, salt, leavening (baking', 'soda,', 'sodium', 'acid', 'pyrophosphate];', 'soybean oil, [', "'powder;, natural flavor;", 'CONTAINS; Wheat', "'contain milk; eggs, soy and tree nuts.", 'barlev', 'thiamin', 'iron,', 'honey "', 'May ']

    Answer: This contains Eggs, which was listed in your allergies.


    Allergies: Milk

    Food: ['INGREDIENTS:', 'Enriched', 'unbleached', 'flour', '(wheat   flour,  malted', 'flour;', "ascorbic acid [dough conditioner] ' niacin;", 'reduced', 'mononitrate ,', 'riboflavin,   folic , acid],   sugar, , degermed', 'vellow cornmeal, salt, leavening (baking', 'soda,', 'sodium', 'acid', 'pyrophosphate];', 'soybean oil, [', "'powder;, natural flavor;", 'CONTAINS; Wheat', "'contain milk; eggs, soy and tree nuts.", 'barlev', 'thiamin', 'iron,', 'honey "', 'May ']

    Answer: This contains Milk, which was listed in your allergies.


    Allergies: Soybeans, Tree Nuts

    Food: ['INGREDIENTS:', 'Enriched', 'unbleached', 'flour', '(wheat   flour,  malted', 'flour;', "ascorbic acid [dough conditioner] ' niacin;", 'reduced', 'mononitrate ,', 'riboflavin,   folic , acid],   sugar, , degermed', 'vellow cornmeal, salt, leavening (baking', 'soda,', 'sodium', 'acid', 'pyrophosphate];', 'soybean oil, [', "'powder;, natural flavor;", 'CONTAINS; Wheat', "'contain milk; eggs, soy and tree nuts.", 'barlev', 'thiamin', 'iron,', 'honey "', 'May ']

    Answer: This contains Soy and Tree Nuts, which were listed in your allergies.


    Allergies: Soybeans

    Food: ['INGREDIENTS:', 'Enriched', 'unbleached', 'flour', '(wheat   flour,  malted', 'flour;', "ascorbic acid [dough conditioner] ' niacin;", 'reduced', 'mononitrate ,', 'riboflavin,   folic , acid],   sugar, , degermed', 'vellow cornmeal, salt, leavening (baking', 'soda,', 'sodium', 'acid', 'pyrophosphate];', 'soybean oil, [', "'powder;, natural flavor;", 'CONTAINS; Wheat', "'contain milk; eggs, soy and tree nuts.", 'barlev', 'thiamin', 'iron,', 'honey "', 'May ']

    Answer: This contains Soy, which was listed in your allergies.


    Allergies: Fish

    Food: ['INGREDIENTS:', 'Enriched', 'unbleached', 'flour', '(wheat   flour,  malted', 'flour;', "ascorbic acid [dough conditioner] ' niacin;", 'reduced', 'mononitrate ,', 'riboflavin,   folic , acid],   sugar, , degermed', 'vellow cornmeal, salt, leavening (baking', 'soda,', 'sodium', 'acid', 'pyrophosphate];', 'soybean oil, [', "'powder;, natural flavor;", 'CONTAINS; Wheat', "'contain milk; eggs, soy and tree nuts.", 'barlev', 'thiamin', 'iron,', 'honey "', 'May ']

    Answer: No restrictions were detected.


    Allergies: {allergies}

    Food: {food}

    Answer: """

    prompt_template = PromptTemplate(
        input_variables=["allergies", "food"],
        template= temp
    )
    return llm(prompt_template.format(allergies=allergy, food=text))

st.write("""
# Welcome to Plate Guardian!
Our handy application helps you feel safe and secure in your food choices. Simply upload an image of a food's ingredient list, and our application will scan the list for allergens, dietary restriced ingredients, or desired macronutrients.
""")
st.subheader("Dietary focus")
selected_tab = st.selectbox("Enter your dietary focus:", ["Allergens", "Dietary restrictions", "Macronutrients"])
def render_page(tab_name):
    if tab_name == "Allergens":
        st.subheader("Allergens")
        a = st.text_input("Enter your allergies:")   
        uploaded_file = st.file_uploader("Upload food label", type=["jpg", "jpeg", "png"])         
        if st.button('Find allergens'):
            st.write('Your allergen report is generating...')
            text = read_img(uploaded_file)
            st.write("These ingredients were found:")
            st.write(text)
            st.title(allergy(a, text))
    elif tab_name == "Dietary restrictions":
        st.subheader("Dietary restrictions")
        b = st.selectbox("Select dietary restriction", ["Kosher","Halal","Vegan", "Vegetarian"])    
        uploaded_file = st.file_uploader("Upload food label", type=["jpg", "jpeg", "png"])            
        if st.button('Find dietary restrictions'):
            st.write('Your dietary restrictions report is generating...')
            text = read_img(uploaded_file)
            st.write("These ingredients were found:")
            st.write(text)
            st.title(allergy(b, text))
    elif tab_name == "Macronutrients":
        st.subheader("Macronutrients")
        c = st.selectbox("Select Macronutrient", ["Carbohydrates", "Fats", "Proteins"])           
        if st.button('Find Target Macronutrient'):
            st.write('Macronutrient Report Generated')
            st.title(macro(c))
render_page(selected_tab)
##uploaded_file = st.file_uploader("Upload food label", type=["jpg", "jpeg", "png"])
