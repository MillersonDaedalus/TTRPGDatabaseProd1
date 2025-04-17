import datetime
import os
import zipfile
import json
import hashlib
from django.conf import settings
from django.core.files.storage import default_storage


def create_lsc_file(source_name, source_abbr, version, json_files, output_path):
    """
    Creates an LSC file from multiple JSON fixtures
    """
    metadata = {
        'source_name': source_name,
        'source_abbr': source_abbr,
        'version': version,
        'created_at': datetime.now().isoformat(),
        'files': [os.path.basename(f) for f in json_files]
    }

    checksum = hashlib.sha256()

    with zipfile.ZipFile(output_path, 'w') as z:
        # Add metadata
        z.writestr('metadata.json', json.dumps(metadata))

        # Add all JSON files and calculate checksum
        for json_file in json_files:
            with open(json_file, 'rb') as f:
                content = f.read()
                checksum.update(content)
                z.writestr(os.path.basename(json_file), content)

    return checksum.hexdigest()


def extract_lsc_file(lsc_path, extract_to):
    """
    Extracts an LSC file to the specified directory
    """
    if not os.path.exists(lsc_path):
        raise FileNotFoundError(f"LSC file not found at {lsc_path}")

    os.makedirs(extract_to, exist_ok=True)
    metadata = {}

    with zipfile.ZipFile(lsc_path) as z:
        # Extract metadata
        if 'metadata.json' in z.namelist():
            with z.open('metadata.json') as f:
                metadata = json.load(f)

        # Extract all files
        z.extractall(extract_to)

    return metadata


def get_fixture_paths_for_source(source):
    """
    Returns all fixture file paths associated with a content source
    """
    # Implement based on how you associate models with sources
    fixtures_dir = os.path.join(settings.BASE_DIR, 'myapp', 'fixtures')
    source_files = []

    for root, dirs, files in os.walk(fixtures_dir):
        for file in files:
            if file.endswith('.json') and source.abbreviation.lower() in file.lower():
                source_files.append(os.path.join(root, file))

    return source_files