
python -c "
from app.instance.models import DatabaseDriver
t = DatabaseDriver()
t.drop_all()
"
