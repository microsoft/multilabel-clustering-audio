import os
import dash


from demo import create_layout, demo_callbacks

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally=True


server = app.server
app.layout = create_layout(app)
demo_callbacks(app)

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)