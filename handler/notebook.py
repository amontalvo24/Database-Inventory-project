from flask import jsonify
import subprocess as sub

class NotebookHandler:
    
    def render_notebook(self, notebook_path):
        # Use Voila to render the notebook within a subprocess
        # Remove --show_tracebacks and this comment when finished
        command = f"voila {notebook_path}"
        sub.Popen(command, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
        return jsonify(f'Dashboard opened in new tab'), 200