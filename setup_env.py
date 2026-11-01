"""Run once: create local configuration without overwriting existing secrets."""
from pathlib import Path
import secrets


def create_env(root):
    target = root / '.env'
    if target.exists():
        return False
    contents = (root / '.env.example').read_text(encoding='utf-8')
    contents = contents.replace('REPLACE_WITH_RANDOM_SECRET', secrets.token_hex(32))
    with target.open('x', encoding='utf-8') as file:
        file.write(contents)
    return True


if __name__ == '__main__':
    created = create_env(Path(__file__).resolve().parent)
    print('.env created. Set your MySQL password and port.' if created
          else '.env already exists; nothing was changed.')
