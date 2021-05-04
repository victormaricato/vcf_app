from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gene_query", methods=["POST", "GET"])
def gene_query():
    query = request.form.get("text")
    return jsonify(query)


if __name__ == "__main__":
    app.run(debug=True)
