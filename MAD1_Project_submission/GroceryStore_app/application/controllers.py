import matplotlib.pyplot as plt
import datetime
import calendar
from datetime import datetime,timedelta
from flask import Flask, request,flash
from flask import render_template,redirect, url_for, session
from flask import current_app as app
from .database import db
from .forms import AddProductForm, EditProductForm
from application.models import User,Manager,InventoryProduct,Cart,Order

def is_logged_in(role):
    return session.get(role)

@app.route('/')
@app.route('/home')
def home_page():

    return render_template('home.html')

@app.route('/register-user', methods=['POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email_id = request.form['email_id']

        if User.query.filter_by(user_name=username).first():
            return render_template('home.html', error="Username already taken. Please choose a different username.")

        new_user = User(user_name=username, password=password,email_id=email_id)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!', 'success')


        return redirect(url_for('home_page'))

    return render_template('home.html')

@app.route('/user-login', methods=['GET', 'POST'])
def User_login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(user_name=username, password=password).first()

        if user:
            session['user'] = username
            session['user_id'] = user.user_id  # Store the user_id in the session
            return redirect(url_for('user_dashboard'))
        else:
            return render_template('user_login.html', error="Invalid credentials")

    return render_template('user_login.html')

@app.route('/manager-login', methods=['GET', 'POST'])
def Manager_login():

    if request.method == 'POST':
        managername = request.form['managername']
        password = request.form['password']

        manager = Manager.query.filter_by(manager_name=managername, password=password).first()

        if manager:
            session['manager'] = managername
            return redirect(url_for('manager_dashboard'))
        else:
            return render_template('manager_login.html', error="Invalid credentials")

    return render_template('manager_login.html')

@app.route('/manager-dashboard')
def manager_dashboard():

    if not is_logged_in('manager'):
        return redirect(url_for('Manager_login'))

    products = InventoryProduct.query.all()

    return render_template('manager_dashboard.html', products=products)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():

    if not is_logged_in('manager'):
        return redirect(url_for('Manager_login'))

    form = AddProductForm()

    if form.validate_on_submit():

        new_product = InventoryProduct(Product_ID=form.product_id.data, Category_ID=form.category_id.data,Category_Name=form.category_name.data,
                                       Product_Name=form.product_name.data, Manufacture_date=form.manufacture_date.data,
                                       Expiry_date=form.expiry_date.data, Price_per_unit=form.price_per_unit.data,
                                       Stocks=form.stocks.data, Unit=form.unit.data)
        
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('manager_dashboard'))

    return render_template('add_product.html', form=form)

@app.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):

    if not is_logged_in('manager'):
        return redirect(url_for('Manager_login'))

    product = InventoryProduct.query.get_or_404(product_id)
    form = EditProductForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            product.Category_ID = form.category_id.data
            product.Category_Name = form.category_name.data
            product.Product_Name = form.product_name.data
            product.Manufacture_date = form.manufacture_date.data
            product.Expiry_date = form.expiry_date.data
            product.Price_per_unit = form.price_per_unit.data
            product.Stocks = form.stocks.data
            product.Unit = form.unit.data

            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('manager_dashboard'))
        else:
            flash('Form validation failed. Please check the input.', 'error')

    form.product_id.data = product.Product_ID
    form.category_id.data = product.Category_ID
    form.category_name.data = product.Category_Name
    form.product_name.data = product.Product_Name
    form.manufacture_date.data = product.Manufacture_date
    form.expiry_date.data = product.Expiry_date
    form.price_per_unit.data = product.Price_per_unit
    form.stocks.data = product.Stocks
    form.unit.data = product.Unit

    return render_template('edit_product.html', form=form, product=product)

@app.route('/delete-product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):

    if not is_logged_in('manager'):
        return redirect(url_for('Manager_login'))

    product = InventoryProduct.query.get_or_404(product_id)

    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()

        flash('Product deleted successfully!', 'success')
        return redirect(url_for('manager_dashboard'))

    return render_template('delete_product.html', product=product)

@app.route('/user-dashboard', methods=['GET', 'POST'])
def user_dashboard():
    if not is_logged_in('user'):
        return redirect(url_for('user_login'))

    # Get all products from the database
    products = InventoryProduct.query.all()

    # Organize products by category
    categories = {}
    for product in products:
        if product.Category_Name not in categories:
            categories[product.Category_Name] = []
        categories[product.Category_Name].append(product)

    return render_template('user_dashboard.html', categories=categories)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if not is_logged_in('user'):
        return redirect(url_for('user_login'))

    user_id = session.get('user_id')
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))

    # Check if the product exists in the inventory
    product = InventoryProduct.query.get(product_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('user_dashboard'))

    # Check if the quantity is valid and available in the inventory
    if not 0 < quantity <= product.Stocks:
        flash('Invalid quantity or insufficient stocks.', 'error')
        return redirect(url_for('user_dashboard'))

    # Check if the product is already in the user's cart
    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        # Calculate the quantity difference
        quantity_diff = quantity - cart_item.quantity

        # Check if the new quantity is valid and available in the inventory
        if 0 < quantity_diff <= product.Stocks:
            cart_item.quantity = quantity
            # Update the inventory stocks with the quantity difference
            product.Stocks -= quantity_diff
        else:
            flash('Invalid quantity or insufficient stocks.', 'error')
            return redirect(url_for('user_dashboard'))
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

        # Update the inventory stocks
        product.Stocks -= quantity

    db.session.commit()

    flash('Product added to cart successfully!', 'success')
    return redirect(url_for('user_dashboard'))

