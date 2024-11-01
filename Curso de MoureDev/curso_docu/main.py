from typing import Literal


def get_status(status: Literal['active', 'inactive', 'pending']) -> str:
    if status == 'active':
        return "The status is active."
    elif status == 'inactive':
        return "The status is inactive."
    else:
        return "The status is pending."


# Uso correcto
print(get_status('active'))   # Imprime: The status is active.

# Uso incorrecto (esto causaría un error de tipo en tiempo de análisis estático)
# Esto genera un error en linters o mypy, pero no en tiempo de ejecución.
print(get_status('unknown'))
