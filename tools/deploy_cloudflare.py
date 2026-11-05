#!/usr/bin/env python3
"""Deploy educationdew.com. Alias for `python3 tools/make.py deploy` (build -> check -> upload).

Usage: python3 tools/deploy_cloudflare.py [site]
"""
import pathlib, sys

TOOLS = pathlib.Path(__file__).resolve().parent
if len(sys.argv) > 2 or (len(sys.argv) == 2 and pathlib.Path(sys.argv[1]).resolve() != TOOLS.parent / "site"):
    sys.exit(__doc__ + "\nOnly the repository's site/ can be deployed (it is rebuilt first).")
sys.path.insert(0, str(TOOLS))
import make  # noqa: E402
make.main(["deploy"])
