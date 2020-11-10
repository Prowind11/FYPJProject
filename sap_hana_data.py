from hana_ml import dataframe
from hana_ml import ConnectionContext

def __get_connection():
    conn = dataframe.ConnectionContext(address='cdab230a-29d1-4a66-ab93-eb0ec219ed8b.hana.trial-us10.hanacloud.ondemand.com', port='443', user='MOVIE_PROJECT_HDI_DB_1_4T01X86GTZG3PJFBDJJ4FGMZR_RT', password='Rh0wQ9.bsJ.2NG_K2x73D.0J06Hh8UTNIE_FAohpy9M5ocviZiyFN8WgR_uq6.kPX0fMR-ASiJrm7za9_uNs_hAsceXRW_qM9vBSTlWbUYPv1dozzBHgukbN4m_6WkaU', encrypt='true', sslValidateCertificate='false')
    return conn
