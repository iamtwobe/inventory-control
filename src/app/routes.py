from flask import render_template, request, flash, redirect, url_for
from src.app import app, users_database, bcrypt
from src.app.models import User
from src.app.forms import FormLogin, FormSignup, FormAddBrand, FormAddCategory, FormAddProduct
from flask_login import login_user, logout_user, login_required
from sqlalchemy import text
from src.database.database_handler import AppDatabase


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'submit_button_login' in request.form:
        user = User.query.filter_by(username=form_login.account.data).first()
        email = User.query.filter_by(email=form_login.account.data).first()
        par_next = request.args.get('next')
        if email and bcrypt.check_password_hash(email.password, form_login.password.data):
            login_user(email, remember=form_login.remember_data.data)
            flash(f'Welcome, {form_login.account.data}', 'alert-success')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        elif user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember_data.data)
            flash(f'Welcome, {form_login.account.data}', 'alert-success')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Login failed. User or password incorrect.', 'alert-danger')
    
    return render_template('login.html', form_login=form_login)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form_signup = FormSignup()
    if form_signup.validate_on_submit() and 'submit_button_signup' in request.form:
        crypt_password = bcrypt.generate_password_hash(form_signup.password.data)
        user = User(username=form_signup.username.data, email=form_signup.email.data, password=crypt_password)
        users_database.session.add(user)
        users_database.session.commit()
        flash(f'Account created. You can log-in now as {form_signup.username.data} ({form_signup.email.data})', 'alert-success')
        return redirect(url_for('home'))#
    return render_template('signup.html', form_signup=form_signup)

@app.route('/inventory', methods=['GET'])
@login_required
def inventory():
    selected_category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', 'price_asc')

    query = "SELECT * FROM products"

    if selected_category:
        query += " WHERE product_category = :category"
    
    # Add sorting based on the selected option
    if sort_by == 'price_asc':
        query += " ORDER BY product_price ASC"
    elif sort_by == 'price_desc':
        query += " ORDER BY product_price DESC"
    elif sort_by == 'index_asc':
        query += " ORDER BY product_id ASC"
    elif sort_by == 'index_desc':
        query += " ORDER BY product_id DESC"

    # Connect to the database and execute the query
    engine = users_database.get_engine(app, bind='inventory')
    with engine.connect() as connection:
        # Pass the category if provided, else pass an empty string
        result = connection.execute(text(query), {'category': selected_category})
        products = result.fetchall()

    # Get all available categories for the dropdown
    categories_query = text("SELECT DISTINCT product_category FROM products")
    with engine.connect() as connection:
        result = connection.execute(categories_query)
        categories = [row[0] for row in result.fetchall()]

    return render_template('inventory.html', products=products, categories=categories, 
                           selected_category=selected_category, sort_by=sort_by)

@app.route('/add_new', methods=['GET', 'POST'])
@login_required
def add_new():
    return render_template('add_new.html')

@app.route('/add_brand', methods=['GET', 'POST'])
@login_required
def add_brand():
    form = FormAddBrand()

    if form.validate_on_submit():
        inventory_db = AppDatabase("src/database/inventory.db")
        verify = inventory_db.insert_brand(form.brand_name.data)
        inventory_db.close()
        if not verify:
            flash('Brand already exists', 'alert-danger')
            return redirect(url_for('add_brand'))
        flash('Brand added', 'alert-success')
        
        return redirect(url_for('inventory'))
    
    return render_template('add_brand.html', form=form)

@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = FormAddCategory()

    if form.validate_on_submit():
        inventory_db = AppDatabase("src/database/inventory.db")
        verify = inventory_db.insert_category(form.category_name.data)
        inventory_db.close()
        
        if not verify:
            flash('Category already exists', 'alert-danger')
            return redirect(url_for('add_category'))
        
        flash('Category added', 'alert-success')
        
        return redirect(url_for('inventory'))
    
    return render_template('add_category.html', form=form)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = FormAddProduct()

    inventory_db = AppDatabase("src/database/inventory.db")
    categories = inventory_db.get_all_table('categories')
    brands = inventory_db.get_all_table('brands')
    inventory_db.close()
    form.product_category.choices = [category.get('category_name') for category in categories]
    form.product_brand.choices = [brand.get('brand_name') for brand in brands]

    if form.validate_on_submit():
        inventory_db = AppDatabase("src/database/inventory.db")
        product_name = form.product_name.data
        product_price = form.product_price.data
        product_brand = form.product_brand.data
        product_category = form.product_category.data
        print(product_brand, product_category)

        verify = inventory_db.insert_product(
            product_name=product_name, product_price=product_price,
            product_brand=product_brand, product_category=product_category
        )
        inventory_db.close()

        if not verify:
            flash('Product already exists', 'alert-danger')
            return redirect(url_for('add_category'))

        flash('Product added successfully', 'alert-success')
        return redirect(url_for('inventory'))

    return render_template('add_product.html', form=form)