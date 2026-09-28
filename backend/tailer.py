import asyncio
import os
import logging
from datetime import datetime
from backend.config import settings
from backend.models import LogEntry

logger = logging.getLogger(__name__)

async def tail_log_file(process_callback):
    """
    Tails the log file asynchronously and passes new log entries to the callback.
    """
    log_file = settings.log_file_path
    
    # Ensure directory and file exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    if not os.path.exists(log_file):
        open(log_file, 'a').close()
        
    logger.info(f"Started monitoring log file: {log_file}")
    
    with open(log_file, 'r') as f:
        # Move to EOF
        f.seek(0, os.SEEK_END)
        
        while True:
            line = f.readline()
            if not line:
                await asyncio.sleep(settings.poll_interval)
                continue
            
            line = line.strip()
            if not line:
                continue
                
            try:
                # Support standard Sentinel format: "2026-09-28 12:30:10 INFO Server started"
                parts = line.split(" ", 2)
                if len(parts) >= 3 and len(parts[0]) == 10 and parts[0].count("-") == 2:
                    timestamp_str = f"{parts[0]} {parts[1]}"
                    level_and_msg = parts[2].split(" ", 1)
                    level = level_and_msg[0].upper()
                    message = level_and_msg[1] if len(level_and_msg) > 1 else ""
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                
                # Support NGINX / Apache Combined Log Format: '127.0.0.1 - - [28/Sep/2026:15:30:10 +0000] "GET /api HTTP/1.1" 502 ...'
                elif "[" in line and "]" in line and '"' in line:
                    import re
                    # Extract timestamp between [ ]
                    ts_match = re.search(r'\[(.*?)\]', line)
                    ts_raw = ts_match.group(1).split(" ")[0] if ts_match else ""
                    try:
                        timestamp = datetime.strptime(ts_raw, "%d/%b/%Y:%H:%M:%S")
                    except:
                        timestamp = datetime.now()
                    
                    # Extract HTTP status code after the quoted request
                    status_match = re.search(r'"\s+(\d{3})\s+', line)
                    status_code = int(status_match.group(1)) if status_match else 200
                    
                    if status_code >= 500:
                        level = "ERROR"
                    elif status_code >= 400:
                        level = "WARNING"
                    else:
                        level = "INFO"
                    
                    message = f"[nginx] {line}"
                else:
                    raise ValueError(f"Unknown log format: {line}")
                
                entry = LogEntry(
                    timestamp=timestamp,
                    level=level,
                    message=message
                )
                
                # Call the processor
                await process_callback(entry)
                
            except Exception as e:
                logger.warning(f"Malformed log entry skipped: {line} - Error: {e}")

