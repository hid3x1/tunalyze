#!/bin/bash

# Check if pyproject.toml exists
check_file_existence() {
    PYPROJECT_FILE="../tunalyze/pyproject.toml"
    if [ ! -f $PYPROJECT_FILE ]; then
        echo "Error: pyproject.toml not found."
        exit 1
    fi
}

# Get the current version
get_current_version() {
    grep "^version = " pyproject.toml | sed 's/version = "\(.*\)"/\1/'
}

# Update version
update_version() {
    local current_version=$1
    local update_type=$2
    IFS='.' read -ra parts <<< "$current_version"
    case $update_type in
        major)
            let parts[0]+=1
            parts[1]=0
            parts[2]=0
            ;;
        minor)
            let parts[1]+=1
            parts[2]=0
            ;;
        patch)
            let parts[2]+=1
            ;;
        *)
            if [[ $update_type =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
                echo $update_type
                return
            else
                echo "Error: Invalid argument (must be major, minor, patch, or a version number)."
                exit 1
            fi
            ;;
    esac
    echo "${parts[0]}.${parts[1]}.${parts[2]}"
}

# Main execution
main() {
    if [ -z "$1" ]; then
        echo "Error: Argument required (major, minor, patch, or a version number)."
        exit 1
    fi

    check_file_existence
    local current_version=$(get_current_version)
    local new_version=$(update_version "$current_version" "$1")

    sed -i "s/^version = .*/version = \"$new_version\"/" pyproject.toml
    echo "Version updated to $new_version."
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$1"
fi