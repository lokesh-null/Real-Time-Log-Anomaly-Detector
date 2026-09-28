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
                # Expected format: "2026-09-28 12:30:10 INFO Server started"
                parts = line.split(" ", 2)
                if len(parts) < 3:
                    raise ValueError("Insufficient parts in log line")
                
                timestamp_str = f"{parts[0]} {parts[1]}"
                level_and_msg = parts[2].split(" ", 1)
                level = level_and_msg[0]
                message = level_and_msg[1] if len(level_and_msg) > 1 else ""
                
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                
                entry = LogEntry(
                    timestamp=timestamp,
                    level=level,
                    message=message
                )
                
                # Call the processor
                await process_callback(entry)
                
            except Exception as e:
                logger.warning(f"Malformed log entry skipped: {line} - Error: {e}")
