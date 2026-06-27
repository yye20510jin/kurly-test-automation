from pathlib import Path
from dotenv import load_dotenv

def load_all_env():
    current_dir = Path(__file__).parent
    local_path = current_dir / "config/.env.local"
    if local_path.exists():
        load_dotenv(dotenv_path = local_path)
    
    shared_path = current_dir / "config/.env.shared"
    if shared_path.exists():
        load_dotenv(dotenv_path = shared_path)
    
