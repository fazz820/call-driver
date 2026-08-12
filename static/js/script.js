(function () {
    'use strict';

    /* ============================
       PAGE LOADER
    ============================ */
    function initPageLoader() {
        var loader = document.getElementById('page-loader');
        if (!loader) return;

        window.addEventListener('load', function () {
            var hideLoader = function () {
                loader.classList.add('hidden');
                setTimeout(function () { loader.style.display = 'none'; }, 500);
            };

            if (document.readyState === 'complete') {
                hideLoader();
            } else {
                setTimeout(hideLoader, 300);
            }
        });
    }

    /* ============================
       NAVBAR SCROLL EFFECT
    ============================ */
    function initNavbarScroll() {
        var navbar = document.querySelector('.navbar');
        if (!navbar) return;

        var checkScroll = function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        };

        window.addEventListener('scroll', checkScroll, { passive: true });
        checkScroll();
    }

    /* ============================
       ACTIVE NAV LINK
    ============================ */
    function initActiveNav() {
        var currentPath = window.location.pathname;
        document.querySelectorAll('.navbar .nav-link, footer .nav-link').forEach(function (link) {
            var href = link.getAttribute('href');
            if (href && href !== '#' && currentPath.startsWith(href) && href !== '/') {
                link.classList.add('active');
            } else if (href === '/' && currentPath === '/') {
                link.classList.add('active');
            }
        });
    }

    /* ============================
       ANIMATE ON SCROLL
    ============================ */
    function initAOS() {
        var elements = document.querySelectorAll('[data-aos]');

        if (elements.length === 0) return;

        if ('IntersectionObserver' in window) {
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('aos-animate');
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            });

            elements.forEach(function (el) { observer.observe(el); });
        } else {
            elements.forEach(function (el) { el.classList.add('aos-animate'); });
        }
    }

    /* ============================
       COUNTER ANIMATION
    ============================ */
    function initCounters() {
        var counters = document.querySelectorAll('.stat-number');

        if (counters.length === 0) return;

        var animateCounter = function (el) {
            var text = el.textContent.trim();
            var target = parseFloat(text.replace(/[^0-9.]/g, ''));
            if (isNaN(target)) return;

            var suffix = text.replace(/[0-9.]/g, '').trim();
            var isDecimal = text.indexOf('.') !== -1;
            var duration = 2000;
            var startTime = null;
            var startValue = 0;

            function step(timestamp) {
                if (!startTime) startTime = timestamp;
                var progress = Math.min((timestamp - startTime) / duration, 1);
                var eased = 1 - Math.pow(1 - progress, 3);
                var current = startValue + (target - startValue) * eased;

                if (isDecimal) {
                    el.textContent = current.toFixed(1) + (suffix ? ' ' + suffix : '');
                } else {
                    el.textContent = Math.floor(current) + (suffix ? ' ' + suffix : '');
                }

                if (progress < 1) {
                    requestAnimationFrame(step);
                } else {
                    el.textContent = text;
                }
            }

            requestAnimationFrame(step);
        };

        if ('IntersectionObserver' in window) {
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            counters.forEach(function (el) { observer.observe(el); });
        } else {
            counters.forEach(animateCounter);
        }
    }

    /* ============================
       AUTO-DISMISS ALERTS
    ============================ */
    function initAlerts() {
        document.querySelectorAll('.alert.show:not(.alert-permanent)').forEach(function (alert) {
            setTimeout(function () {
                var bsAlert = bootstrap.Alert.getInstance(alert);
                if (bsAlert) {
                    bsAlert.close();
                }
            }, 5000);
        });
    }

    /* ============================
       BUTTON RIPPLE EFFECT
    ============================ */
    function initRipple() {
        document.querySelectorAll('.btn').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                var ripple = document.createElement('span');
                var rect = btn.getBoundingClientRect();

                ripple.style.cssText =
                    'position:absolute;border-radius:50%;background:rgba(255,255,255,0.3);' +
                    'width:60px;height:60px;margin-top:-30px;margin-left:-30px;' +
                    'left:' + (e.clientX - rect.left) + 'px;' +
                    'top:' + (e.clientY - rect.top) + 'px;' +
                    'transform:scale(0);animation:rippleAnim 0.6s ease-out;pointer-events:none;';

                btn.style.position = 'relative';
                btn.style.overflow = 'hidden';
                btn.appendChild(ripple);

                setTimeout(function () { ripple.remove(); }, 600);
            });
        });
    }

    /* ============================
       ADD RIPPLE KEYFRAME
    ============================ */
    function addRippleStyle() {
        if (document.getElementById('ripple-style')) return;
        var style = document.createElement('style');
        style.id = 'ripple-style';
        style.textContent =
            '@keyframes rippleAnim {to{transform:scale(4);opacity:0}}';
        document.head.appendChild(style);
    }

    /* ============================
       INIT ON DOM READY
    ============================ */
    function domReady(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    domReady(function () {
        initPageLoader();
        initAOS();
        initCounters();
        initAlerts();
        initNavbarScroll();
        initActiveNav();
        addRippleStyle();
        initRipple();
    });

})();
