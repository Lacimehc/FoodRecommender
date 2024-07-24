import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error

with open('unit.json', 'r', encoding='utf-8') as f:
    unit_mapping = json.load(f)

with open('factors.json', 'r', encoding='utf-8') as f:
    conversion_factors = json.load(f)

# Từ điển ánh xạ tên thực phẩm đồng nghĩa về một tên chung
food_name_mapping = {
    'thịt ba chỉ': 'thịt ba chỉ',
    'thịt ba rọi': 'thịt ba chỉ',
    # Thêm các ánh xạ tên thực phẩm khác nếu cần
}

# Hàm cập nhật đơn vị
def update_unit(unit, food_name):
    if unit in unit_mapping:
        for key, mapped_unit in unit_mapping[unit].items():
            if key == food_name:
                return mapped_unit
    return unit

# Hàm chuyển đổi đơn vị về gram
def convert_to_grams(amount, unit):
    if unit in conversion_factors:
        return amount * conversion_factors[unit]
    else:
        return None

# Hàm cập nhật tên thực phẩm
def update_food_name(food_name):
    if food_name in food_name_mapping:
        return food_name_mapping[food_name]
    return food_name

# Đọc và tiền xử lý bộ dữ liệu đầu tiên
df1 = pd.read_csv('food_name.csv', encoding='utf-8')
df1['unit'] = df1.apply(lambda row: update_unit(row['unit'], row['food_name']), axis=1)
df1['food_name'] = df1['food_name'].apply(update_food_name)  # Cập nhật tên thực phẩm
df1['weight(g)'] = df1.apply(lambda row: convert_to_grams(row['amount'], row['unit']), axis=1)

# Đọc và tiền xử lý bộ dữ liệu thứ hai
df2 = pd.read_csv('condiment.csv', encoding='utf-8')
df2['unit'] = df2.apply(lambda row: update_unit(row['unit'], row['food_name']), axis=1)
df2['food_name'] = df2['food_name'].apply(update_food_name)  # Cập nhật tên thực phẩm
df2['weight(g)'] = df2.apply(lambda row: convert_to_grams(row['amount'], row['unit']), axis=1)

# Tạo mô hình học máy cho bộ dữ liệu đầu tiên
X1 = df1[['food_name', 'weight(g)']]
y1 = df1[['calories(g)', 'fats(g)', 'carbs(g)', 'protein(g)', 'saturated_fat(g)', 'cholesterol(mg)', 'sodium(mg)', 'dietary_fiber(g)', 'sugars(g)', 'calcium(mg)', 'iron(mg)', 'potassium(mg)', 'vitamin_A(mcg)', 'vitamin_C(mg)']]

preprocessor1 = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), ['food_name'])
    ], remainder='passthrough'
)

model1 = Pipeline(steps=[
    ('preprocessor', preprocessor1),
    ('regressor', RandomForestRegressor(
        bootstrap= True, 
        ccp_alpha= 0.0, 
        max_depth= 20, 
        max_leaf_nodes= None, 
        min_samples_leaf= 1, 
        min_samples_split= 2, 
        min_weight_fraction_leaf= 0.0, 
        n_estimators= 300, 
        oob_score= True, 
        warm_start= True, 
        random_state=66
        ))
])

X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=66)
model1.fit(X1_train, y1_train)

# Tạo mô hình học máy cho bộ dữ liệu thứ hai
X2 = df2[['food_name', 'weight(g)']]
y2 = df2[['calories(g)', 'fats(g)', 'carbs(g)', 'protein(g)', 'saturated_fat(g)', 'cholesterol(mg)', 'sodium(mg)', 'dietary_fiber(g)', 'sugars(g)', 'calcium(mg)', 'iron(mg)', 'potassium(mg)', 'vitamin_A(mcg)', 'vitamin_C(mg)']]

preprocessor2 = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), ['food_name'])
    ], remainder='passthrough'
)

model2 = Pipeline(steps=[
    ('preprocessor', preprocessor2),
    ('regressor', RandomForestRegressor(
        bootstrap= True, 
        ccp_alpha= 0.0, 
        max_depth= 20, 
        max_leaf_nodes= None, 
        min_samples_leaf= 1, 
        min_samples_split= 2, 
        min_weight_fraction_leaf= 0.0, 
        n_estimators= 300, 
        oob_score= True, 
        warm_start= True, 
        random_state=66
        ))
])

X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=66)
model2.fit(X2_train, y2_train)

