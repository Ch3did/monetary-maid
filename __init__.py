from click import group

from main import mconf, mget, mput, mup


@group("mm")
def mm():
    ...


mm.add_command(mget)
mm.add_command(mput)
mm.add_command(mconf)
mm.add_command(mup)
mm()
