
import mariadb

try:
    conn = mariadb.connect(
        user="jabiott",
        password="lB2]uMIasP",
        host="jabi.us",
        port=3307,
        database="jabiott"
    )
    cur = conn.cursor()
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
cur.execute("INSERT INTO online (ip,url,account,platform) VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE url = ?", ("220.85.206.108", "aaa", "bbb", "ccc", "ddd"))
conn.commit()
# Get Cursor