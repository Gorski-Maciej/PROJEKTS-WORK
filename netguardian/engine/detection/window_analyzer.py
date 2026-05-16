import time

import numpy as np
import redis.asyncio as redis

from detection.ml_model import anomaly_model
from response.executor import trigger_alert

FEATURE_WINDOW = 10
THRESHOLD = -0.1


async def get_features_from_redis(redis_client: redis.Redis):
    now = time.time()
    min_time = now - FEATURE_WINDOW
    flows = await redis_client.xrange("flows", min=f"{int(min_time * 1000)}-0", max="+")

    ip_features: dict[str, dict] = {}
    for _, data in flows:
        src = data.get("src_ip", "")
        if not src:
            continue
        if src not in ip_features:
            ip_features[src] = {
                "count": 0,
                "length_sum": 0,
                "unique_dst": set(),
                "syn_count": 0,
                "dst_port_80": 0,
            }

        feats = ip_features[src]
        feats["count"] += 1
        feats["length_sum"] += int(data.get("length", 0))
        feats["unique_dst"].add(data.get("dst_ip"))
        if data.get("flags") == "SYN":
            feats["syn_count"] += 1
        if str(data.get("dst_port")) == "80":
            feats["dst_port_80"] += 1

    features_list = []
    ips = []
    for src, feats in ip_features.items():
        features = [
            feats["count"] / FEATURE_WINDOW,
            feats["length_sum"] / FEATURE_WINDOW,
            len(feats["unique_dst"]) / FEATURE_WINDOW,
            feats["syn_count"] / FEATURE_WINDOW,
            feats["dst_port_80"] / FEATURE_WINDOW,
        ]
        features_list.append(features)
        ips.append(src)

    return ips, np.array(features_list)


async def analyze_window(redis_client: redis.Redis):
    ips, X = await get_features_from_redis(redis_client)
    if len(X) == 0:
        return
    scores = anomaly_model.decision_function(X)
    for index, score in enumerate(scores):
        if score < THRESHOLD:
            await trigger_alert(redis_client, ips[index], float(score), X[index].tolist())
