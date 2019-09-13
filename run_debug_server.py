#!/usr/bin/env python

import rutertider

if __name__ == '__main__':
    app = rutertider.create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
