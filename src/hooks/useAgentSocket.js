import { useState, useEffect, useRef, useCallback } from 'react'

const WS_URL = 'ws://localhost:8000/ws'
const MAX_EVENTS = 200

const DEFAULT_AGENTS = {
  board:      { status: 'idle', strategy: null, directive: null, model: 'claude-opus-4-7' },
  overseer:   { status: 'idle', task: null, queue: [], model: 'claude-sonnet-4-6' },
  research:   { status: 'idle', task: null, lastAction: null },
  design:     { status: 'idle', task: null, lastAction: null },
  listing:    { status: 'idle', task: null, lastAction: null },
  marketing:  { status: 'idle', task: null, lastAction: null },
  analytics:  { status: 'idle', task: null, lastAction: null },
  operations: { status: 'idle', task: null, lastAction: null },
}

export function useAgentSocket() {
  const [agents,    setAgents]    = useState(DEFAULT_AGENTS)
  const [events,    setEvents]    = useState([])
  const [products,  setProducts]  = useState([])
  const [revenue,   setRevenue]   = useState({})
  const [connected, setConnected] = useState(false)

  const ws = useRef(null)
  const reconnectTimer = useRef(null)

  const connect = useCallback(() => {
    if (ws.current?.readyState === WebSocket.OPEN) return

    const socket = new WebSocket(WS_URL)
    ws.current = socket

    socket.onopen = () => {
      setConnected(true)
      clearTimeout(reconnectTimer.current)
    }

    socket.onclose = () => {
      setConnected(false)
      reconnectTimer.current = setTimeout(connect, 3000)
    }

    socket.onerror = () => socket.close()

    socket.onmessage = (ev) => {
      let msg
      try { msg = JSON.parse(ev.data) } catch { return }

      switch (msg.type) {
        case 'agent_update':
          setAgents(prev => ({
            ...prev,
            [msg.agent]: { ...prev[msg.agent], ...msg.data },
          }))
          break

        case 'event':
          setEvents(prev => [msg, ...prev].slice(0, MAX_EVENTS))
          break

        case 'products':
          setProducts(msg.data)
          break

        case 'revenue':
          setRevenue(msg.data)
          break

        case 'state':
          // Full state snapshot on connect
          if (msg.agents)   setAgents(a => ({ ...a, ...msg.agents }))
          if (msg.products) setProducts(msg.products)
          if (msg.revenue)  setRevenue(msg.revenue)
          if (msg.events)   setEvents(msg.events)
          break

        default:
          break
      }
    }
  }, [])

  useEffect(() => {
    connect()
    return () => {
      clearTimeout(reconnectTimer.current)
      ws.current?.close()
    }
  }, [connect])

  const sendCommand = useCallback((cmd) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(cmd))
    }
  }, [])

  return { agents, events, products, revenue, connected, sendCommand }
}
