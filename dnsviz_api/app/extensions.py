from flask_cors import CORS
from flask_talisman import Talisman

from dnsviz_api.app.database.DGraphConnection import DGraphConnection


cors = CORS()
talisman = Talisman()
db = DGraphConnection()