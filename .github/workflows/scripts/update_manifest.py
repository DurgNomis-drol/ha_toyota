"""Update the manifest file."""

# pylint: skip-file

import json
import os
import sys


def update_manifest():
    """Update the manifest file."""
    version = "v0.0.0"
    for index, value in enumerate(sys.argv):
        if value in ["--version", "-V"]:
            version = sys.argv[index + 1]

    version_striped = version.replace("v", "")

    print("Version number being inserted: " + str(version_striped))

    print("Opening file...")

    with open(f"{os.getcwd()}/custom_components/toyota/manifest.json") as manifestfile:
        manifest = json.load(manifestfile)

    manifest["version"] = version_striped

    print("Manifest file after inserting new version number:")
    print(manifest)

    print("Saving file...")

    with open(
        f"{os.getcwd()}/custom_components/toyota/manifest.json", "w"
    ) as manifestfile:
        manifestfile.write(json.dumps(manifest, indent=4, sort_keys=True))

    print("Done!")


update_manifest()
