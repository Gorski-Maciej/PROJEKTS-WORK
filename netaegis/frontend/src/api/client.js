export async function getSummary(){
  const r = await fetch('/api/dashboard/summary')
  return r.json()
}

export async function getIncidents(){
  const r = await fetch('/api/incidents/')
  return r.json()
}

export async function acknowledgeIncident(id){
  const r = await fetch(`/api/incidents/${id}/acknowledge`, {method:'POST'})
  return r.json()
}

export async function getRecommendations(){
  const r = await fetch('/api/recommendations/')
  return r.json()
}

export async function getPredictions(){
  const r = await fetch('/api/predictions/incidents')
  return r.json()
}
