
import argparse
import yaml
from pathlib import Path

def get_latest_version(version: str):
   directory = "lts" / Path(version)
   latest = -1
   latest_path = None
   for path in directory.iterdir():
      version_number = int(path.stem)
      if version_number > latest:
         latest = version_number
         latest_path = path

   return latest_path, latest_path.parent / f"{latest + 1}.yaml"

def update_snapshot(snapshot, repository, git_hash):
   packages = snapshot["packages"]

   for package in packages:
      if isinstance(package, str):
         continue

      print
      if package["git"] == f"ssh://git@github.com/{repository}.git":
         print("update hash")
         package["commit"] = git_hash



def main(version, repo, git_hash):

   input_path, output_path = get_latest_version(version)
   data = yaml.safe_load(input_path.read_text())
   update_snapshot(data, repo, git_hash)
   output_path.write_text(yaml.safe_dump(data))

   pass


if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Update a latest snapshot.')

   # Add the positional arguments
   parser.add_argument('version', help='The version of the snapshot to update (e.g. 18/28)')
   parser.add_argument('repository', help='The url of the repo to update in the snapshot (e.g. github.com/bank-manager/teir-config.git)')
   parser.add_argument('git_hash', help='Commit hash to update')

   args = parser.parse_args()

   main(args.version, args.repository, args.git_hash)
