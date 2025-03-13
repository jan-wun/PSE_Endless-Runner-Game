import os
import subprocess
import tiktoken

# GitHub-Repo-URL
GITHUB_REPO_URL = "https://github.com/jan-wun/PSE_Endless-Runner-Game"
LOCAL_REPO_DIR = "../../../Library/Application Support/JetBrains/PyCharm2024.2/scratches/PSE_Endless-Runner-Game"
ADDITIONAL_RELEVANT_FILES = ["requirements.txt", "config.json", "start.bat"]

# GPT-4o Tokenizer laden
encoding = tiktoken.encoding_for_model("gpt-4o")


def clone_repo(repo_url, target_dir):
    """Klonen des GitHub-Repos"""
    if os.path.exists(target_dir):
        print("Repo existiert bereits. Lösche und klone neu...")
        subprocess.run(["rm", "-rf", target_dir])

    subprocess.run(["git", "clone", repo_url, target_dir], check=True)
    print(f"Repo erfolgreich geklont: {target_dir}")


def get_relevant_files(directory):
    """Finde alle relevanten Dateien im Repo"""
    relevant_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") or file in ADDITIONAL_RELEVANT_FILES:
                relevant_files.append(os.path.join(root, file))
    return relevant_files


def count_tokens_in_file(file_path):
    """Token-Anzahl für eine einzelne Datei berechnen"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    return len(encoding.encode(code))


def count_total_tokens(directory):
    """Token-Anzahl für alle relevante Dateien summieren"""
    relevant_files = get_relevant_files(directory)
    total_tokens = 0

    print("\nToken-Anzahl pro Datei:")
    for file in relevant_files:
        tokens = count_tokens_in_file(file)
        total_tokens += tokens
        print(f"{file}: {tokens} Tokens")

    print(f"\nGesamtanzahl an Tokens: {total_tokens}")
    return total_tokens


if __name__ == "__main__":
    clone_repo(GITHUB_REPO_URL, LOCAL_REPO_DIR)
    count_total_tokens(LOCAL_REPO_DIR)