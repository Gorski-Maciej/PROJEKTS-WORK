import json
from datetime import datetime, timedelta

from jinja2 import Template
from weasyprint import HTML

TEMPLATE_HTML = """
<html><head><title>NetGuardian Raport</title></head><body>
<h1>Raport bezpieczeństwa – {{ period }}</h1>
<p>Całkowita liczba przepływów: {{ total_flows }}</p>
<p>Liczba alertów: {{ alert_count }}</p>
<p>Zablokowane adresy IP: {{ blocked_ips }}</p>
<h2>Top 5 źródłowych IP</h2>
<ul>{% for ip, cnt in top_src %}<li>{{ ip }} – {{ cnt }}</li>{% endfor %}</ul>
<h2>Ostatnie alerty</h2>
<table border="1"><tr><th>Czas</th><th>IP</th><th>Score</th></tr>
{% for alert in recent_alerts %}<tr><td>{{ alert.timestamp }}</td><td>{{ alert.src_ip }}</td><td>{{ alert.score }}</td></tr>{% endfor %}
</table>
</body></html>
"""


async def generate_report(pool, duck_con, redis_client):
    now = datetime.utcnow()
    yesterday = now - timedelta(hours=24)

    async with pool.acquire() as conn:
        total_flows = await conn.fetchval("SELECT COUNT(*) FROM flows WHERE time > $1", yesterday)
        top_src_rows = await conn.fetch(
            """
            SELECT src_ip::text AS src_ip, COUNT(*) AS cnt
            FROM flows
            WHERE time > $1
            GROUP BY src_ip
            ORDER BY cnt DESC
            LIMIT 5
            """,
            yesterday,
        )

    alerts_json = await redis_client.lrange("alerts_list", -10, -1)
    recent_alerts = [json.loads(a) for a in alerts_json]
    blocked_ips = await redis_client.smembers("blocked_ips")

    duck_con.execute(
        """
        CREATE TABLE IF NOT EXISTS flows (
            time TIMESTAMP,
            agent_id TEXT,
            src_ip TEXT,
            dst_ip TEXT,
            src_port INTEGER,
            dst_port INTEGER,
            proto INTEGER,
            flags TEXT,
            length INTEGER
        )
        """
    )
    avg_length = duck_con.execute("SELECT AVG(length) FROM flows WHERE time > ?", (yesterday,)).fetchone()[0]

    html = Template(TEMPLATE_HTML).render(
        period=f"{yesterday} - {now}",
        total_flows=total_flows,
        alert_count=len(alerts_json),
        blocked_ips=", ".join(blocked_ips) if blocked_ips else "brak",
        top_src=[(row["src_ip"], row["cnt"]) for row in top_src_rows],
        recent_alerts=recent_alerts,
        avg_length=avg_length,
    )
    output_path = "/tmp/netguardian_report.pdf"
    HTML(string=html).write_pdf(output_path)
    return output_path
