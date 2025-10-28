"""
Packs mcstructure files into a usable MCBE add-on.
"""

from datetime import datetime
import json
from pathlib import Path
from uuid import uuid4
from tempfile import TemporaryDirectory
import zipfile

here = Path(__file__).parent
root = here.parent
logo = root / "logo.png"
structures = root / "examples/out"


def main() -> None:
    timestamp = datetime.now().strftime("%d.%m %H:%M")
    name = f"mcstructure pack - {timestamp}"
    manifest = {
        "format_version": 2,
        "header": {
            "name": name,
            "description": "github.com/phoenixr-codes/mcstructure",
            "uuid": str(uuid4()),
            "version": [1, 0, 0],
            "min_engine_version": [1, 21, 0],
        },
        "modules": [{"type": "data", "uuid": str(uuid4()), "version": [1, 0, 0]}],
        "metadata": {"product_type": "addon"},
    }
    with TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        with (temp_dir / "manifest.json").open("w") as f:
            json.dump(manifest, f)
        with (temp_dir / "pack_icon.png").open("wb") as f:
            f.write(logo.read_bytes())
        structures_dir = temp_dir / "structures"
        structures_dir.mkdir()
        for structure_path in structures.glob("*.mcstructure"):
            destination = structures_dir / structure_path.name
            destination.write_bytes(structure_path.read_bytes())
            print(f"adding {structure_path}")
        destination = (root / name.replace(".", "_")).with_suffix(".mcpack")
        with zipfile.ZipFile(destination, "w") as archive:
            for source_path in temp_dir.glob("**/*"):
                print(f"archiving {source_path}")
                archive.write(source_path, arcname=source_path.relative_to(temp_dir))
        print(f"bundled add-on at {destination}")


if __name__ == "__main__":
    main()
