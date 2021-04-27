print('TODO: install virtual environments from specified file(s)')

import os
import os.path
import subprocess
import venv
import yaml

print('Successfully imported yaml package')


def config1():
    return yaml.safe_load('''
virtualenvs:
  /tmp/virtualenvs/dbt-0.19.0:
    # requirements: 'path/to/requirements.txt'
    requirements: 'bin/requirements-dbt-0.19.0.txt'
    install_binary:
      - name: dbt
        alias: dbt-v0.19.0
  /tmp/virtualenvs/dbt-0.18.0:
    # requirements: 'path/to/requirements.txt'
    requirements: 'bin/requirements-dbt-0.18.0.txt'
    install_binary:
      - name: dbt
        alias: dbt-v0.18.0
''')

EXE_DEFAULT_LOCATION = '/usr/local/bin'
# EXE_DEFAULT_LOCATION = '/tmp/virtualenvs/bin'

def read_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def testit():
    install_virtualenv(config1())


def install_virtualenv(venv_configs):
    venvs = venv_configs.get('virtualenvs', [])
    # import ipdb; ipdb.set_trace();
    for venv_root, venv_config in venvs.items():
        # Create virtualenv directory
        venv.create(venv_root, symlinks=True, with_pip=True)

        # Run '${VIRTUALENV}}/env/bin/pip install -r <requirements>'
        pip_bin_path = os.path.join(venv_root, 'bin', 'pip')
        p = subprocess.Popen([pip_bin_path, 'install', '-U', 'pip', 'wheel'])
        p.wait()

        requirements_file = venv_config.get('requirements')
        # import ipdb; ipdb.set_trace();
        if requirements_file:
            pip_bin_path = os.path.join(venv_root, 'bin', 'pip')
            cmd = [pip_bin_path, 'install', '-r', requirements_file]
            p = subprocess.Popen(cmd)
            p.wait()

        # Install any binaries by the appropriate aliases
        for bin_config in venv_config.get('install_binary', []):
            name = bin_config.get('name')
            alias = bin_config.get('alias', name)
            bin_source = os.path.join(venv_root, 'bin', name)
            in_directory = bin_config.get('in_directory') or EXE_DEFAULT_LOCATION
            bin_destination = os.path.join(in_directory, alias)

            print(f'Symlinking {bin_source} -> {bin_destination}')
            os.symlink(bin_source, bin_destination)


if __name__ == '__main__':
    testit()
