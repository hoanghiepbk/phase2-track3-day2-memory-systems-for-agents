# Python Tips & Best Practices

## Virtual Environments
Always use virtual environments for Python projects. Use `python -m venv .venv` to create one, then activate it with `.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on Linux/Mac.

## List Comprehensions
List comprehensions are faster and more Pythonic than manual loops:
```python
# Good
squares = [x**2 for x in range(10)]

# Less ideal
squares = []
for x in range(10):
    squares.append(x**2)
```

## Type Hints
Use type hints for better code readability and IDE support:
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

## Error Handling
Use specific exception types rather than bare `except`:
```python
try:
    result = int(user_input)
except ValueError:
    print("Please enter a valid number")
```

## Async/Await
Python's `asyncio` allows concurrent I/O operations. Use `async def` for coroutines and `await` for async calls. Common pitfall: forgetting to await a coroutine makes it return a coroutine object instead of the actual result.

## Package Management
Use `pip freeze > requirements.txt` to capture dependencies. Use `pip install -r requirements.txt` to restore them. Consider using `pip-tools` for production dependency management.
