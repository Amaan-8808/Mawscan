
def generate_report(detected_files):
    print(detected_files)
    with open('malware_report.txt', 'w') as report_file:
        report_file.write("Malicious Files Detected:\n\n")
        for path, row in detected_files:
            if path is None:
                continue
            report_file.write(f"Hash / Rule Path: {path}\n")
            report_file.write(f"Malicious File Path: {row}\n\n")
    print("\nReport generated successfully.\n")