def predict_total_nutrition(food_items):
    total_nutrition = {'calories': 0, 'fats': 0, 'carbs': 0, 'protein': 0, 'saturated_fat': 0,'cholesterol': 0, 'sodium': 0, 'dietary_fiber': 0, 'sugars': 0, 'calcium': 0, 'iron': 0, 'potassium': 0, 'vitamin_A': 0, 'vitamin_C': 0}
    # not_found = []
    # unsupported_units = []
    issues = []
    for food_name, amount, unit in food_items:
        amount = float(amount)
        
        food_name = update_food_name(food_name)
        unit = update_unit(unit, food_name)            
        weight_in_grams = convert_to_grams(amount, unit)
        
        if weight_in_grams is None:
            issues.append((food_name, amount, unit))
            continue
        
        nutrition1 = None
        nutrition2 = None

        if food_name in df1['food_name'].values:
            nutrition1 = model1.predict(pd.DataFrame([[food_name, weight_in_grams]], columns=['food_name', 'weight(g)']))
        if food_name in df2['food_name'].values:
            nutrition2 = model2.predict(pd.DataFrame([[food_name, weight_in_grams]], columns=['food_name', 'weight(g)']))

        if nutrition1 is not None and nutrition2 is not None:
            nutrition = (nutrition1 + nutrition2) / 2
        elif nutrition1 is not None:
            nutrition = nutrition1
        elif nutrition2 is not None:
            nutrition = nutrition2
        else:
            issues.append((food_name, amount, unit))
            continue

        print(f"Nguyên liệu: {food_name}, Khối lượng: {amount} {unit} ({weight_in_grams}g)")
        print(f"  Calories: {nutrition[0][0]:.2f}")
        print(f"  Chất béo: {nutrition[0][1]:.2f}g")
        print(f"  Chất béo bão hòa: {nutrition[0][4]:.2f}g")
        print(f"  Cholesterol: {nutrition[0][5]:.2f}mg")
        print(f"  Natri: {nutrition[0][6]:.2f}mg")
        print(f"  Carbohydrate: {nutrition[0][2]:.2f}g")
        print(f"  Chất xơ: {nutrition[0][7]:.2f}g")
        print(f"  Đường: {nutrition[0][8]:.2f}g")
        print(f"  Protein: {nutrition[0][3]:.2f}g")
        print(f"  Canxi: {nutrition[0][9]:.2f}mg")
        print(f"  Sắt: {nutrition[0][10]:.2f}mg")
        print(f"  Kali: {nutrition[0][11]:.2f}mg")
        print(f"  Vitamin A: {nutrition[0][12]:.2f}mcg")
        print(f"  Vitamin C: {nutrition[0][13]:.2f}mg")
        print()
        total_nutrition['calories'] += nutrition[0][0]
        total_nutrition['fats'] += nutrition[0][1]
        total_nutrition['saturated_fat'] += nutrition[0][4]
        total_nutrition['cholesterol'] += nutrition[0][5]
        total_nutrition['sodium'] += nutrition[0][6]
        total_nutrition['carbs'] += nutrition[0][2]
        total_nutrition['dietary_fiber'] += nutrition[0][7]
        total_nutrition['sugars'] += nutrition[0][8]
        total_nutrition['protein'] += nutrition[0][3]
        total_nutrition['calcium'] += nutrition[0][9]
        total_nutrition['iron'] += nutrition[0][10]
        total_nutrition['potassium'] += nutrition[0][11]
        total_nutrition['vitamin_A'] += nutrition[0][12]
        total_nutrition['vitamin_C'] += nutrition[0][13]
        
    if issues:
        for item in issues:
            food_name, amount, unit = item
            if food_name not in df1['food_name'].values or food_name not in df2['food_name'].values:
                print(f"- Nguyên liệu không tìm thấy: {food_name}")
            if unit not in conversion_factors:
                print(f"- Đơn vị không được hỗ trợ: {food_name} ({amount} {unit})")
        print()
        
    for key in total_nutrition:
        total_nutrition[key] = round(total_nutrition[key], 2)
        
    return total_nutrition

# Main logic
if __name__ == "__main__":
    from ingredient_selection import get_user_input, show_recipes_and_predict

    print("Mời bạn chọn:")
    print("1. Nhập thủ công")
    print("2. Chọn thực đơn có sẵn")

    choice = input("Nhập lựa chọn của bạn (1 hoặc 2): ").strip()

    if choice == '1':
        food_items = get_user_input()
    elif choice == '2':
        food_items = show_recipes_and_predict('recipe.csv')
    else:
        print("Lựa chọn không hợp lệ.")
        exit()

    # Predict and display nutritional information
    total_nutrition = predict_total_nutrition(food_items)
    print("Tổng lượng dinh dưỡng cho các nguyên liệu đã nhập:")
    print(f"  Calories: {total_nutrition['calories']:.2f}")
    print(f"  Chất béo: {total_nutrition['fats']:.2f}g")
    print(f"  Chất béo bão hòa: {total_nutrition['saturated_fat']:.2f}g")
    print(f"  Cholesterol: {total_nutrition['cholesterol']:.2f}mg")
    print(f"  Natri: {total_nutrition['sodium']:.2f}mg")
    print(f"  Carbohydrate: {total_nutrition['carbs']:.2f}g")
    print(f"  Chất xơ: {total_nutrition['dietary_fiber']:.2f}g")
    print(f"  Đường: {total_nutrition['sugars']:.2f}g")
    print(f"  Protein: {total_nutrition['protein']:.2f}g")
    print(f"  Canxi: {total_nutrition['calcium']:.2f}mg")
    print(f"  Sắt: {total_nutrition['iron']:.2f}mg")
    print(f"  Kali: {total_nutrition['potassium']:.2f}mg")
    print(f"  Vitamin A: {total_nutrition['vitamin_A']:.2f}mcg")
    print(f"  Vitamin C: {total_nutrition['vitamin_C']:.2f}mg")