import { useEffect, useState } from 'react'
import { getPredictions, getSummary } from '../api/client'
import useWebSocket from '../hooks/useWebSocket'

export default function Dashboard(){
  const [summary,setSummary]=useState({incidents_open:0,incidents_acknowledged:0,agents_online:0,total_metrics:0})
  const [prediction,setPrediction]=useState({forecast:0,trend:'stable'})
  const [liveMessage,setLiveMessage]=useState('n/a')

  useEffect(()=>{ getSummary().then(setSummary); getPredictions().then(setPrediction) },[])
  useWebSocket('/ws/live', (msg)=> setLiveMessage(msg.type || 'live'))

  return <div><h1>Dashboard</h1><ul><li>Open: {summary.incidents_open}</li><li>Ack: {summary.incidents_acknowledged}</li><li>Agents: {summary.agents_online}</li><li>Metrics: {summary.total_metrics}</li><li>Forecast: {prediction.forecast} ({prediction.trend})</li><li>Live: {liveMessage}</li></ul></div>
}
