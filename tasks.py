from invoke import task


def black(c, check):
    c.run("isort .")
    return c.run(
        f"black tasks.py mybot/ scripts/ --line-length=79 {'--check' if check is True else ''}"
    )


@task(aliases=["f"])
def format(c):
    return black(c, False)


@task(aliases=["cf", "fc"])
def check_format(c):
    return black(c, True)


@task(aliases=["ct"])
def check_templates(c):
    return c.run(
        "checkov -o json --output-file-path results/checkov --quiet --skip-resources-without-violations"
    )
