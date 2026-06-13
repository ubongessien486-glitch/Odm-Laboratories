import { supabase } from './supabase.js';

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function resolveServiceLink(service) {
  const raw = String(service.link || '').trim();
  if (raw) return raw;
  return 'booking.html';
}

function serviceCard(service) {
  const title = escapeHtml(service.title || 'Service');
  const description = escapeHtml(service.description || 'Learn more about this service.');
  const price = String(service.price || '').trim();
  const icon = escapeHtml(service.icon || '🔬');
  const href = escapeHtml(resolveServiceLink(service));

  return `
    <div class="service-card">
      <div style="width:56px;height:56px;border-radius:12px;background:rgba(249,168,37,0.15);display:flex;align-items:center;justify-content:center;font-size:26px;margin-bottom:16px;">${icon}</div>
      <h3>${title}</h3>
      <p>${description}${price ? `<br><strong style="color:var(--navy);">${escapeHtml(price)}</strong>` : ''}</p>
      <a href="${href}" class="service-link">View Details <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
    </div>
  `;
}

export async function renderPublicServices(targetId, pages = []) {
  const container = document.getElementById(targetId);
  if (!container) return;

  try {
    let query = supabase.from('services').select('*').eq('is_published', true);
    if (pages.length) query = query.in('page', pages);

    const { data, error } = await query
      .order('sort_order', { ascending: true })
      .order('created_at', { ascending: false });

    if (error || !data || !data.length) return;
    container.innerHTML = data.map(serviceCard).join('');
  } catch {
    // Keep static fallback content on failure.
  }
}

function materialCard(item) {
  const title = escapeHtml(item.title || 'Resource');
  const description = escapeHtml(item.description || item.module || 'Learning resource');
  const moduleName = escapeHtml(item.module || 'General');
  const type = String(item.type || 'link').toLowerCase();
  const icon = type === 'file' ? '📄' : type === 'video' ? '🎥' : '🔗';
  const url = String(item.url || '').trim()
    || (item.file_path ? supabase.storage.from('materials').getPublicUrl(item.file_path).data.publicUrl : '');

  if (!url) return '';

  return `
    <div class="module-card">
      <div class="mod-icon" style="font-size:22px;">${icon}</div>
      <div style="font-size:11px;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;color:var(--gray-500);margin-bottom:8px;">${moduleName}</div>
      <h3>${title}</h3>
      <p>${description}</p>
      <a href="${escapeHtml(url)}" class="mod-link" target="_blank" rel="noopener">Open Resource &rarr;</a>
    </div>
  `;
}

export async function renderMemberMaterials(targetId) {
  const container = document.getElementById(targetId);
  if (!container) return;

  try {
    const { data, error } = await supabase
      .from('materials')
      .select('*')
      .eq('is_published', true)
      .order('sort_order', { ascending: true })
      .order('created_at', { ascending: false });

    if (error || !data || !data.length) return;
    const html = data.map(materialCard).filter(Boolean).join('');
    if (html) container.innerHTML = html;
  } catch {
    // Keep static fallback content on failure.
  }
}

function tpaPricingCard(item) {
  const title = escapeHtml(item.title || 'Plan');
  const price = escapeHtml(item.price || '');
  const description = escapeHtml(item.description || 'Service details available on request.');
  const link = escapeHtml(String(item.link || '').trim() || 'https://app.autobooks.co/pay/oxygen-medical-diagnostic');

  return `
    <a class="price-card" href="${link}" target="_blank" rel="noopener" aria-label="Pay for ${title}">
      <h3>${title}</h3>
      <div class="price">${price}</div>
      <p>${description}</p>
      <span class="payment-action">Pay now</span>
    </a>
  `;
}

export async function renderTpaPricingCards(targetId) {
  const container = document.getElementById(targetId);
  if (!container) return;

  try {
    const { data, error } = await supabase
      .from('services')
      .select('*')
      .eq('page', 'tpa-pricing')
      .eq('is_published', true)
      .order('sort_order', { ascending: true })
      .order('created_at', { ascending: false });

    if (error || !data || !data.length) return;
    container.innerHTML = data.map(tpaPricingCard).join('');
  } catch {
    // Keep static fallback content on failure.
  }
}
