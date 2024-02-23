from app import app
@app.route("/pcat/addnew")
def pcat_addnew():
    return "Add new product category"