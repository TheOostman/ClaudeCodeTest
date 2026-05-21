import styles from './Panel.module.css'

export default function ProductsBoard({ products = [] }) {
  if (products.length === 0) {
    return <div className={styles.empty}>No products listed yet. Start the agents to create your first Etsy listing.</div>
  }

  return (
    <div className={styles.productsGrid}>
      {products.map((p) => (
        <div key={p.id} className={styles.productCard}>
          <div className={styles.productImg}>
            {p.mockupUrl
              ? <img src={p.mockupUrl} alt={p.title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              : 'No mockup yet'}
          </div>
          <div className={styles.productInfo}>
            <div className={styles.productTitle}>{p.title}</div>
            <div className={styles.productMeta}>
              <span>${p.price ?? '—'}</span>
              <span>{p.sales ?? 0} sold</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
