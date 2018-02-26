# -*- coding: utf-8 -*-
"""main"""

from backend.backend import create_backend

backend = create_backend()

if __name__ == '__main__':
    backend.run(host="0.0.0.0", port=5000, debug=True)
