#!/usr/bin/env python3
""" Main 101
"""
from api.v1.auth.auth import Auth

a = Auth()



excluded_paths = ["/api/v1/stat*", "/api/v1/open"]
path1 = "/api/v1/users"
path2 = "/api/v1/status"
path3 = "/api/v1/stats"

print(a.require_auth(path1, excluded_paths))  # True
print(a.require_auth(path2, excluded_paths))  # False
print(a.require_auth(path3, excluded_paths))  
