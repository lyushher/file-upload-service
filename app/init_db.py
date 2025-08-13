from __future__ import annotations
import sys
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

try:
    from app.core.database import engine
    from app.api.models import Base
except Exception as e:
    try:
        from .core.database import engine
        from .api.models import Base
    except Exception:
        raise e

def main() -> None:
    print("Veritabanı tabloları oluşturuluyor...")
    Base.metadata.create_all(bind=engine)
    print("Tablolar oluşturuldu!")

if __name__ == "__main__":
    main()
