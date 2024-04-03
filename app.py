from flask import Flask, request, render_template_string
from order import Order  # Make sure order.py is in the same directory or adjust the import path

app = Flask(__name__)

# HTML form
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Order Form</title>
</head>
<body>
    <h2>Order Form</h2>
    <form method="post">
        ID: <input type="text" name="id"><br>
        Description: <input type="text" name="description"><br>
        Quantity: <input type="number" name="quantity"><br>
        <input type="submit" value="Send">
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def order_form():
    if request.method == 'POST':
        # Extract form data
        order_id = request.form['id']
        description = request.form['description']
        quantity = request.form['quantity']
        
        # Construct order dictionary
        order = {
            'id': int(order_id),
            'description': description,
            'quantity': int(quantity)
        }
        
        # Send order
        rabbitmq_publisher = Order()
        rabbitmq_publisher.send_message(order)
        
        return 'Order sent successfully!'
    return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(debug=True)