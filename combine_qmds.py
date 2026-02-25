import os

OUTPUT_FILE = "combined_course_content.qmd"
ROOT_DIR = "."

def should_include_file(root, filename):
    if not filename.endswith(".qmd"):
        return False
    if filename == OUTPUT_FILE:
        return False

    # Check if we are in the Projects folder
    # We check if 'Projects' is the immediate parent directory name
    # or if it's somewhere in the path (though prompt implied "the project folder")
    # Using basename checks the immediate directory.
    if os.path.basename(root) == "Projects":
        if filename == "project_0_dp.qmd":
            return True
        if filename.startswith("unit"):
            return True
        # Skip everything else in Projects (e.g. project_1.qmd, project_0.qmd)
        return False
    
    return True

def main():
    qmd_files_to_process = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Sort to ensure deterministic order
        dirs.sort()
        files.sort()
        
        for file in files:
            if should_include_file(root, file):
                qmd_files_to_process.append(os.path.join(root, file))

    print(f"Found {len(qmd_files_to_process)} files to combine.")

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
            for i, file_path in enumerate(qmd_files_to_process):
                print(f"Processing: {file_path}")
                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        content = infile.read()
                        
                        outfile.write(content)
                        
                        # Add separator if not the last file
                        if i < len(qmd_files_to_process) - 1:
                            outfile.write("\n\n---\n---\n\n")
                            
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    
        print(f"Successfully created {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    main()
