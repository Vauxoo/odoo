from . import models


def pre_init_hook(env):
    env.cr.execute("CREATE TABLE test_uuid_ids_legacy (id SERIAL PRIMARY KEY, code UUID)")
