#!/usr/bin/env python3
"""Site now runs on Cloudflare Workers (static assets). Kept for the old command name."""
import runpy, sys, pathlib
sys.argv = [str(pathlib.Path(__file__).with_name("deploy_worker.py"))] + sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
