import styles from './Panel.module.css'

export default function BoardPanel({ data }) {
  const strategy  = data?.strategy  ?? 'Awaiting first directive…'
  const directive = data?.directive ?? '—'
  const model     = data?.model     ?? 'claude-opus-4-7'

  return (
    <div className={`${styles.panel} ${styles.panelAccent}`}>
      <div className={styles.header}>
        <span className={styles.icon}>🏛️</span>
        <span className={styles.title}>Board of Directors</span>
        <span className={styles.badge} style={{ color: 'var(--accent2)', fontSize: 10 }}>{model}</span>
      </div>
      <div className={styles.body}>
        <div className={styles.row}>
          <span className={styles.label}>Active strategy</span>
          <span className={styles.value}>{strategy}</span>
        </div>
        <div className={styles.row}>
          <span className={styles.label}>Last directive</span>
          <span className={styles.value}>{directive}</span>
        </div>
      </div>
    </div>
  )
}
