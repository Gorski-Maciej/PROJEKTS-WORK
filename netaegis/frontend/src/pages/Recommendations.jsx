import { useEffect, useState } from 'react'
import { getRecommendations } from '../api/client'

export default function Recommendations(){
  const [items,setItems]=useState([])
  useEffect(()=>{ getRecommendations().then(setItems) },[])
  return <div><h1>Recommendations</h1><ul>{items.map((r,idx)=><li key={idx}>#{r.incident_id} [{r.priority}] {r.recommendation}</li>)}</ul></div>
}
