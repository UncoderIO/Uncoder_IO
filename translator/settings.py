import os


INIT_FUNCTIONS = os.getenv("INIT_FUNCTIONS", '0').lower() in ('true', '1', 't')
