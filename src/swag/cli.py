import fire

def hello(name='World'):
  return f'Hello {name}!'

def main():
  fire.Fire(hello)
