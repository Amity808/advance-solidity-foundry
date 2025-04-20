# report.py
def generate_report(issues, output_file=None):
    if not issues:
        report = "No issues found."
    else:
        report = "\n".join(issues)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report)
    return report