# Restarting the Jupyter Notebook after a Reboot

This file contains the exact commands you need to run each time you restart your computer to get back to a working state for the `experiments.ipynb` notebook.

---

## 1️⃣ Open a terminal and go to the project folder
```bash
cd /home/aignishant/Documents/genaiproject/dp/document_portal
```

## 2️⃣ Activate the virtual environment
```bash
source myvenv/bin/activate
```
You should see the prompt change to something like `(myvenv) …$`.

## 3️⃣ (Optional) Clear notebook outputs
If you want to keep the notebook lightweight after adding new large outputs, run:
```bash
jupyter nbconvert --clear-output --inplace notebook/experiments.ipynb
```
*Skip this step if the notebook is already clean.*

## 4️⃣ Launch Jupyter Lab (no browser auto‑open)
```bash
jupyter lab notebook/experiments.ipynb --no-browser --port=8889
```
The terminal will print a URL similar to:
```
http://localhost:8889/lab?token=YOUR_TOKEN_HERE
```
Copy that URL into any web browser on the same machine (or open the `file:///…/jpserver-*.html` shortcut that Jupyter prints). The notebook will open ready for you to edit and run cells.

## 5️⃣ Shut down the server when finished
In the terminal where Jupyter is running, press **Ctrl‑C**, confirm with **y**, and the server will stop cleanly.

---

### One‑click shortcut (optional)
If you prefer a single command, create the following script in the project root:
```bash
# File: run_notebook.sh   (make it executable with chmod +x run_notebook.sh)
#!/usr/bin/env bash
PROJECT_ROOT="/home/aignishant/Documents/genaiproject/dp/document_portal"

cd "$PROJECT_ROOT" || exit 1
source myvenv/bin/activate
# Uncomment the next line if you want to clear outputs each time
# jupyter nbconvert --clear-output --inplace notebook/experiments.ipynb
jupyter lab notebook/experiments.ipynb --no-browser --port=8889
```
Create it with:
```bash
cat > run_notebook.sh <<'EOF'
#!/usr/bin/env bash
PROJECT_ROOT="/home/aignishant/Documents/genaiproject/dp/document_portal"

cd "$PROJECT_ROOT" || exit 1
source myvenv/bin/activate
# Uncomment the next line if you want to clear outputs each time
# jupyter nbconvert --clear-output --inplace notebook/experiments.ipynb
jupyter lab notebook/experiments.ipynb --no-browser --port=8889
EOF
chmod +x run_notebook.sh
```
Now you can simply run:
```bash
./run_notebook.sh
```
---

**TL;DR – one‑liner after a reboot**
```bash
cd /home/aignishant/Documents/genaiproject/dp/document_portal && \
source myvenv/bin/activate && \
jupyter lab notebook/experiments.ipynb --no-browser --port=8889
```

Feel free to edit this file if you want to change the port or add additional steps.
