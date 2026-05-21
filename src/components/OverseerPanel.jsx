import styles from './Panel.module.css'

export default function OverseerPanel({ data }) {
  const status  = data?.status  ?? 'idle'
  const task    = data?.task    ?? '—'
  const queue   = data?.queue   ?? []
  const model   = data?.model   ?? 'claude-sonnet-4-6'

  return (
    <div className={`${styles.panel} ${styles.panelAccent2}`}>
      <div className={styles.header}>
        <span className={styles.icon}>👁️</span>
        <span className={styles.title}>Overseer</span>
        <span className={styles.badge} style={{ color: 'var(--yellow)', fontSize: 10 }}>{model}</span>
      </div>
      <div className={styles.body}>
        <div className={styles.row}>
          <span className={styles.label}>Current task</span>
          <span className={styles.value}>{task}</span>
        </div>
        <div className={styles.row}>
          <span className={styles.label}>Queue</span>
          <span className={styles.value}>
            {queue.length === 0 ? 'Empty' : `${queue.length} pending`}
          </span>
        </div>
        {queue.length > 0 && (
          <ul className={styles.queueList}>
            {queue.slice(0, 4).map((item, i) => (
              <li key={i} className={styles.queueItem}>→ {item}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
