(function () {
  function ready(callback) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', callback, { once: true });
    } else {
      callback();
    }
  }

  var reduceMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add(reduceMotion ? 'motion-reduced' : 'motion-ready');

  var SUPABASE_URL = 'https://jzlkovnrymlwkuvbewkc.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_lORAx-U_P3YiIjiR9ekd6w_Bd2hnP4S';
  var FALLBACKS = {
    phoneDisplay: '(219) 306-0674',
    phoneTel: '+12193060674',
    email: 'info@oxygendx.com',
    addressLine1: '8300 BROADWAY UNIT D2',
    addressLine2: 'MERRILLVILLE, INDIANA 46410',
    operatingHours: 'Mon-Fri: 9:00 AM - 5:00 PM | 24/7 On-Call for Emergencies'
  };

  function safeTrim(value) {
    return String(value || '').trim();
  }

  function normalizeTel(value) {
    return safeTrim(value).replace(/\s+/g, '');
  }

  function replacePhoneInText(text, phoneDisplay) {
    var input = String(text || '');
    var replaced = input.replace(/\+?\d[\d\s().-]{6,}\d/g, phoneDisplay);
    if (replaced !== input) return replaced;
    if (/\bphone\b/i.test(input)) {
      return input.replace(/phone[^:]*:?.*/i, 'Phone: ' + phoneDisplay);
    }
    return phoneDisplay;
  }

  function updateAddressBlocks(addressLine1, addressLine2) {
    var addressHtml = addressLine1 + '<br>' + addressLine2;

    var topAddress = document.querySelector('.top-bar .container > span:first-child');
    if (topAddress) {
      var svg = topAddress.querySelector('svg');
      topAddress.innerHTML = '';
      if (svg) topAddress.appendChild(svg);
      topAddress.appendChild(document.createTextNode(' ' + addressLine1 + ' ' + addressLine2));
    }

    Array.prototype.slice.call(document.querySelectorAll('.footer-contact-item span:last-child'))
      .forEach(function (el) {
        var text = safeTrim(el.textContent).toUpperCase();
        if (text.indexOf('BROADWAY') >= 0 || text.indexOf('MERRILLVILLE') >= 0 || text.indexOf('UNIT') >= 0) {
          el.innerHTML = addressHtml;
        }
      });

    Array.prototype.slice.call(document.querySelectorAll('.ci-label')).forEach(function (label) {
      if (safeTrim(label.textContent).toLowerCase() === 'headquarters') {
        var value = label.parentElement && label.parentElement.querySelector('.ci-value');
        if (value) value.innerHTML = addressHtml;
      }
    });
  }

  function updateOperatingHours(hoursText) {
    Array.prototype.slice.call(document.querySelectorAll('.ci-label')).forEach(function (label) {
      if (safeTrim(label.textContent).toLowerCase() === 'operating hours') {
        var value = label.parentElement && label.parentElement.querySelector('.ci-value');
        if (value) value.innerHTML = hoursText.replace(/\s*\|\s*/g, '<br>');
      }
    });
  }

  function applySiteSettings(settings) {
    var phoneDisplay = safeTrim(settings.phone_display) || FALLBACKS.phoneDisplay;
    var phoneTel = normalizeTel(settings.phone_tel) || FALLBACKS.phoneTel;
    var email = safeTrim(settings.email) || FALLBACKS.email;
    var addressLine1 = safeTrim(settings.address_line1) || FALLBACKS.addressLine1;
    var addressLine2 = safeTrim(settings.address_line2) || FALLBACKS.addressLine2;
    var operatingHours = safeTrim(settings.operating_hours) || FALLBACKS.operatingHours;

    Array.prototype.slice.call(document.querySelectorAll('a[href^="tel:"]')).forEach(function (link) {
      link.setAttribute('href', 'tel:' + phoneTel);
      link.textContent = replacePhoneInText(link.textContent, phoneDisplay);
    });

    Array.prototype.slice.call(document.querySelectorAll('a[href^="mailto:"]')).forEach(function (link) {
      link.setAttribute('href', 'mailto:' + email);
      if (safeTrim(link.textContent).indexOf('@') >= 0 || safeTrim(link.textContent) === '') {
        link.textContent = email;
      }
    });

    updateAddressBlocks(addressLine1, addressLine2);
    updateOperatingHours(operatingHours);
  }

  async function syncSiteSettingsFromBackend() {
    try {
      var params = new URLSearchParams({
        select: 'title,description',
        page: 'eq.site-settings',
        is_published: 'eq.true',
        order: 'sort_order.asc,created_at.asc'
      });
      var response = await timedFetch(SUPABASE_URL + '/rest/v1/services?' + params.toString(), {
        headers: {
          apikey: SUPABASE_KEY,
          Authorization: 'Bearer ' + SUPABASE_KEY
        }
      }, 3200);
      if (!response.ok) return;
      var rows = await response.json();
      if (!Array.isArray(rows) || !rows.length) return;

      var settings = {};
      rows.forEach(function (row) {
        var key = safeTrim(row.title).toLowerCase();
        if (!key || settings[key]) return;
        settings[key] = safeTrim(row.description);
      });
      applySiteSettings(settings);
    } catch (_err) {
      // Keep current page values as fallback.
    }
  }

  function currentPageSlug() {
    var file = (window.location.pathname.split('/').pop() || 'diagnostic.html').toLowerCase();
    if (!file || file === 'index.html') return 'diagnostic';
    return file.replace(/\.html$/, '') || 'diagnostic';
  }

  function applyContentValue(element, value, type) {
    if (!element || !value) return;
    var fieldType = safeTrim(type).toLowerCase();
    if (fieldType === 'image' || element.tagName === 'IMG') {
      element.setAttribute('src', value);
      return;
    }
    if (fieldType === 'background') {
      element.style.backgroundImage = "url('" + value.replace(/'/g, "\\'") + "')";
      return;
    }
    element.textContent = value;
  }

  async function syncPageContentFromBackend() {
    try {
      var pageSlug = currentPageSlug();
      var params = new URLSearchParams({
        select: 'title,description,icon',
        page: 'eq.page-content-' + pageSlug,
        is_published: 'eq.true',
        order: 'sort_order.asc,created_at.asc'
      });
      var response = await timedFetch(SUPABASE_URL + '/rest/v1/services?' + params.toString(), {
        headers: {
          apikey: SUPABASE_KEY,
          Authorization: 'Bearer ' + SUPABASE_KEY
        }
      }, 3200);
      if (!response.ok) return;
      var rows = await response.json();
      if (!Array.isArray(rows) || !rows.length) return;

      rows.forEach(function (row) {
        var key = safeTrim(row.title);
        var value = safeTrim(row.description);
        if (!key || !value) return;
        Array.prototype.slice.call(document.querySelectorAll('[data-cms="' + key + '"]'))
          .forEach(function (element) {
            applyContentValue(element, value, row.icon);
          });
      });
    } catch (_err) {
      // Keep page fallback content.
    }
  }

  function timedFetch(url, options, timeoutMs) {
    if (!window.AbortController) return fetch(url, options);
    var controller = new AbortController();
    var timer = window.setTimeout(function () {
      controller.abort();
    }, timeoutMs || 3000);
    var requestOptions = Object.assign({}, options || {}, { signal: controller.signal });
    return fetch(url, requestOptions).finally(function () {
      window.clearTimeout(timer);
    });
  }

  function runWhenIdle(callback) {
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(callback, { timeout: 1200 });
    } else {
      window.setTimeout(callback, 80);
    }
  }

  function setupReveals() {
    var revealSelector = [
      '.section-header',
      '.service-card',
      '.training-card',
      '.svc-list-item',
      '.product-body > h2',
      '.product-body > h3',
      '.product-body > p',
      '.product-body > ul',
      '.product-body > .drug-info-section',
      '.product-sidebar',
      '.panel-card',
      '.collection-method',
      '.tpa-lead',
      '.tpa-card',
      '.tpa-list li',
      '.price-card',
      '.compliance-note',
      '.contact-grid > div',
      '.contact-info-item',
      '.footer-col',
      '.footer-brand'
    ].join(',');

    var elements = Array.prototype.slice.call(document.querySelectorAll(revealSelector))
      .filter(function (element) {
        return !element.closest('.mobile-menu');
      });

    elements.forEach(function (element, index) {
      element.classList.add('motion-reveal');
      element.style.setProperty('--motion-index', String(index % 8));
    });

    if (!('IntersectionObserver' in window)) {
      elements.forEach(function (element) {
        element.classList.add('is-visible');
      });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      rootMargin: '0px 0px -8% 0px',
      threshold: 0.12
    });

    elements.forEach(function (element) {
      observer.observe(element);
    });
  }

  function setupRipples() {
    var clickableSelector = [
      '.btn-primary',
      '.btn-outline',
      '.cta-btn',
      '.cta-btn-outline',
      '.form-submit',
      '.enroll-btn',
      '.nav-links a',
      '.mobile-menu a'
    ].join(',');

    document.addEventListener('pointerdown', function (event) {
      var target = event.target.closest(clickableSelector);
      if (!target || target.disabled) {
        return;
      }

      var rect = target.getBoundingClientRect();
      var ripple = document.createElement('span');
      ripple.className = 'motion-ripple';
      ripple.style.setProperty('--ripple-x', (event.clientX - rect.left) + 'px');
      ripple.style.setProperty('--ripple-y', (event.clientY - rect.top) + 'px');
      target.appendChild(ripple);

      window.setTimeout(function () {
        ripple.remove();
      }, 700);
    });
  }

  function setupAdminAccessButton() {
    var file = (window.location.pathname.split('/').pop() || '').toLowerCase();
    var path = window.location.pathname.replace(/\/+$/, '').toLowerCase();
    if (['', '/', '/index.html'].indexOf(path) >= 0 || ['index.html', 'admin.html', 'login.html', 'dashboard.html'].indexOf(file) >= 0) return;
    var adminHref = '/admin.html';
    if (document.querySelector('[data-admin-access-link]')) return;

    var style = document.createElement('style');
    style.textContent = [
      '[data-admin-access-link]{font-size:12px!important;opacity:.78}',
      '[data-admin-access-link]:hover{opacity:1}',
      '.staff-login-footer-item{margin-top:8px}',
      '.staff-login-footer-inline{display:inline-flex;margin-left:10px}',
      '.staff-login-footer-block{margin-top:14px;text-align:center}',
      '.staff-login-fixed{position:fixed;left:18px;bottom:18px;z-index:9999;display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border-radius:999px;background:#0f2554;color:#fff!important;font-size:12px!important;font-weight:800;box-shadow:0 10px 28px rgba(15,37,84,.24);opacity:.92;text-decoration:none!important}',
      '.staff-login-fixed:hover{opacity:1;transform:translateY(-1px)}',
      '@media(max-width:640px){.staff-login-fixed{left:12px;bottom:12px;padding:9px 12px;font-size:11px!important}}'
    ].join('');
    document.head.appendChild(style);

    var link = document.createElement('a');
    link.href = adminHref;
    link.textContent = 'Staff Login';
    link.setAttribute('data-admin-access-link', 'true');
    link.setAttribute('aria-label', 'Open staff admin login');

    var fixedLink = link.cloneNode(true);
    fixedLink.className = 'staff-login-fixed';
    fixedLink.textContent = 'Staff Login';
    document.body.appendChild(fixedLink);

    var quickLinks = Array.prototype.slice.call(document.querySelectorAll('.footer-col')).find(function (col) {
      var heading = col.querySelector('h4');
      return heading && safeTrim(heading.textContent).toLowerCase().indexOf('quick') >= 0;
    });
    var quickList = quickLinks && quickLinks.querySelector('ul');
    if (quickList) {
      var item = document.createElement('li');
      item.className = 'staff-login-footer-item';
      item.appendChild(link);
      quickList.appendChild(item);
      return;
    }

    var footerLinks = document.querySelector('.hc-footer .f-links, footer .f-links, footer .footer-links');
    if (footerLinks) {
      if (footerLinks.tagName === 'UL') {
        var listItem = document.createElement('li');
        listItem.className = 'staff-login-footer-item';
        listItem.appendChild(link);
        footerLinks.appendChild(listItem);
      } else {
        link.className = 'staff-login-footer-inline';
        footerLinks.appendChild(link);
      }
      return;
    }

    var gatewayFooter = document.querySelector('.gw-footer');
    if (gatewayFooter) {
      var separator = document.createTextNode(' · ');
      gatewayFooter.appendChild(separator);
      gatewayFooter.appendChild(link);
      return;
    }

    var footer = document.querySelector('footer');
    if (footer) {
      var wrapper = document.createElement('div');
      wrapper.className = 'staff-login-footer-block';
      wrapper.appendChild(link);
      footer.appendChild(wrapper);
    }
  }

  ready(function () {
    setupAdminAccessButton();
    if (!reduceMotion) {
      setupReveals();
      setupRipples();
    }
    runWhenIdle(function () {
      syncSiteSettingsFromBackend();
      syncPageContentFromBackend();
    });
  });
})();
