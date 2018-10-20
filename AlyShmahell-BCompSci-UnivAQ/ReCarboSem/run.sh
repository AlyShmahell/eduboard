#!/bin/bash

(cd static && npm run build && cd .. && python server.py)

