import { useEffect, useRef } from 'react'

export default function useWebSocket(url, onMessage){
  const wsRef = useRef(null)

  useEffect(()=>{
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}${url}`
    wsRef.current = new WebSocket(wsUrl)
    wsRef.current.onmessage = (event)=>{
      try { onMessage(JSON.parse(event.data)) } catch { onMessage({type:'raw', message:event.data}) }
    }
    return ()=> wsRef.current && wsRef.current.close()
  }, [url, onMessage])

  return wsRef
}
