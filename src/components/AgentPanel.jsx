import styles from './Panel.module.css'

const STATUS_COLOR = {
  idle:    'var(--text-dim)',
  working: 'var(--green)',
  error:   'var(--red)',
  waiting: 'var(--yellow)',
}

const AGENT_LABELS = {
  research:   { icon: '🔍', label: 'Research' },
  design:     { icon: '🎨', label: 'Design' },
  listing:    { icon: '📝', label: 'Listing' },
  marketing:  { icon: '📣', label: 'Marketing' },
  analytics:  { icon: '📊', label: 'Analytics' },
  operations: { icon: '⚙️', label: 'Operations' },
}

export default function AgentPanel({ name, data }) {
  const { icon, label } = AGENT_LABELS[name] ?? { icon: '🤖', label: name }
  const status  = data?.status ?? 'idle'
  const task    = data?.task   ?? '—'
  const lastAct = data?.lastAction ?? '—'

  return (
    <div className={styles.panel}>
      <div className={styles.header}>
        <span className={styles.icon}>{icon}</span>
        <span className={styles.title}>{label} Agent</span>
        <span className={styles.badge} style={{ color: STATUS_COLOR[status] ?? 'var(--text-dim)' }}>
          {status.toUpperCase()}
        </span>
      </div>
      <div className={styles.body}>
        <div className={styles.row}>
          <span className={styles.label}>Task</span>
          <span className={styles.value}>{task}</span>
        </div>
        <div className={styles.row}>
          <span className={styles.label}>Last action</span>
          <span className={styles.value}>{lastAct}</span>
        </div>
      </div>
    </div>
  )
}
