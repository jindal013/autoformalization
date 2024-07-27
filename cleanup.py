import subprocess
import sys

def get_installed_packages():
    result = subprocess.run([sys.executable, "-m", "pip", "list", "--format=freeze"], capture_output=True, text=True)
    return [line.split('==')[0] for line in result.stdout.split('\n') if line]

def uninstall_package(package):
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package])

# Essential packages for pip functionality
core_packages = [
    "pip", "setuptools", "wheel", "certifi", "charset-normalizer", 
    "idna", "urllib3", "requests", "packaging", "six"
]

installed_packages = get_installed_packages()

packages_to_remove = []
for package in installed_packages:
    if package.lower() not in [p.lower() for p in core_packages]:
        packages_to_remove.append(package)

if packages_to_remove:
    print("The following packages will be uninstalled from your global pip environment:")
    for package in packages_to_remove:
        print(f"  - {package}")
    
    confirm = input("Do you want to proceed? (y/n): ").lower()
    if confirm == 'y':
        for package in packages_to_remove:
            print(f"Uninstalling {package}...")
            uninstall_package(package)
        print("Cleanup complete.")
    else:
        print("Operation cancelled.")
else:
    print("No packages to remove. Your global pip environment is already minimal.")

print("\nRemaining packages in your global pip environment:")
subprocess.run([sys.executable, "-m", "pip", "list"])