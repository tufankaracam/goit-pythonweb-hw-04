import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile
import argparse
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def read_folder(source_folder, output_folder):
    source = AsyncPath(source_folder)
    if not await source.exists():
        logging.error(f"Source folder not found: {source_folder}")
        return

    async for file in source.rglob("*"):
        if await file.is_file():
            await copy_file(file, output_folder)


async def copy_file(file, output_folder):
    ext = file.suffix.lower()
    target_folder = AsyncPath(output_folder) / ext.strip(".")

    await target_folder.mkdir(parents=True, exist_ok=True)
    target_file = target_folder / file.name
    try:
        await copyfile(file, target_file)
        logging.info(f"Copied: {file} -> {target_file}")
    except Exception as e:
        logging.error(f"Copy Error!: {file} -> {target_file}: {e}")


async def main():
    parser = argparse.ArgumentParser(
        description="Arrange files depends on their extensions."
    )
    parser.add_argument("source_folder", type=str, help="Source File Path")
    parser.add_argument("output_folder", type=str, help="Target File Path")
    args = parser.parse_args()

    source_folder = args.source_folder
    output_folder = args.output_folder

    await read_folder(source_folder, output_folder)


if __name__ == "__main__":
    asyncio.run(main())
