from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()



































# import ast  # For safely evaluating literal expressions

# # Example ingredient string
# # ingredient_str = "'ức gà: 1 kg', 'ớt chuông: 2 trái', 'tỏi: 1 tbsp', 'dầu hào: 1 tbsp', 'nước tương: 2 tbsp', 'đường: 1 tsp', 'tương cà: 1 tbsp', 'tương ớt: 1 tbsp', 'gừng: 50 gram'"
# ingredient_str = " 'Bước 1: Ức gà rửa sạch, cắt khối đem luộc sơ với nước có đập dập 1 miếng gứng. Vớt ráo rồi cho vào 3 muỗng canh bột chiên giòn. Bắc chảo cho dầu vào đợi dầu nóng cho gà vào chiên vàng rồi gắp ra để ráo.', 'Bước 2: Ớt chuông bỏ hột xắt vuông, đem trụng qua nước sôi để bớt mùi hăng.', 'Bước 3: Củ hành xắt múi cau, làm chén nước sauce gồm dầu hào, nước tương, tương ớt, đường, tương cà và nước lọc, quậy đều tay.', 'Bước 4: Bắc chảo cho dầu vào phi tỏi thơm rồi cho sauce vào nấu, nước vừa cạn bớt cho thịt gà, ớt chuông, hành vào đảo đều rồi cho ra dĩa.'"

# # Safely evaluate the string to get a list
# ingredient_list = ast.literal_eval(ingredient_str)

# # Clean up each ingredient
# # cleaned_ingredients = []
# # for item in ingredient_list:
# #     # Remove leading and trailing quotes and spaces
# #     cleaned_item = item.strip("'\" ")
# #     cleaned_ingredients.append(cleaned_item)

# cleaned_ingredients = [item.strip("'\" ") for item in ingredient_list]

# # a = ', '.join(cleaned_ingredients)
# # print(a)
# # print(type(a))
# # Print or use cleaned ingredients

# abc = []
# abc.append({'ingredient': cleaned_ingredients})

# # print(abc)

# ban = abc[0]['ingredient']
# for step in ban:
#     print(step)
# # print(type(cleaned_ingredients))
# # print(cleaned_ingredients)
# # for ingredient in cleaned_ingredients:
# #     print(ingredient)
# # for i in abc:
# #     print(i)