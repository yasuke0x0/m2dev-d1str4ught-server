import os
import shutil
import chardet  # pip install chardet

def convert_to_utf8(root_dir, backup=True, recursive=True):
	for dirpath, _, filenames in os.walk(root_dir):
		for filename in filenames:
			file_path = os.path.join(dirpath, filename)

			# Skip already UTF-8 files if possible
			try:
				with open(file_path, 'rb') as f:
					raw = f.read()
					detected = chardet.detect(raw)
					enc = detected['encoding'] or 'utf-8'
			except Exception as e:
				print(f"⚠️ Skipping {file_path} (read error: {e})")
				continue

			if enc.lower() == 'utf-8':
				# Already UTF-8
				continue

			print(f"Converting {file_path} ({enc} → utf-8)")

			try:
				text = raw.decode(enc, errors='replace')

				if backup:
					shutil.copy2(file_path, file_path + ".bak")

				with open(file_path, 'w', encoding='utf-8', newline='') as f:
					f.write(text)
			except Exception as e:
				print(f"❌ Failed to convert {file_path}: {e}")

		if not recursive:
			break

if __name__ == "__main__":
	directory = "."  # current directory
	convert_to_utf8(directory, backup=True, recursive=True)
