#!/bin/bash

# wrapper to run all available tests
for TEST in `ls test_*.yml` do;
  ansible-playbook -i hosts ${TEST}
done;

