from __future__ import annotations

def test_add_and_list(cli_runner, task_file, capsys):
    assert cli_runner(["add", "Write spec", "--priority", "high", "--due", "2024-03-20"]) == 0
    assert cli_runner(["add", "Plan tests"]) == 0

    assert cli_runner(["list", "--all"]) == 0
    output = capsys.readouterr().out
    assert "Write spec" in output
    assert "Plan tests" in output


def test_complete_flow(cli_runner, task_file, capsys):
    cli_runner(["add", "Finish doc"])
    cli_runner(["add", "Ship feature"])

    assert cli_runner(["complete", "1"]) == 0
    assert cli_runner(["complete", "1"]) == 1  # cannot double complete
    error_output = capsys.readouterr().err
    assert "already completed" in error_output

    cli_runner(["list", "--completed"])
    list_output = capsys.readouterr().out
    assert "Finish doc" in list_output


def test_complete_dry_run_does_not_save(cli_runner, task_file, capsys):
    cli_runner(["add", "Dry run test"])
    cli_runner(["--dry-run", "complete", "1"])
    cli_runner(["list"])
    output = capsys.readouterr().out
    assert "Dry run test" in output


def test_delete_force(cli_runner, task_file, capsys):
    cli_runner(["add", "Delete me"])
    assert cli_runner(["delete", "--force", "1"]) == 0
    cli_runner(["list", "--all"])
    assert "No tasks" in capsys.readouterr().out
