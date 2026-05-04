import typer
from dotenv import load_dotenv

from runner.config import load_report_config
from runner.sources.file import fetch_file_source
from runner.template import render_template
from runner.emailer import send_email
from runner.sources.http import fetch_http_source
from runner.secrets import load_secrets


load_dotenv()
app = typer.Typer(help="Report Runner CLI")

@app.command()
def run(path: str, dry_run: bool=typer.Option(False, "--dry-run", help="Render report without email",),):
    typer.echo(f"Running report : {path}")
    typer.echo(f"Dry run : {dry_run}")
    try:
        config = load_report_config(path)
        report_data={}

        for yaml_source_key, yaml_source_val in config["sources"].items():
            print(yaml_source_val)
            print(yaml_source_key)

            if yaml_source_val.get('type') == "file":
                report_data[yaml_source_key] = fetch_file_source(yaml_source_val)
            elif yaml_source_val.get('type') == "http":
                secrets = load_secrets()
                report_data[yaml_source_key] = fetch_http_source(yaml_source_val, secrets)
            else:
                raise ValueError(f"Unsupported source type: {yaml_source_val.get('type')}")

            rendered_html = render_template(
            config["template"],
            {
                "report": config,
                "sources": report_data,
            },
        )
            
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    if dry_run:
        typer.echo(rendered_html)
    else:
        typer.echo("Report rendered successfully.")
        typer.echo(rendered_html)
        send_email(config["email"], rendered_html)



@app.command()
def validate(path: str):
    """Validate a report YAML file."""
    typer.echo(f"Validating report: {path}")
    try:
        config = load_report_config(path)
    except Exception as e:
        typer.echo(f"Invalid report config: {e}")
        raise typer.Exit(code=1)

    typer.echo(f"Valid report config: {config['name']}")



