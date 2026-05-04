import os


def load_secrets() -> dict:
    prefix = "REPORT_RUNNER_SECRET_"
    secrets = {}

    for key, value in os.environ.items():
        if key.startswith(prefix):
            secret_name = key.removeprefix(prefix)
            secrets[secret_name] = value

    return secrets
