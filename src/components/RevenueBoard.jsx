import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import styles from './Panel.module.css'

export default function RevenueBoard({ revenue = {} }) {
  const { daily = [], totalRevenue = 0, totalOrders = 0, totalProfit = 0 } = revenue

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      {/* KPI row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 16 }}>
        {[
          { label: 'Total Revenue', value: `$${totalRevenue.toFixed(2)}`, color: 'var(--green)' },
          { label: 'Total Orders',  value: totalOrders, color: 'var(--yellow)' },
          { label: 'Est. Profit',   value: `$${totalProfit.toFixed(2)}`, color: 'var(--accent)' },
        ].map(({ label, value, color }) => (
          <div key={label} className={styles.panel} style={{ padding: 16, textAlign: 'center' }}>
            <div style={{ fontSize: 12, color: 'var(--text-dim)', marginBottom: 6, textTransform: 'uppercase', letterSpacing: 1 }}>{label}</div>
            <div style={{ fontSize: 28, fontWeight: 700, color }}>{value}</div>
          </div>
        ))}
      </div>

      {/* Revenue chart */}
      <div className={styles.panel} style={{ padding: 16 }}>
        <div style={{ fontSize: 12, color: 'var(--text-dim)', marginBottom: 12, textTransform: 'uppercase', letterSpacing: 1 }}>Daily Revenue</div>
        {daily.length > 0 ? (
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={daily}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="date" tick={{ fill: 'var(--text-dim)', fontSize: 11 }} />
              <YAxis tick={{ fill: 'var(--text-dim)', fontSize: 11 }} />
              <Tooltip
                contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 6 }}
                labelStyle={{ color: 'var(--text)' }}
                itemStyle={{ color: 'var(--green)' }}
              />
              <Line type="monotone" dataKey="revenue" stroke="var(--green)" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className={styles.empty}>Revenue data will appear once products start selling.</div>
        )}
      </div>
    </div>
  )
}
