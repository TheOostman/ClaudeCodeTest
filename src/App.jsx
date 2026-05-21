import { useState } from 'react'
import { useAgentSocket } from './hooks/useAgentSocket'
import BoardPanel from './components/BoardPanel'
import OverseerPanel from './components/OverseerPanel'
import AgentPanel from './components/AgentPanel'
import ProductsBoard from './components/ProductsBoard'
import RevenueBoard from './components/RevenueBoard'
import EventLog from './components/EventLog'
import styles from './App.module.css'

const WORKER_AGENTS = ['research', 'design', 'listing', 'marketing', 'analytics', 'operations']

export default function App() {
  const { agents, events, products, revenue, connected, sendCommand } = useAgentSocket()
  const [activeTab, setActiveTab] = useState('agents')

  return (
    <div className={styles.shell}>
      {/* Top bar */}
      <header className={styles.topbar}>
        <span className={styles.logo}>AGENT CONTROL ROOM</span>
        <nav className={styles.tabs}>
          {['agents', 'products', 'revenue'].map(tab => (
            <button
              key={tab}
              className={`${styles.tab} ${activeTab === tab ? styles.tabActive : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab.toUpperCase()}
            </button>
          ))}
        </nav>
        <div className={styles.statusBar}>
          <span className={`${styles.dot} ${connected ? styles.dotGreen : styles.dotRed}`} />
          {connected ? 'Backend connected' : 'Connecting…'}
          <button
            className={styles.startBtn}
            onClick={() => sendCommand({ type: 'start' })}
            disabled={!connected}
          >
            ▶ START
          </button>
          <button
            className={styles.stopBtn}
            onClick={() => sendCommand({ type: 'stop' })}
            disabled={!connected}
          >
            ■ STOP
          </button>
        </div>
      </header>

      {/* Main content */}
      <main className={styles.main}>
        {activeTab === 'agents' && (
          <div className={styles.agentsLayout}>
            <div className={styles.topAgents}>
              <BoardPanel data={agents.board} />
              <OverseerPanel data={agents.overseer} />
            </div>
            <div className={styles.workerGrid}>
              {WORKER_AGENTS.map(name => (
                <AgentPanel key={name} name={name} data={agents[name]} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'products' && <ProductsBoard products={products} />}
        {activeTab === 'revenue' && <RevenueBoard revenue={revenue} />}
      </main>

      {/* Event log sidebar */}
      <aside className={styles.sidebar}>
        <EventLog events={events} />
      </aside>
    </div>
  )
}
