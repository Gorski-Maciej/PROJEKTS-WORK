from statistics import mean


class PredictionService:
    def forecast_incident_pressure(self, incident_history: list[int]) -> dict:
        if not incident_history:
            return {"forecast": 0, "trend": "stable"}
        avg = mean(incident_history[-7:])
        trend = "up" if incident_history and incident_history[-1] > avg else "stable"
        return {"forecast": round(avg, 2), "trend": trend}
