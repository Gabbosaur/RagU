import os

def list_files(directory):
    # List all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files


def convert_txt_to_md(txt_file, md_file):
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.readlines()

    # Aggiungi formattazione Markdown se necessario (esempio di titolo)
    formatted_content = []
    for line in content:
        # Aggiungi formattazione come preferisci, qui sto trasformando la prima riga in un titolo
        if content.index(line) == 0:
            formatted_content.append(f"# {line.strip()}\n")
        else:
            formatted_content.append(line)

    # Scrivi il contenuto nel file .md
    with open(md_file, 'w', encoding='utf-8') as f:
        f.writelines(formatted_content)


directory_path = '..\\countries_data\\'
files = list_files(directory_path)

for file in files:
    convert_txt_to_md(directory_path + file, '..\\countries_md\\' + file.replace(".txt", ".md"))
