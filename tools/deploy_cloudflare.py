#!/usr/bin/env python3
"""Deploy site/ to the Cloudflare Worker `educationdew` (educationdew.com).

Usage: python3 tools/deploy_cloudflare.py site
Runs tools/deploy_worker.py: brand.py + seo.py on site/ (in place), D1 migrations, asset upload, Worker code.
"""
import runpy, sys, pathlib
sys.argv = [str(pathlib.Path(__file__).with_name("deploy_worker.py"))] + sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
