from glob import glob
from pathlib import Path
import subprocess

from svdconv.svd import write_spec_for_device

sample_files = glob('samples/*.svd')

for sample_file in sample_files:
    output_folder = Path(sample_file).with_suffix('')
    output_folder.mkdir(parents=True, exist_ok=True)
    write_spec_for_device(sample_file, output_folder)

    # Format the generated sources
    subprocess.run(['gnatformat', *glob(f'{output_folder}/*.ads')])
