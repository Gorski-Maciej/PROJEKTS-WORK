import { useEffect, useState } from 'react'
import { acknowledgeIncident, getIncidents } from '../api/client'

export default function Incidents(){
  const [incidents,setIncidents]=useState([])
  const load = ()=> getIncidents().then(setIncidents)
  useEffect(()=>{ load() },[])
  const ack = async (id)=>{ await acknowledgeIncident(id); load() }
  return <div><h1>Incidents</h1><table><thead><tr><th>ID</th><th>Type</th><th>Status</th><th>Severity</th><th>Action</th></tr></thead><tbody>{incidents.map(i=><tr key={i.id}><td>{i.id}</td><td>{i.type}</td><td>{i.status}</td><td>{i.severity}</td><td>{i.status==='open' && <button onClick={()=>ack(i.id)}>Ack</button>}</td></tr>)}</tbody></table></div>
}
