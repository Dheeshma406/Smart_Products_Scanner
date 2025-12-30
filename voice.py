try:
    import pyttsx3
except:
    pyttsx3 = None

_engine = None


def get_engine():
    global _engine

    if pyttsx3 is None:
        return None

    if _engine is None:
        _engine = pyttsx3.init(driverName="sapi5")
        _engine.setProperty("rate", 160)
        _engine.setProperty("volume", 1.0)

    return _engine


def speak_product(product):
    engine = get_engine()
    if engine is None:
        return

    text = (
        f"Product name {product['product_name']}. "
        f"Brand {product['brand']}. "
        f"Weight {product['weight']}. "
        f"Price rupees {product['price']}. "
        f"Expiry date {product['expiry']}."
    )

    engine.stop()
    engine.say(text)
    engine.runAndWait()
