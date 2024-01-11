# pyright: reportUndefinedVariable=false
@app.command(name="test")
def cli_test_command():
  print("Test command")
