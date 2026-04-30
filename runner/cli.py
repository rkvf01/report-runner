import typer
from runner.config import load_report_config
from runner.sources.file import fetch_file_source
from runner.template import render_template

app = typer.Typer(help="Report Runner CLI")

@app.command()
def run(path: str, dry_run: bool=typer.Option(False, "--dry-run", help="Render report without email",),):
    typer.echo(f"Running report : {path}")
    typer.echo(f"Dry run : {dry_run}")
    try:
        config = load_report_config(path)
        report_input={}

        for yaml_source_key, yaml_source_val in config["sources"].items():
            print(yaml_source_val)
            print(yaml_source_key)

            if yaml_source_val.get('type') == "file":
                report_input[yaml_source_key] = fetch_file_source(yaml_source_val)
            else:
                raise ValueError(f"Unsupported source type: {yaml_source_val.get('type')}")

            rendered_html = render_template(
            config["template"],
            {
                "report": config,
                "sources": report_input,
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



