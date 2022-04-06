"""based on YAMLDash
https://github.com/DrGFreeman/YAMLDash
"""

import json
import webbrowser
from multiprocessing import cpu_count
from pathlib import Path

import dash
import jsonschema
import yaml
from dash import Input, Output

from gdsfactory.config import logger
from gdsfactory.icyaml.layout import layout, theme
from gdsfactory.placer import component_grid_from_yaml
from gdsfactory.read.from_yaml import from_yaml

app = dash.Dash(
    __name__,
    external_stylesheets=[
        theme,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
    ],
)

dirpath = Path(__file__).parent.parent.joinpath("schemas")
schema_path = dirpath / "netlist.json"
schema_dict = json.loads(schema_path.read_text())

mask_schema_path = dirpath / "mask.json"
mask_schema_dict = json.loads(schema_path.read_text())

logger.info(f"Loaded netlist schema from {str(schema_path)!r}")

wsgi_app = app.server
app.title = "gdsfactory webapp"
app.layout = layout


def run_debug():
    app.run_server(debug=True)
    # app.run_server(debug=True)


def run():
    print("gdsfactory webapp")
    webbrowser.open("127.0.0.1:8080", new=2)

    try:
        import waitress

        print("Listening on 127.0.0.1:8080.")
        print("Press CTRL-C to stop.")
        waitress.serve(wsgi_app, listen="127.0.0.1:8080", threads=cpu_count())

    except ModuleNotFoundError:
        print("Waitress server not found (use 'pip install waitress' to install it)")
        print("Defaulting to Flask development server.\n")

        app.run_server(port=8080)


@app.callback(
    Output("yaml_text", "className"),
    Output("yaml_feedback", "children"),
    Input("yaml_text", "value"),
    Input("dd-input-mode", "value"),
)
def validate_yaml(yaml_text, input_mode):
    class_name = "form-control"

    try:
        if yaml_text != "" and yaml_text is not None:
            yaml_dict = yaml.safe_load(yaml_text)
        else:
            return class_name, ""
    except Exception as e:
        return (class_name + " is-invalid", f"YAML ParsingError: {e}")

    if yaml_dict is not None:
        try:
            if input_mode == "netlist":
                jsonschema.validate(yaml_dict, schema_dict)
                c = from_yaml(yaml_text)
            elif input_mode == "mask":
                # print(input_mode)
                # jsonschema.validate(yaml_dict, mask_schema_dict)
                c = component_grid_from_yaml(yaml_text)
            c.show()
            return class_name + " is-valid", ""
        except (
            ValueError,
            ModuleNotFoundError,
            KeyError,
            Exception,
            jsonschema.exceptions.ValidationError,
        ) as e:
            return (class_name + " is-invalid", f"Error {e}")
    else:
        return class_name, ""
