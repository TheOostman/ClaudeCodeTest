import styles from './Panel.module.css'

function formatTime(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  return d.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

export default function EventLog({ events = [] }) {
  return (
    <div className={styles.logWrap}>
      <div className={styles.logHeader}>Event Log</div>
      <div className={styles.logList}>
        {events.length === 0 && (
          <div className={styles.logItem} style={{ color: 'var(--text-dim)', textAlign: 'center', padding: 20 }}>
            No events yet
          </div>
        )}
        {events.map((ev, i) => (
          <div key={i} className={styles.logItem}>
            <span className={styles.logTime}>{formatTime(ev.ts)}</span>
            <span className={styles.logAgent}>[{ev.agent ?? 'system'}]</span>
            {ev.message}
          </div>
        ))}
      </div>
    </div>
  )
}