@app.route('/user-cart')
def user_cart():

    if not is_logged_in('user'):
        return redirect(url_for('user_login'))

    user_id = session.get('user_id')
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    cart_data = {}
    total_quantity = 0
    total_price = 0

    for item in cart_items:
        product = InventoryProduct.query.get(item.product_id)
        cart_data[product] = {
            'cart_item_id': item.id,
            'quantity': item.quantity,
            'price_per_unit': product.Price_per_unit,
            'total_price': item.quantity * product.Price_per_unit
        }
        total_quantity += item.quantity
        total_price += item.quantity * product.Price_per_unit


    if request.method == 'POST':
        cart_item_id = request.form.get('cart_item_id')
        quantity = int(request.form.get('quantity'))

        cart_item = Cart.query.get_or_404(cart_item_id)
        product = InventoryProduct.query.get(cart_item.product_id)

        if 1 <= quantity <= product.Stocks:
            cart_item.quantity = quantity
            cart_item.total_price = quantity * product.Price_per_unit
            db.session.commit()
            flash('Cart item updated successfully!', 'success')
        else:
            flash('Invalid quantity or not enough stocks available for this product.', 'error')

    return render_template('user_cart.html', cart_data=cart_data,total_quantity=total_quantity, total_price=total_price)

@app.route('/user-update-cart-item/<int:cart_item_id>', methods=['POST'])
def user_update_cart_item(cart_item_id):

    if not is_logged_in('user'):
        return redirect(url_for('user_login'))

    cart_item = Cart.query.get_or_404(cart_item_id)

    if request.method == 'POST':
        new_quantity = int(request.form.get('quantity', 1))
        product = InventoryProduct.query.get(cart_item.product_id)

        # Calculate the difference in quantity
        quantity_diff = new_quantity - cart_item.quantity

        # Check if the new quantity is valid and available in the inventory
        if 1 <= new_quantity <= product.Stocks + cart_item.quantity:
            # Update the product stocks and cart item quantity
            product.Stocks -= quantity_diff
            cart_item.quantity = new_quantity
            cart_item.total_price = product.Price_per_unit * new_quantity
            db.session.commit()
            flash('Cart item updated successfully!', 'success')
        else:
            flash('Invalid quantity or not enough stocks available for this product.', 'error')

    return redirect(url_for('user_cart'))

@app.route('/user-remove-cart-item/<int:cart_item_id>', methods=['POST'])
def user_remove_cart_item(cart_item_id):

    if not is_logged_in('user'):
        return redirect(url_for('user_login'))

    cart_item = Cart.query.get_or_404(cart_item_id)
    product = InventoryProduct.query.get(cart_item.product_id)

    product.Stocks += cart_item.quantity
    db.session.delete(cart_item)
    db.session.commit()
    flash('Cart item removed successfully!', 'success')

    return redirect(url_for('user_cart'))

@app.route('/user-confirm-order', methods=['POST'])
def user_confirm_order():
    if not is_logged_in('user'):
        return redirect(url_for('user_login'))

    user_id = session.get('user_id')
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    for cart_item in cart_items:
        product = InventoryProduct.query.get(cart_item.product_id)

        if cart_item.quantity <= product.Stocks:
            # Log the order details to the Order data model
            order = Order(user_id=user_id,
                          product_id=cart_item.product_id,
                          quantity=cart_item.quantity,
                          price_per_unit=product.Price_per_unit,
                          total_price=cart_item.quantity * product.Price_per_unit)
            db.session.add(order)

            # Update the inventory stocks
            product.Stocks -= cart_item.quantity

    # Clear the user's cart after submitting the order
    Cart.query.filter_by(user_id=user_id).delete()

    db.session.commit()

    flash('Order submitted successfully!', 'success')
    return redirect(url_for('user_dashboard'))

@app.route('/user-profile')
def user_profile():
    if not is_logged_in('user'):
        return redirect(url_for('user_login'))

    user_id = session.get('user_id')

    # Get user information from the User model
    user = User.query.get(user_id)

    # Get user order history from the Order model
    orders = Order.query.filter_by(user_id=user_id).all()

    return render_template('user_profile.html', user=user, orders=orders)

@app.route('/order-summary')
def order_summary():
    if not is_logged_in('manager'):
        return redirect(url_for('Manager_login'))

    # Get all orders from the Order table
    orders = Order.query.all()

    if not orders:
        return render_template('order_summary.html', message="No orders available.")

    # Create dictionaries to store user-wise data
    user_data = {}
    user_names = []

    # Aggregate total price for each user
    for order in orders:
        user_id = order.user_id
        user = User.query.get(user_id)
        user_name = user.user_name

        if user_name not in user_names:
            user_names.append(user_name)
            user_data[user_name] = {
                'order_dates': [],
                'total_amounts': []
            }

        user_data[user_name]['order_dates'].append(order.order_date.strftime('%Y-%m-%d'))
        user_data[user_name]['total_amounts'].append(order.total_price)

    # Create the bar plots
    plt.figure(figsize=(10, 8))

    # Plot total order amounts
    plt.subplot(2, 1, 1)
    for user_name in user_names:
        total_amounts = user_data[user_name]['total_amounts']
        plt.bar(user_name, sum(total_amounts))

    plt.xlabel('Users')
    plt.ylabel('Total Amount')
    plt.title('Total Order Amounts')

    # Plot order counts
    plt.subplot(2, 1, 2)
    for user_name in user_names:
        order_dates = user_data[user_name]['order_dates']
        plt.bar(user_name, len(order_dates))

    plt.xlabel('Users')
    plt.ylabel('Order Count')
    plt.title('Order Counts')

    # Adjust layout
    plt.tight_layout()

    # Save the plot to a file
    plot_file = 'static/order_summary_plot.png'
    plt.savefig(plot_file)

    return render_template('order_summary.html', plot_file=plot_file)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_page'))