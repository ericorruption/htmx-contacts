Create a virtual env:

```bash
python3 -m venv .venv
```

Use virtual env:

```bash
. .venv/bin/activate
```

Install dependencies:

```bash
# After activating virtual env
pip install -r requirements.txt
```

Running the flask app locally:

```bash
# After activating virtual env
flask --debug run
```

Follow the terminal instructions to find the address of the app.

## Installing new dependencies

Don't forget to re-generate requirements.txt after installing new dependencies:

```bash
pip freeze > requirements.txt
```
