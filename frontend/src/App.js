import React, { useEffect, useMemo, useRef, useState } from 'react';
import './App.css';

const categoryDetails = [
  { name: 'Electronics', icon: '⌁', note: 'For your everyday upgrade', color: 'lavender' },
  { name: 'Footwear', icon: '↗', note: 'Made to move with you', color: 'peach' },
  { name: 'Men', icon: '◌', note: 'The new-season edit', color: 'sage' },
  { name: 'Women', icon: '✳', note: 'Find your point of view', color: 'rose' },
];

const money = (amount) =>
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(Number(amount) || 0);

function readSavedList(key) {
  try {
    const saved = JSON.parse(window.localStorage.getItem(key) || '[]');
    if (!Array.isArray(saved)) return [];
    if (key === 'aero-cart') {
      return saved.filter(
        (item) =>
          Number.isInteger(item?.id) &&
          Number.isInteger(item?.quantity) &&
          item.quantity > 0
      );
    }
    return [...new Set(saved.filter((id) => Number.isInteger(id)))];
  } catch (error) {
    console.warn(`Could not read saved ${key} data.`, error);
    return [];
  }
}

function saveList(key, value) {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.warn(`Could not save ${key} data.`, error);
  }
}

function App() {
  const [products, setProducts] = useState([]);
  const [status, setStatus] = useState('Connecting to store…');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');
  const [maxPrice, setMaxPrice] = useState(1500);
  const [sortBy, setSortBy] = useState('popular');
  const [discountOnly, setDiscountOnly] = useState(false);
  const [wishlistOnly, setWishlistOnly] = useState(false);
  const [cart, setCart] = useState(() => readSavedList('aero-cart'));
  const [wishlist, setWishlist] = useState(() => readSavedList('aero-wishlist'));
  const [cartOpen, setCartOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [toast, setToast] = useState('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const catalogRef = useRef(null);
  const toastTimer = useRef(null);

  useEffect(() => {
    const controller = new AbortController();
    fetch('/api/products', { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`Store request failed (${response.status}).`);
        return response.json();
      })
      .then((data) => {
        const catalog = Array.isArray(data.products) ? data.products : [];
        setProducts(catalog);
        setStatus(data.db_status || 'Store connected');
        setError('');
      })
      .catch((requestError) => {
        if (requestError.name === 'AbortError') return;
        console.error('Product catalog request failed:', requestError);
        setStatus('Store unavailable');
        setError('We couldn’t load the catalog. Check your connection and try again.');
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });

    return () => controller.abort();
  }, []);

  useEffect(() => {
    saveList('aero-cart', cart);
  }, [cart]);

  useEffect(() => {
    saveList('aero-wishlist', wishlist);
  }, [wishlist]);

  useEffect(() => {
    const onKeyDown = (event) => {
      if (event.key === 'Escape') {
        setCartOpen(false);
        setSelectedProduct(null);
        setMobileMenuOpen(false);
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, []);

  useEffect(
    () => () => {
      if (toastTimer.current) window.clearTimeout(toastTimer.current);
    },
    []
  );

  const productById = useMemo(
    () => new Map(products.map((product) => [product.id, product])),
    [products]
  );

  const cartItems = useMemo(
    () =>
      cart
        .map((entry) => {
          const product = productById.get(entry.id);
          return product ? { ...product, quantity: entry.quantity } : null;
        })
        .filter(Boolean),
    [cart, productById]
  );

  const cartCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);
  const subtotal = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const maxCatalogPrice = Math.max(100, ...products.map((product) => Number(product.price) || 0));

  const filteredProducts = useMemo(() => {
    const query = search.trim().toLowerCase();
    const result = products.filter((product) => {
      const matchesSearch =
        !query ||
        [product.name, product.brand, product.category, product.description]
          .filter(Boolean)
          .some((value) => value.toLowerCase().includes(query));
      const matchesCategory = category === 'All' || product.category === category;
      const matchesPrice = Number(product.price) <= maxPrice;
      const discount = parseInt(product.discount, 10) || 0;
      const matchesDiscount = !discountOnly || discount >= 20;
      const matchesWishlist = !wishlistOnly || wishlist.includes(product.id);
      return matchesSearch && matchesCategory && matchesPrice && matchesDiscount && matchesWishlist;
    });

    if (sortBy === 'price-low') result.sort((a, b) => a.price - b.price);
    if (sortBy === 'price-high') result.sort((a, b) => b.price - a.price);
    if (sortBy === 'popular') {
      result.sort(
        (a, b) =>
          (b.reviews_count || 0) * (b.rating || 0) - (a.reviews_count || 0) * (a.rating || 0)
      );
    }
    return result;
  }, [category, discountOnly, maxPrice, products, search, sortBy, wishlist, wishlistOnly]);

  const showToast = (message) => {
    setToast(message);
    if (toastTimer.current) window.clearTimeout(toastTimer.current);
    toastTimer.current = window.setTimeout(() => setToast(''), 2600);
  };

  const scrollToCatalog = () => {
    catalogRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const chooseCategory = (nextCategory) => {
    setCategory(nextCategory);
    setWishlistOnly(false);
    setMobileMenuOpen(false);
    scrollToCatalog();
  };

  const addToCart = (product) => {
    setCart((current) => {
      const existing = current.find((item) => item.id === product.id);
      if (existing) {
        return current.map((item) =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      return [...current, { id: product.id, quantity: 1 }];
    });
    showToast(`${product.name} added to your bag`);
  };

  const changeQuantity = (productId, amount) => {
    setCart((current) =>
      current
        .map((item) =>
          item.id === productId ? { ...item, quantity: item.quantity + amount } : item
        )
        .filter((item) => item.quantity > 0)
    );
  };

  const toggleWishlist = (product) => {
    const saved = wishlist.includes(product.id);
    setWishlist((current) =>
      saved ? current.filter((id) => id !== product.id) : [...current, product.id]
    );
    showToast(saved ? 'Removed from your wishlist' : 'Saved to your wishlist');
  };

  const clearFilters = () => {
    setSearch('');
    setCategory('All');
    setMaxPrice(maxCatalogPrice);
    setDiscountOnly(false);
    setWishlistOnly(false);
    setSortBy('popular');
  };

  const renderProductCard = (product) => {
    const discount = parseInt(product.discount, 10);
    return (
      <article className="product-card" key={product.id}>
        <div className="product-visual">
          {product.badge && <span className="product-badge">{product.badge}</span>}
          <button
            type="button"
            className={`wishlist-button ${wishlist.includes(product.id) ? 'is-saved' : ''}`}
            aria-label={
              wishlist.includes(product.id) ? 'Remove from wishlist' : 'Add to wishlist'
            }
            aria-pressed={wishlist.includes(product.id)}
            onClick={(event) => {
              event.stopPropagation();
              toggleWishlist(product);
            }}
          >
            {wishlist.includes(product.id) ? '♥' : '♡'}
          </button>
          <span className="product-emoji" aria-hidden="true">
            {product.icon || '✦'}
          </span>
          <button
            type="button"
            className="quick-view"
            onClick={(event) => {
              event.stopPropagation();
              setSelectedProduct(product);
            }}
          >
            Quick view
          </button>
        </div>
        <div className="product-info">
          <div className="product-meta">
            <span>{product.brand}</span>
            <span className="rating">
              ★ {Number(product.rating || 0).toFixed(1)}
              <span className="review-count">({product.reviews_count || 0})</span>
            </span>
          </div>
          <button
            type="button"
            className="product-name"
            onClick={() => setSelectedProduct(product)}
          >
            {product.name}
          </button>
          <div className="product-price-row">
            <strong>{money(product.price)}</strong>
            {product.original_price > product.price && (
              <>
                <del>{money(product.original_price)}</del>
                <span className="discount-label">{discount || ''}% off</span>
              </>
            )}
          </div>
          <button type="button" className="add-button" onClick={() => addToCart(product)}>
            <span aria-hidden="true">＋</span> Add to bag
          </button>
        </div>
      </article>
    );
  };

  const renderSection = (eyebrow, title, description, items, linkText) => (
    <section className="product-section" key={title}>
      <div className="section-heading">
        <div>
          <span className="eyebrow">{eyebrow}</span>
          <h2>{title}</h2>
          {description && <p>{description}</p>}
        </div>
        {linkText && (
          <button type="button" className="text-link" onClick={scrollToCatalog}>
            {linkText} <span aria-hidden="true">↗</span>
          </button>
        )}
      </div>
      <div className="product-grid">{items.map((product) => renderProductCard(product))}</div>
    </section>
  );

  const featuredProducts = products.slice(0, 4);
  const trendingProducts = [...products]
    .sort(
      (a, b) =>
        (b.reviews_count || 0) * (b.rating || 0) - (a.reviews_count || 0) * (a.rating || 0)
    )
    .slice(0, 4);
  const bestSellerProducts = [...products]
    .sort((a, b) => (b.reviews_count || 0) - (a.reviews_count || 0))
    .slice(0, 4);
  const hasActiveFilters =
    search || category !== 'All' || maxPrice < maxCatalogPrice || discountOnly || wishlistOnly;

  return (
    <div className="app-shell">
      <div className="announcement">
        <span>Thoughtful finds for everyday life</span>
        <span className="announcement-divider">·</span>
        <span>New finds, thoughtfully selected.</span>
      </div>

      <header className="site-header">
        <div className="header-main">
          <button
            type="button"
            className="mobile-menu-toggle"
            aria-label="Toggle navigation"
            aria-expanded={mobileMenuOpen}
            onClick={() => setMobileMenuOpen((open) => !open)}
          >
            {mobileMenuOpen ? '×' : '☰'}
          </button>
          <button type="button" className="brand" onClick={clearFilters} aria-label="AERO home">
            <span className="brand-symbol">A</span>
            <span className="brand-word">AERO<span>.</span></span>
          </button>
          <div className="search-wrap">
            <span className="search-symbol" aria-hidden="true">⌕</span>
            <input
              type="search"
              aria-label="Search products"
              placeholder="Search products, brands and more"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              onFocus={() => setWishlistOnly(false)}
            />
            {search && (
              <button
                type="button"
                className="clear-search"
                aria-label="Clear search"
                onClick={() => setSearch('')}
              >
                ×
              </button>
            )}
          </div>
          <div className="header-actions">
            <button
              type="button"
              className={`header-action ${wishlistOnly ? 'active' : ''}`}
              onClick={() => {
                setWishlistOnly((current) => !current);
                setCategory('All');
                scrollToCatalog();
              }}
              aria-pressed={wishlistOnly}
            >
              <span className="action-icon" aria-hidden="true">♡</span>
              <span className="action-label">Saved</span>
              <span className="action-count">{wishlist.length}</span>
            </button>
            <button
              type="button"
              className="header-action bag-action"
              onClick={() => setCartOpen(true)}
            >
              <span className="action-icon" aria-hidden="true">⌑</span>
              <span className="action-label">Bag</span>
              <span className="action-count">{cartCount}</span>
            </button>
          </div>
        </div>
        <nav className={`category-nav ${mobileMenuOpen ? 'is-open' : ''}`} aria-label="Categories">
          <button
            type="button"
            className={category === 'All' && !wishlistOnly ? 'selected' : ''}
            onClick={() => chooseCategory('All')}
          >
            Discover
          </button>
          {categoryDetails.map((item) => (
            <button
              type="button"
              key={item.name}
              className={category === item.name ? 'selected' : ''}
              onClick={() => chooseCategory(item.name)}
            >
              {item.name}
            </button>
          ))}
          <button type="button" className={discountOnly ? 'selected' : ''} onClick={() => {
            setDiscountOnly((current) => !current);
            setWishlistOnly(false);
            scrollToCatalog();
          }}>
            Offers
          </button>
          <span className="api-status" title={status}>
            <span className={error ? 'status-dot offline' : 'status-dot'} />
            {error ? 'Store unavailable' : 'Store live'}
          </span>
        </nav>
      </header>

      <main>
        <section className="hero">
          <div className="hero-copy">
            <span className="hero-kicker"><span /> THE AERO EDIT · 01</span>
            <h1>Good things,<br /><em>well chosen.</em></h1>
            <p>A considered collection of things you’ll love to live with. Discover something a little different.</p>
            <div className="hero-actions">
              <button type="button" className="primary-button" onClick={scrollToCatalog}>
                Explore the edit <span aria-hidden="true">↗</span>
              </button>
              <span className="hero-note">New season, new favourites</span>
            </div>
            <div className="hero-proof">
              <span className="proof-stars">★★★★★</span>
              <span>Picked by people with good taste</span>
            </div>
          </div>
          <div className="hero-art" aria-label="Featured collection">
            <div className="hero-orbit orbit-one" />
            <div className="hero-orbit orbit-two" />
            <div className="hero-sun" />
            <div className="hero-product hero-product-main">
              <span className="hero-product-icon">👟</span>
              <span className="hero-product-caption">Move in your own direction</span>
            </div>
            <div className="hero-product hero-product-small">
              <span>✦</span>
            </div>
            <div className="hero-sticker">THE<br />GOOD<br />FIND</div>
            <div className="hero-art-label"><span>01</span> Objects for everyday life</div>
          </div>
          <div className="hero-index">SCROLL TO EXPLORE <span>↓</span></div>
        </section>

        <div className="service-strip">
          <div><span className="service-icon">↗</span><span><strong>Easy, considered shopping</strong><small>Find something worth keeping</small></span></div>
          <div><span className="service-icon">✳</span><span><strong>Made for everyday</strong><small>Thoughtful picks, lasting value</small></span></div>
          <div><span className="service-icon">⌁</span><span><strong>Delivery calculated at checkout</strong><small>Clear options before you place an order</small></span></div>
        </div>

        <section className="category-section content-width">
          <div className="section-heading">
            <div><span className="eyebrow">A PLACE TO BEGIN</span><h2>Shop by mood.</h2></div>
            <span className="category-caption">The good stuff, all in one place.</span>
          </div>
          <div className="category-cards">
            {categoryDetails.map((item, index) => (
              <button
                type="button"
                className={`category-card ${item.color}`}
                key={item.name}
                onClick={() => chooseCategory(item.name)}
              >
                <span className="category-number">0{index + 1}</span>
                <span className="category-icon">{item.icon}</span>
                <span className="category-name">{item.name}</span>
                <span className="category-note">{item.note}</span>
                <span className="category-arrow" aria-hidden="true">↗</span>
              </button>
            ))}
          </div>
        </section>

        {error && (
          <div className="catalog-error content-width" role="alert">
            <span>{error}</span>
            <button type="button" onClick={() => window.location.reload()}>Try again</button>
          </div>
        )}

        {!loading && !error && !hasActiveFilters && (
          <div className="content-width editorial-banner">
            <div className="editorial-copy">
              <span className="eyebrow">A LITTLE SOMETHING EXTRA</span>
              <h2>Everyday favourites.<br /><em>Not everyday prices.</em></h2>
              <p>Find your next can’t-live-without-it, with a little more left in your pocket.</p>
              <button type="button" className="editorial-link" onClick={() => {
                setDiscountOnly(true);
                scrollToCatalog();
              }}>Shop the offers <span>↗</span></button>
            </div>
            <div className="editorial-art"><span>GOOD<br />THINGS<br /><em>INSIDE</em></span><i>✳</i></div>
          </div>
        )}

        <div className="content-width collections">
          {!loading && !error && !hasActiveFilters && (
            <>
              {featuredProducts.length > 0 && (
                renderSection(
                  'HAND-PICKED FOR YOU',
                  'The current edit.',
                  'A few things we think deserve a closer look.',
                  featuredProducts,
                  'View all'
                )
              )}
              {trendingProducts.length > 0 && (
                renderSection('MAKING A LITTLE NOISE', 'Trending now.', '', trendingProducts, 'Explore the collection')
              )}
              {bestSellerProducts.length > 0 && (
                renderSection('THE CROWD-PLEASERS', 'Loved for a reason.', '', bestSellerProducts, 'Shop best sellers')
              )}
            </>
          )}

          <section className="catalog-section" ref={catalogRef} id="catalog">
            <div className="catalog-topline">
              <div>
                <span className="eyebrow">{wishlistOnly ? 'YOUR LITTLE BLACK BOOK' : 'THE WHOLE COLLECTION'}</span>
                <h2>{wishlistOnly ? 'Saved for later.' : search ? `Results for “${search}”` : category === 'All' ? 'Find your thing.' : `${category}, your way.`}</h2>
                <p>{wishlistOnly ? 'All your favourites, in one place.' : 'Good finds, no rabbit holes.'}</p>
              </div>
              <label className="sort-control">
                <span>Sort by</span>
                <select value={sortBy} onChange={(event) => setSortBy(event.target.value)}>
                  <option value="popular">Most popular</option>
                  <option value="price-low">Price: low to high</option>
                  <option value="price-high">Price: high to low</option>
                </select>
              </label>
            </div>

            <div className="catalog-layout">
              <aside className="filter-panel">
                <div className="filter-title-row"><h3>Make it yours</h3><button type="button" onClick={clearFilters}>Reset</button></div>
                <div className="filter-group">
                  <h4>Category</h4>
                  {['All', ...categoryDetails.map((item) => item.name)].map((item) => (
                    <button
                      type="button"
                      key={item}
                      className={`filter-category ${category === item ? 'checked' : ''}`}
                      onClick={() => {
                        setCategory(item);
                        setWishlistOnly(false);
                      }}
                    >
                      <span className="filter-check">{category === item ? '✓' : ''}</span>{item}
                    </button>
                  ))}
                </div>
                <div className="filter-group">
                  <div className="filter-label-row"><h4>Price</h4><span>Up to {money(maxPrice)}</span></div>
                  <input
                    className="price-slider"
                    type="range"
                    min="0"
                    max={maxCatalogPrice}
                    value={Math.min(maxPrice, maxCatalogPrice)}
                    onChange={(event) => setMaxPrice(Number(event.target.value))}
                    aria-label="Maximum price"
                  />
                  <div className="price-range-labels"><span>$0</span><span>{money(maxCatalogPrice)}</span></div>
                </div>
                <div className="filter-group filter-check-group">
                  <label><input type="checkbox" checked={discountOnly} onChange={(event) => {
                    setDiscountOnly(event.target.checked);
                    setWishlistOnly(false);
                  }} /> On offer</label>
                  <label><input type="checkbox" checked={wishlistOnly} onChange={(event) => setWishlistOnly(event.target.checked)} /> My saved items</label>
                </div>
                <div className="filter-help">The catalog API does not provide live stock levels.</div>
              </aside>

              <div className="catalog-results">
                <div className="results-toolbar">
                  <span>{loading ? 'Finding good things…' : `${filteredProducts.length} ${filteredProducts.length === 1 ? 'find' : 'finds'}`}</span>
                  {hasActiveFilters && <button type="button" onClick={clearFilters}>Clear filters <span>×</span></button>}
                </div>
                {loading ? (
                  <div className="loading-state"><span className="loader" /> Curating your collection…</div>
                ) : filteredProducts.length ? (
                  <div className="product-grid catalog-grid">
                    {filteredProducts.map((product) => renderProductCard(product))}
                  </div>
                ) : (
                  <div className="empty-results">
                    <span>⌕</span>
                    <h3>No finds this time.</h3>
                    <p>Try a different search or clear a filter to see more of the collection.</p>
                    <button type="button" className="primary-button" onClick={clearFilters}>Clear filters</button>
                  </div>
                )}
              </div>
            </div>
          </section>
        </div>

        <section className="newsletter">
          <div className="newsletter-mark">A.</div>
          <div><span className="eyebrow">NOTES FROM AERO</span><h2>A good find, now and then.</h2><p>We’re keeping this little corner of the internet thoughtful.</p></div>
          <span className="newsletter-note">No noise. Just good things. <span>✳</span></span>
        </section>
      </main>

      <footer className="site-footer">
        <div className="footer-main">
          <div className="footer-brand">
            <button type="button" className="brand footer-logo" onClick={clearFilters}><span className="brand-symbol">A</span><span className="brand-word">AERO<span>.</span></span></button>
            <p>Good things, well chosen.<br />A little more joy in the everyday.</p>
          </div>
          <div className="footer-column"><h3>Explore</h3>{['Discover', 'Electronics', 'Footwear', 'Men', 'Women'].map((name) => <button key={name} type="button" onClick={() => chooseCategory(name === 'Discover' ? 'All' : name)}>{name}</button>)}</div>
          <div className="footer-column"><h3>Need a hand?</h3><span>Shipping & delivery</span><span>Returns & exchanges</span><span>Get in touch</span></div>
          <div className="footer-column footer-status"><h3>Store status</h3><p><span className={error ? 'status-dot offline' : 'status-dot'} /> {status}</p><small>Powered by the AERO catalog service</small></div>
        </div>
        <div className="footer-bottom"><span>© {new Date().getFullYear()} AERO. Good things, well chosen.</span><span>Thoughtfully found. Happily kept.</span></div>
      </footer>

      {cartOpen && (
        <div className="overlay-layer" onMouseDown={(event) => {
          if (event.target === event.currentTarget) setCartOpen(false);
        }}>
          <aside className="cart-drawer" role="dialog" aria-modal="true" aria-labelledby="cart-title">
            <div className="drawer-header"><div><span className="eyebrow">YOUR GOOD FINDS</span><h2 id="cart-title">Your bag <span>({cartCount})</span></h2></div><button type="button" className="close-button" aria-label="Close bag" onClick={() => setCartOpen(false)}>×</button></div>
            {cartItems.length ? (
              <>
                <div className="cart-list">
                  {cartItems.map((item) => (
                    <div className="cart-item" key={item.id}>
                      <div className="cart-item-visual"><span>{item.icon || '✦'}</span></div>
                      <div className="cart-item-details"><span className="cart-brand">{item.brand}</span><h3>{item.name}</h3><strong>{money(item.price)}</strong>
                        <div className="quantity-control">
                          <button type="button" aria-label={`Decrease ${item.name} quantity`} onClick={() => changeQuantity(item.id, -1)}>−</button>
                          <span>{item.quantity}</span>
                          <button type="button" aria-label={`Increase ${item.name} quantity`} onClick={() => changeQuantity(item.id, 1)}>＋</button>
                          <button type="button" className="remove-item" onClick={() => setCart((current) => current.filter((entry) => entry.id !== item.id))}>Remove</button>
                        </div>
                      </div>
                      <strong className="cart-line-total">{money(item.price * item.quantity)}</strong>
                    </div>
                  ))}
                </div>
                <div className="drawer-summary">
                  <div className="shipping-message">Delivery options and any charges are confirmed at checkout.</div>
                  <div className="summary-row"><span>Subtotal</span><strong>{money(subtotal)}</strong></div>
                  <div className="summary-row"><span>Delivery</span><strong>Calculated at checkout</strong></div>
                  <div className="summary-total"><span>Estimated total</span><strong>{money(subtotal)}</strong></div>
                  <button type="button" className="checkout-button" onClick={() => showToast('Checkout isn’t connected to the current store API yet.')}>Continue to checkout <span>↗</span></button>
                  <p className="checkout-note">Checkout and payment are not available through the current store API.</p>
                </div>
              </>
            ) : (
              <div className="empty-cart"><span>⌑</span><h3>Your bag is taking a breather.</h3><p>When something feels just right, you’ll find it here.</p><button type="button" className="primary-button" onClick={() => { setCartOpen(false); scrollToCatalog(); }}>Find your thing</button></div>
            )}
          </aside>
        </div>
      )}

      {selectedProduct && (
        <div className="overlay-layer modal-layer" onMouseDown={(event) => {
          if (event.target === event.currentTarget) setSelectedProduct(null);
        }}>
          <section className="product-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
            <button type="button" className="close-button modal-close" aria-label="Close product details" onClick={() => setSelectedProduct(null)}>×</button>
            <div className="modal-visual"><span className="modal-emoji">{selectedProduct.icon || '✦'}</span></div>
            <div className="modal-details">
              <span className="eyebrow">{selectedProduct.brand} · {selectedProduct.category}</span>
              <h2 id="modal-title">{selectedProduct.name}</h2>
              <div className="modal-rating"><span>★ {Number(selectedProduct.rating || 0).toFixed(1)}</span> ({selectedProduct.reviews_count || 0} reviews)</div>
              <p>{selectedProduct.description || 'A considered find for your everyday.'}</p>
              <div className="modal-price"><strong>{money(selectedProduct.price)}</strong>{selectedProduct.original_price > selectedProduct.price && <><del>{money(selectedProduct.original_price)}</del><span>{selectedProduct.discount}</span></>}</div>
              {Array.isArray(selectedProduct.sizes) && selectedProduct.sizes.length > 0 && <div className="product-options"><h3>Available options</h3><div>{selectedProduct.sizes.map((option) => <span key={option}>{option}</span>)}</div></div>}
              <div className="stock-note"><span className="status-dot unavailable" /> Live stock levels aren’t provided by the current catalog API.</div>
              <div className="modal-actions"><button type="button" className="add-button" onClick={() => addToCart(selectedProduct)}>＋ Add to bag</button><button type="button" className={`modal-wishlist ${wishlist.includes(selectedProduct.id) ? 'is-saved' : ''}`} onClick={() => toggleWishlist(selectedProduct)} aria-label="Toggle wishlist">{wishlist.includes(selectedProduct.id) ? '♥' : '♡'}</button></div>
            </div>
          </section>
        </div>
      )}

      {toast && <div className="toast-message" role="status">{toast}</div>}
      <div className="sr-only" aria-live="polite">{cartCount} items in bag</div>
    </div>
  );
}

export default App;
