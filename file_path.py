import os, sys

p = os.path.abspath('C://Users//rlaru//Desktop//2024//llm_study//github2//real-estate-agent//app')
p2 = os.path.abspath('C://Users//rlaru//Desktop//2024//llm_study//github2//real-estate-agent//bot')

sys.path.insert(1,p)
sys.path.insert(2,p)

# %%
from pathlib import Path
f = Path('./app') / "tools"
f.exists()