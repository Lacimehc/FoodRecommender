from flask import Flask, render_template, url_for, redirect, request
import psycopg2
import base64
import re

app = Flask(__name__)

postgresql_url = "postgresql://firstdb_owner:hFvAz4V7YJZE@ep-dark-darkness-a1madbxh.ap-southeast-1.aws.neon.tech/recipe?sslmode=require"

connection = psycopg2.connect(postgresql_url)

@app.route("/", methods = ["GET", "POST"])
def swiper():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from recipe")
            recipes = cursor.fetchall()
            
        recipe_entries = []
    for recipe in recipes:
        image_data = recipe[5]
        if image_data:
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        else:
            image_base64 = None

        ingredient_string = recipe[2]
        ingredient_list = re.findall(r"'(.*?)'", ingredient_string)
        ingredient_list = [ingredient.strip("' ") for ingredient in ingredient_list]
        
        step_string = recipe[3]
        step_list = re.findall(r"'(Bước \d+:.*?)'", step_string)
        step_list = [step.strip("' ") for step in step_list]

        recipe_entries.append({
            'id': recipe[0],
            'name': recipe[1],
            'ingredient': ingredient_list,
            'step': step_list,
            'serving': recipe[4],
            'image': image_base64
        })
    
    return render_template("card_slider.html", entries = recipe_entries)

if __name__ == '__main__':
    app.run(debug=True)