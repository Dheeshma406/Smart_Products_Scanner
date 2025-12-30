from predict_image import predict_product
from product_lookup import get_product_details

img_path = "dataset/Product_Images/Lux_Soap/Lux1.jpg"



product_class, confidence = predict_product(img_path)
details = get_product_details(product_class)

if details:
    print("\n✅ PRODUCT FOUND")
    print("Class      :", product_class)
    print("Confidence :", round(confidence*100,2), "%")
    print("Name       :", details["product_name"])
    print("Brand      :", details["brand"])
    print("Weight     :", details["weight"])
    print("Price      :", details["price"])
    print("Expiry     :", details["expiry"])
else:
    print("❌ Product not found")
