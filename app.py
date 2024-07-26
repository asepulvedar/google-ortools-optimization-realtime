from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from math_models.diet import solve

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Recibir datos del formulario y proporcionar valores predeterminados en caso de que estén vacíos
            parameters = [
                ["Calories (kcal)", int(request.form.get('calories', 0))],
                ["Protein (g)", int(request.form.get('protein', 0))],
                ["Calcium (g)", float(request.form.get('calcium') or 0.0)],
                ["Iron (mg)", float(request.form.get('iron') or 0.0)],
                ["Vitamin A (KIU)", float(request.form.get('vitamin_a') or 0.0)],
                ["Vitamin B1 (mg)", float(request.form.get('vitamin_b1') or 0.0)],
                ["Vitamin B2 (mg)", float(request.form.get('vitamin_b2') or 0.0)],
                ["Niacin (mg)", float(request.form.get('niacin') or 0.0)],
                ["Vitamin C (mg)", float(request.form.get('vitamin_c') or 0.0)],
            ]
        except ValueError as e:
            return f"Error en la entrada: {e}"

        # Llamar a la función solve y obtener resultados
        diet_foods, df_nutrients = solve(parameters)

        # Convertir los resultados a HTML para mostrarlos en la página de resultados
        diet_foods_html = diet_foods.to_html(classes='table table-bordered')
        df_nutrients_html = df_nutrients.to_html(classes='table table-bordered')

        # Pasar los resultados a la página de resultados
        return render_template('results.html', diet_foods_html=diet_foods_html, df_nutrients_html=df_nutrients_html)

    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
