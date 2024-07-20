import csv
import textwrap
from amp import conversion_factors, unit_mapping, update_unit

# Function to get user input (same as in MLP.py)
def get_user_input():
    food_items = []
    while True:
        food_name = input("Nhập tên thực phẩm (hoặc gõ 'xong' để kết thúc): ").lower().strip()
        if food_name.strip() == 'xong':
            print()
            break
        if not food_name:
            print("Tên thực phẩm không được để trống. Vui lòng thử lại.")
            continue

        amount = input("Nhập khối lượng thực phẩm: ").strip()
        if not amount:
            print("Khối lượng thực phẩm không được để trống. Vui lòng thử lại.")
            continue
        if not amount.isdigit():
            print("Khối lượng thực phẩm phải là một số hợp lệ. Vui lòng thử lại.")
            continue
        amount = float(amount)

        unit = input("Nhập đơn vị (gram, quả, muỗng cafe, muỗng canh, ml, l): ").lower().strip()
        if not unit:
            print("Đơn vị không được để trống. Vui lòng thử lại.")
            continue

        unit = update_unit(unit, food_name)    

        if unit not in conversion_factors:
            print("Đơn vị không được hỗ trợ. Vui lòng thử lại.")
            continue

        print()
        food_items.append((food_name, amount, unit))
    
    return food_items

# Function to show recipes and predict nutrition
def show_recipes_and_predict(recipe_file):
    recipes = []
    with open(recipe_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipes.append((row['name'], eval(row['ingredient']), eval(row['step']), row['serving']))

    # Display recipes
    print("Thực đơn sẵn có:")
    for i, (name, ingredients, step, serving) in enumerate(recipes, start=1):
        print(f"{i}. {name} ({serving} người)")
        # for ingredient in ingredients:
        #     print(f"   - {ingredient}")
        print()

    # User selects a recipe
    recipe_index = int(input("Chọn thực đơn: ")) - 1
    if recipe_index < 0 or recipe_index >= len(recipes):
        print("Lựa chọn không hợp lệ.")
        return

    selected_recipe = recipes[recipe_index]
    
    # Display the selected recipe steps
    print(f"\nMón: {selected_recipe[0]}")
    print("Nguyên liệu:")
    for ingredient in selected_recipe[1]:
        print(f"   - {ingredient}")
    print("\nCác bước nấu:")
    for step in selected_recipe[2]:
        wrapped_step = textwrap.fill(step, width=100)
        print(f"   - {wrapped_step}")
        print()

    
    # Convert selected recipe ingredients into the format needed for prediction
    food_items = []
    for ingredient in selected_recipe[1]:
        food_name, amount_unit = ingredient.split(':')
        amount, unit = amount_unit.strip().split(' ', 1)
        food_items.append((food_name.strip(), float(amount), unit.strip()))

    return food_items

