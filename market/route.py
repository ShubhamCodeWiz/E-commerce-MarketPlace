from market import app,db
from flask import render_template,redirect,url_for,flash,request
from market.model import Item,User
from market.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm
from flask_login import login_user,logout_user,current_user,login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/market", methods=["GET", "POST"])
@login_required  # Ensure the user is logged in to make purchases
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()

    def purchase_item(item_id):
        item = Item.query.get(item_id)
        if item:
            if current_user.budget >= item.price:
                try:
                    current_user.budget -= item.price
                    item.owner = current_user.id

                    db.session.commit()
                    flash(f"Successfully purchased {item.name}!", 'success')
                except Exception as e:
                    db.session.rollback()
                    flash("An error occurred while purchasing the item.", 'danger')
                    print(f"Error purchasing item: {e}")
            else:
                flash("Insufficient budget to purchase this item.", 'danger')
        else:
            flash("Item not found.", 'danger')

    if purchase_form.validate_on_submit():
        print("POST request received.")  # Debugging statement
        try:
            item_id = request.form.get("item_id")
            print(f"Item ID from form: {item_id}")  # Debugging statement
            if item_id:
                item_id = int(item_id)
                purchase_item(item_id)
        except ValueError:
            flash("Invalid item ID.", 'danger')

    def sell_item(item_id):
        item = Item.query.get(item_id)
        if item:
            try:
                current_user.budget += item.price
                item.owner = None

                db.session.commit()
                flash(f"Successfully sells {item.name}!", 'success')
            except Exception as e:
                db.session.rollback()
                flash("An error occurred while purchasing the item.", 'danger')
                print(f"Error purchasing item: {e}")
        else:
            flash("Item not found.", 'danger')

    if sell_form.validate_on_submit():
        print("POST request received.")  # Debugging statement
        try:
            item_id = request.form.get("submit")
            print(f"Item ID from form: {item_id}")  # Debugging statement
            if item_id:
                item_id = int(item_id)
                sell_item(item_id)
        except ValueError:
            flash("Invalid item ID.", 'danger')
            
            
    owned_items = Item.query.filter_by(owner=current_user.id)
        
    items = Item.query.filter_by(owner=None)
    return render_template("market.html", items=items,purchase_form=purchase_form,sell_form=sell_form,owned_items=owned_items)



@app.route("/register" ,methods=["GET","POST"])
def register_page():
    forms = RegisterForm()
    if forms.validate_on_submit():
        new_user = User(username=forms.username.data,
                        email=forms.email.data,
                        password = forms.password1.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("market_page"))

# Check and print errors if any
    elif forms.errors!={}:
        for err in forms.errors.values():
            flash(f'There is an error in creating a user: {err}')
        
    else:
        print("something wrong")
    return render_template("register.html",forms=forms)

@app.route("/login",methods=["GET","POST"])
def login_page():
    forms = LoginForm()
    if forms.validate_on_submit():
        attempted_user = User.query.filter_by(username=forms.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=forms.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as:{attempted_user.username}")
            return redirect(url_for('market_page'))
        else:
            flash("Username and Password does not match! please try again")

    return render_template("login.html",forms=forms)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!")
    return redirect("/home")

