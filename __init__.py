from click import group

from main import mget, mput


@group("mm")
def mm():
    ...


mm.add_command(mget)
mm.add_command(mput)
mm()
