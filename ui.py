import gradio as gr
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import google.generativeai as genai  
import os
from dotenv import load_dotenv
import sele

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

products = [
    {"name": "Lipstick", "price": "₹1500", "image": r"images\images.jpeg", "category": "Makeup"},
    {"name": "Foundation", "price": "₹2500", "image": r"images\foundation.jpg", "category": "Makeup"},
    {"name": "Eyeliner", "price": "₹1000", "image": r"images\eyeliner.jpeg", "category": "Makeup"},
    {"name": "Perfume", "price": "₹400", "image": r"images\perfume.jpg", "category": "Fragrance"},
    {"name": "Mascara", "price": "₹200", "image": r"images\maskara.jpeg", "category": "Makeup"},
    {"name": "Blush", "price": "₹1800", "image": r"images\blush.jpeg", "category": "Makeup"},
    {"name": "Nail Polish", "price": "₹120", "image": r"images\nailpolish.jpeg", "category": "Nail Care"},
    {"name": "Compact Powder", "price": "₹2200", "image": r"images\compact.jpeg", "category": "Makeup"},
]

cart = []

css_style = """
<style>
    body{
        background-color: pink !important;
    }
    .gradio-container{
        text-align: center;
        font-family: Arial, sans-serif;
        background-color: pink !important;
    }
    .box{
        text-align: center;
    }
    .box:hover{
        transform: scale(1.1);
    }
    
    .gr-row {
        margin-bottom: 40px;  
    }
    .custom-button {
        background-color: deeppink !important;
        color: white !important;
        border-radius: 20px;
        padding: 10px;
        width:250px;
        margin-left:30px;
    }
    .heading{
        font-family: Times New Roman;
        font-size:100px;
    }
"""

product_data = pd.DataFrame(products)
product_features = pd.get_dummies(product_data[['category']])
product_features['price'] = product_data['price'].apply(lambda x: int(x.replace("₹", "")))
similarity_matrix = cosine_similarity(product_features)

def automation():
    try:
        otp = None
        sele.run_sele(otp)  
        return "Automation executed successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

def recommend_products(selected_product):
    index = product_data[product_data["name"] == selected_product].index[0]
    similar_indices = np.argsort(-similarity_matrix[index])[:3]  
    recommendations = product_data.iloc[similar_indices]["name"].tolist()
    return f"Recommended Products: {', '.join(recommendations)}"

def best_brands_recommendation(cart_items):
    categories = set([item['category'] for item in cart_items])
    user_query = f"What are the best brands for {', '.join(categories)} in India?"
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(user_query)
    return response.text if response else "No recommendations available."

def format_cart():
    if not cart:
        return "Your cart is empty! Add some products first."
    cart_items = [f"{item['name']} - {item['price']}" for item in cart]
    total_price = sum(int(item["price"].replace("₹", "")) for item in cart)
    return f" Items in Cart:\n" + "\n".join(cart_items) + f"\n\n **Total Price: ₹{total_price}**"

def checkout():
    if not cart:
        return "Your cart is empty! Add some products first."
    total_price = sum(int(item["price"].replace("₹", "")) for item in cart)
    summary = f" **Checkout Summary:**\n\n"
    summary += "\n".join([f"{item['name']} - {item['price']}" for item in cart])
    summary += f"\n\n **Total Price: ₹{total_price}**\n **Order Placed Successfully!**"
    brand_recommendations = best_brands_recommendation(cart)
    cart.clear()  
    return summary + "\n\nBest Brands for Your Selected Products:\n" + brand_recommendations

def add_to_cart(product_name):
    for product in products:
        if product["name"] == product_name:
            cart.append(product)
            break
    return format_cart()

with gr.Blocks(css=css_style,elem_classes=["screen"]) as ui:
    gr.Markdown("# Nykaa",elem_classes=["heading"])
    gr.Markdown(css_style)
    cart_output = gr.Textbox(label="Shopping Cart", interactive=False)
    gr.Markdown("<br><br>", visible=True)

    for i in range(0, len(products), 4):
        with gr.Row(equal_height=True,elem_classes=["gr-row"]):  
            for product in products[i:i+4]:
                with gr.Column(scale=1, min_width = 250,elem_classes=["box"]): 
                    gr.Image(product['image'] ,interactive=False, type="pil", height=300, width=250)
                    gr.Markdown(f"**{product['name']}** - {product['price']}")
                    button = gr.Button(f"Add {product['name']} to Cart",elem_classes=["custom-button"])
                    button.click(fn=add_to_cart, inputs=[gr.Textbox(value=product["name"], visible=False)], outputs=[cart_output])
                    
        gr.Markdown("<br><br>", visible=True)   
    checkout_button = gr.Button("Checkout", elem_classes=["custom-button"])
    checkout_button.click(fn=checkout, inputs=[], outputs=[cart_output])
    
    auto = gr.Button("Nykaa Website", elem_classes=["custom-button"])
    auto_output = gr.Textbox(label="Script Output", interactive=False)
    auto.click(fn=automation, inputs=[], outputs=[auto_output])

ui.launch()
