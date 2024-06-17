#!/bin/bash

repo_dir=$(dirname "${BASH_SOURCE[0]}")
directory_relative="bin"

directory="$repo_dir/$directory_relative"

export PATH="$directory:$PATH"

