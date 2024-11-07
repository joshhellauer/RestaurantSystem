
from flask import Flask, render_template, redirect, request, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Category, Order, Product, engine, orders_engine
import json

app = Flask(__name__)
app.secret_key = "example123"
order_engine = create_engine("sqlite:///order.db")

#Automatically reroute to main_page
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        x = 1

    return redirect(url_for('main_page', category_name="Featured Favorites"))

# Route to display all outstanding orders in the database
@app.route('/kitchen', methods=['GET']) 
def kitchen():
    SessionOrders = sessionmaker(bind=orders_engine)
    db_session = SessionOrders()
    # get all outstanding orders from the database
    orders = db_session.query(Order).all()

    # Process order_data and create a list of dictionaries with individual values
    processed_orders = []
    for order in orders:
        order_data = order.order_data
        print(order_data)
        data = json.loads(order_data)
        order_dict = {
            'id': order.id,
            "quantities": data.get("quantities", []),
            "product_names": data.get("product_names", []),
            "prices": data.get("prices", []),
            "customer_name": order.name
        }

        processed_orders.append(order_dict)

    return render_template('kitchen.html', orders=processed_orders)
    


# Route to display category content
@app.route('/main_page/<category_name>', methods=['GET', 'POST'])
def main_page(category_name):
    
    Session = sessionmaker(bind=orders_engine)
    db_session = Session()
    if request.method == 'POST':
        order_summary = request.form.get('order-ticket')
        customer_name = request.form.get('customer-name')
        # must split the form data due to the way it is formatted with the javascript
        order_items = order_summary.split('\r\n')
        quantities = []
        product_names = []
        prices = []

        # iterate through rows and split each row into quantity, product name, and price
        for row in order_items:
            if row:
                fields = row.split('\t')
                quantities.append(fields[0])
                product_names.append(fields[1])
                prices.append(fields[2])
        order_data = {
            "quantities": quantities,
            "product_names": product_names,
            "prices": prices,
            "customer_name": customer_name
        }
        # hanlde Flask's session object vs the database session object carefully
        session['order_data'] = order_data
        order_data = json.dumps(order_data)
        the_order = Order(name=customer_name, order_data=order_data)
        db_session.add(the_order)
        db_session.commit()

                
        
        return redirect(url_for('transaction_page', order_id=the_order.id))

    Session = sessionmaker(bind=engine)
    db_session = Session()

    category = db_session.query(Category).filter_by(name=category_name).first()
    if category:
        # returns all products of the given category 
        category_products = db_session.query(Product).filter_by(category_id=category.id).all()

        db_session.close()
        return render_template('main_page.html', category_name=category_name, products=category_products)
    else:
        return "Category not found"
    
@app.route('/products/<int:product_id>', methods=['GET', 'POST'])
def get_product(product_id):
    # handle database session vs Flask session object
    Session = sessionmaker(bind=orders_engine)
    db_session = Session()
    if request.method == 'POST':

        order_summary = request.form.get('order-ticket')
        customer_name = request.form.get('customer-name')
        # split the textarea string because of how it gets formatted with the js
        order_items = order_summary.split('\r\n')
        quantities = []
        product_names = []
        prices = []

        # go through eac hsub string and further pick out the different fields of each item
        for row in order_items:
            if row:
                fields = row.split('\t')
                quantities.append(fields[0])
                product_names.append(fields[1])
                prices.append(fields[2])
        order_data = {
            "quantities": quantities,
            "product_names": product_names,
            "prices": prices,
            "customer_name": customer_name
        }
        order_data = json.dumps(order_data)
        
        the_order = Order(name=customer_name, order_data=order_data)


        order_data = {
            "quantities": quantities,
            "product_names": product_names,
            "prices": prices,
            "customer_name": customer_name,
            "id": the_order.id
        }
        session['order_data'] = order_data
        db_session.add(the_order)
        db_session.commit()

                
        
        return redirect(url_for('transaction_page', order_id=the_order.id))
    Session = sessionmaker(bind=engine)
    db_session = Session()

    # find the product in the data base
    product = db_session.query(Product).filter_by(id=product_id).first()
    db_session.close()

    # Check if the product was found
    if product:
        return render_template('products.html', product=product)
    else:
        return "Product not found"

@app.route('/transaction_page/<int:order_id>', methods=['GET'])
def transaction_page(order_id):
    # using Flask's session object here to retrieve the order that was just placed
    order_data = session.get('order_data', {})
    return render_template('transaction_page.html', order_data=order_data, order_id=order_id)

@app.route('/delete_order/<int:order_id>', methods=['DELETE', 'GET'])
def delete_order(order_id):
    SessionOrders = sessionmaker(bind=orders_engine)
    db_session = SessionOrders()
    order = db_session.query(Order).get(order_id)

    if order:
        db_session.delete(order)
        db_session.commit()
    else:
        return jsonify({'error': 'Order not found'}), 404

    return redirect( url_for('kitchen'))

if __name__ == "__main__":
    app.run(debug=True)
