# SQLAlchemy
# http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import config

engine = create_engine(config.DevelopmentConfig.DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def inint_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from taberu_admin.models.tag_models import Tag, TagSet
    from taberu_admin.models.nutrient_models import Nutrient,\
        NutrientSet, NutrientPattern, DataPattern
    from taberu_admin.models.factor_models import Factor, FactorSet
    from taberu_admin.models.unit_models import UnitCommon, UnitUscs
    Base.metadata.create_all(bind=engine)
