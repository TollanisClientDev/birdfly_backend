# app/utils/uid.py
from datetime import datetime

# Map your role_id -> prefix. Edit mapping to match your roles.
ROLE_PREFIX = {
    1: "RBF",  # rider / user
    2: "DBF",  # driver
    3: "ABF",  # admin
}

def make_uid(role_id: int, seq_id: int, pad: int = 4) -> str:
    """
    Generate UID in format: <PREFIX><SEQ_PADDED><MMYY>
    Example: RBF0001 11 25 -> RBF00011125
    - role_id: integer role id from users.role_id
    - seq_id: numeric auto-increment id for the user (db id)
    - pad: zero-pad length for seq (default 4 -> 0001)
    """
    mm_yy = datetime.utcnow().strftime("%m%y")
    seq = str(seq_id).zfill(pad)
    prefix = ROLE_PREFIX.get(role_id, "UBF")
    return f"{prefix}{seq}{mm_yy}"
