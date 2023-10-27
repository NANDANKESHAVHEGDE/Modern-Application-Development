@app.route('/edit-cart-item/<int:cart_item_id>', methods=['GET', 'POST'])
def user_edit_cart_item(cart_item_id):
    if not is_logged_in('user'):
        return redirect(url_for('user_login'))
    
    cart_item = Cart.query.get_or_404(cart_item_id)

    if request.method == 'POST':
        new_quantity = int(request.form['quantity'])
        if 0 < new_quantity <= cart_item.product.Stocks:
            cart_item.quantity = new_quantity
            db.session.commit()
            flash('Cart item updated successfully!', 'success')
        else:
            flash('Invalid quantity or insufficient stocks.', 'error')

    return redirect(url_for('user_cart'))

@app.route('/delete-cart-item/<int:cart_item_id>', methods=['POST'])
def user_delete_cart_item(cart_item_id):
    if not is_logged_in('user'):
        return redirect(url_for('user_login'))
    
    cart_item = Cart.query.get_or_404(cart_item_id)

    # Update the inventory stocks
    cart_item.product.Stocks += cart_item.quantity
    db.session.delete(cart_item)
    db.session.commit()

    flash('Cart item deleted successfully!', 'success')
    return redirect(url_for('user_cart'))

@app.route('/review-orders')
def user_review_orders():
    if not is_logged_in('user'):
        return redirect(url_for('user_login'))

    user_id = session.get('user_id')
    orders = Order.query.filter_by(user_id=user_id).all()

    return render_template('user_review_orders.html', orders=orders)
