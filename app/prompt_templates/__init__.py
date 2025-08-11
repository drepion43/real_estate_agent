import os


dirname = os.getenv("PROMPT_TEMPLATES")


def read_template(filename):
    with open(os.path.join(dirname, filename), 'r') as f:
        template = f.read()
    return template
