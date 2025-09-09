# Dev Environment Setup

1. Add entries to the `.gitignore` file using [gitignore.io](https://www.gitignore.io/). Add Python, venv, your IDE, and your OS.
2. Commit the `.gitignore` file.
    ```
    git add .gitignore
    git commit -m "Add .gitignore"
    ```

3. Create a new [virtual env](https://docs.python.org/3/library/venv.html) (venv) for your project.
    ```
    cd /path/to/repository
    python3 -m venv .
    ```

    If you run into issues invoking python, please try `python`, `py` for some other command depending on your OS.

4. Activate your venv. Detailed instructions [here](https://docs.python.org/3/library/venv.html#how-venvs-work)

    ```
    source bin/activate
    ```

    You can confirm that the virtual environment is active by checking which python interpreter is being used.
    ```
    which python
    which pip
    ```

5. Add basic packages

    ```
    pip install black mypy jupyterlab plotly numpy
    ```

6. Configure your IDE to use the venv's Python interpreter. (Ctrl+Shift+P/Command+Shift+P > Python: Select Interpreter for VSCode).

7. Install relevant extensions for your IDE (mypy, black)

8. To use Jupyter lab, run 

    ```
    jupyter lab
    ```