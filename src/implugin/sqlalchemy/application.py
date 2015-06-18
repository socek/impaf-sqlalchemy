from morfdict import StringDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from impaf.application import Application


class SqlAlchemyApplication(Application):

    def _populte_default_settings(self):
        def morf_sql_url(obj, value):
            if obj['type'] == 'sqlite':
                value = 'sqlite:///%(paths:sqlite_db)s'
            else:
                value = (
                    '%(type)s://%(login)s:%(password)s@%(host)s:%(port)s/'
                    '%(name)s'
                )
            return value % obj

        def morf_main_sql_url(obj, url):
            if obj['type'] == 'sqlite':
                return 'sqlite:///%(paths:sqlite_db)s' % obj
            else:
                return (
                    '%(type)s://%(login)s:%(password)s@%(host)s:%(port)s'
                    '/postgres'
                    % obj
                )
        super()._populte_default_settings()
        dbsettings = StringDict()
        dbsettings['url'] = ''
        dbsettings.set_morf('url', morf_sql_url)
        dbsettings['mainurl'] = ''
        dbsettings.set_morf('mainurl', morf_main_sql_url)
        self.settings['db'] = dbsettings

    def _generate_registry(self, registry):
        super()._generate_registry(registry)
        engine = create_engine(self.settings['db:url'])
        registry['db_engine'] = engine
        registry['db'] = sessionmaker(bind=engine)()
