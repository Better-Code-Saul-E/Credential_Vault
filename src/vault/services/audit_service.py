import os 
import re
import datetime

class AuditService:
    def __init__(self, data_dir: str):
        self.log_file = os.path.join(data_dir, "audit.log")
    
    def log_event(self, action: str, details: str = ""):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {action.upper()}: {details}\n"

        try:
            with open(self.log_file, "a") as f:
                f.write(entry)
        except Exception as e:
            print(f"Failed to write audit log: {e}")
    
    def get_parsed_logs(self, limit: int = 20) -> list[dict]:
        if not os.path.exists(self.log_file):
            return []
        
        results = []
        try:
            with open(self.log_file, "r") as f:
                lines = f.readlines()
                
            pattern = re.compile(r"\[(.*?)\] (.*?): (.*)")

            for line in lines[-limit:]:
                match = pattern.match(line.strip())
                if match:
                    results.append({
                        "timestamp": match.group(1),
                        "action": match.group(2),
                        "details": match.group(3)
                    })
            return results
        except Exception:
            return []
    