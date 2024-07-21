from flask import render_template, request, Flask, url_for, flash, redirect
import psycopg2
import base64
import re 

app = Flask(__name__)

# postgresql_url = "postgresql://firstdb_owner:hFvAz4V7YJZE@ep-dark-darkness-a1madbxh.ap-southeast-1.aws.neon.tech/firstdb?sslmode=require"

#recipe table
postgresql_url = "postgresql://firstdb_owner:hFvAz4V7YJZE@ep-dark-darkness-a1madbxh.ap-southeast-1.aws.neon.tech/recipe?sslmode=require"

connection = psycopg2.connect(postgresql_url)

try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE recipe (id SERIAL, name TEXT, ingredient TEXT, step TEXT, serving INT, image BYTEA, PRIMARY KEY (id));"
            )
except psycopg2.errors.DuplicateTable:
    pass

@app.route("/home_page", methods = ["GET", "POST"])
def home():
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
    
    return render_template("home_page.html", entries = recipe_entries)

@app.route("/search_result", methods=["GET"])
def search():
    search_query = request.args.get('search_query', '')
    with connection:
        with connection.cursor() as cursor:
            if search_query:
                cursor.execute("SELECT * FROM recipe WHERE name ILIKE %s OR ingredient ILIKE %s", (f"%{search_query}%", f"%{search_query}%"))
            else:
                cursor.execute("SELECT * FROM recipe")
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

    return render_template("search_result.html", entries=recipe_entries)

@app.route("/add_recipe", methods = ["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        ingredient = request.form.get("ingredient")
        step = request.form.get("step")
        serving = int(request.form.get("serving"))
        image_file = request.files.get("image")
        
        # Validate inputs
        if not name or not ingredient or not step or not serving:
            flash("All fields are required.")
            return redirect(url_for('add'))

        try:
            serving = int(serving)
        except ValueError:
            flash("Serving must be a valid integer.")
            return redirect(url_for('add'))
        
        image_binary = image_file.read() if image_file else None
        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO recipe (name, ingredient, step, serving, image) VALUES (%s, %s, %s, %s, %s);", 
                    (
                        name,
                        ingredient,
                        step,
                        serving,
                        image_binary
                    )
                )
    return render_template("add.html")




if __name__ == '__main__':
    app.run(debug=True)