import subprocess

packages = ['tqdm', 'requests', 'urllib', 'time', 're', 'configparser']

for package in packages:
    try:
        subprocess.check_call(['pip', 'install', package])
        print(f'Successfully installed {package}')
    except subprocess.CalledProcessError:
        print(f'Error installing {package}')

print('All packages installed successfully!')
