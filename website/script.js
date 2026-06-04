/* ============================================================
   PriceHarvest — script.js  (v2 — EDA Filtering + Lightbox Nav)
   ============================================================ */

/* ── LOADER ── */
(function () {
  const loader = document.getElementById("loader");
  const fill   = document.getElementById("loaderFill");
  let pct = 0;
  const iv = setInterval(() => {
    pct += Math.random() * 18 + 6;
    if (pct >= 100) { pct = 100; clearInterval(iv); setTimeout(() => loader.classList.add("done"), 300); }
    fill.style.width = pct + "%";
  }, 90);
})();

/* ── CUSTOM CURSOR ── */
(function () {
  const cursor = document.getElementById("cursor");
  const dot    = document.getElementById("cursorDot");
  if (!cursor) return;
  let mx=0, my=0, cx=0, cy=0;
  document.addEventListener("mousemove", e => {
    mx = e.clientX; my = e.clientY;
    dot.style.left = mx+"px"; dot.style.top = my+"px";
  });
  function anim() {
    cx += (mx-cx)*0.12; cy += (my-cy)*0.12;
    cursor.style.left = cx+"px"; cursor.style.top = cy+"px";
    requestAnimationFrame(anim);
  }
  anim();
  document.querySelectorAll("a,button,.vcard,.feat-btn,.crop-tile,.ins-card").forEach(el => {
    el.addEventListener("mouseenter", () => cursor.classList.add("active"));
    el.addEventListener("mouseleave", () => cursor.classList.remove("active"));
  });
})();

/* ── NAVBAR ── */
(function () {
  const nav   = document.getElementById("navbar");
  const ham   = document.getElementById("hamburger");
  const links = document.getElementById("navLinks");
  window.addEventListener("scroll", () => nav.classList.toggle("scrolled", window.scrollY > 50));
  ham.addEventListener("click", () => { ham.classList.toggle("open"); links.classList.toggle("open"); });
  links.querySelectorAll("a").forEach(a => a.addEventListener("click", () => { ham.classList.remove("open"); links.classList.remove("open"); }));
})();

/* ── HERO CANVAS PARTICLES ── */
(function () {
  const canvas = document.getElementById("heroCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  let W, H, particles = [];
  function resize() { W = canvas.width = canvas.offsetWidth; H = canvas.height = canvas.offsetHeight; }
  resize();
  window.addEventListener("resize", resize);
  class Particle {
    constructor() { this.reset(); }
    reset() { this.x=Math.random()*W; this.y=Math.random()*H; this.r=Math.random()*1.5+0.3; this.a=Math.random()*Math.PI*2; this.sp=Math.random()*0.25+0.05; this.op=Math.random()*0.35+0.05; }
    update() { this.y-=this.sp; this.x+=Math.sin(this.a+Date.now()*0.0003)*0.3; if(this.y<-10){this.y=H+10;this.x=Math.random()*W;} }
    draw()   { ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2); ctx.fillStyle=`rgba(201,146,42,${this.op})`; ctx.fill(); }
  }
  for(let i=0;i<80;i++) particles.push(new Particle());
  function drawLines() {
    for(let i=0;i<6;i++){
      const x=(W/6)*i-W*0.1;
      const g=ctx.createLinearGradient(x,0,x+W*0.3,H);
      g.addColorStop(0,"rgba(26,71,49,0)"); g.addColorStop(0.5,"rgba(39,98,73,0.04)"); g.addColorStop(1,"rgba(26,71,49,0)");
      ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x+W*0.3,H);
      ctx.strokeStyle=g; ctx.lineWidth=40; ctx.stroke();
    }
  }
  function loop() { ctx.clearRect(0,0,W,H); drawLines(); particles.forEach(p=>{p.update();p.draw();}); requestAnimationFrame(loop); }
  loop();
})();

/* ── COUNTER ── */
(function () {
  const nums = document.querySelectorAll(".hstat-n[data-target]");
  let done = false;
  function easeOut(t) { return 1-Math.pow(1-t,4); }
  function count(el, target, dur) {
    const s = performance.now();
    function step(now) { const p=Math.min((now-s)/dur,1); el.textContent=Math.round(easeOut(p)*target).toLocaleString(); if(p<1)requestAnimationFrame(step); }
    requestAnimationFrame(step);
  }
  new IntersectionObserver(entries => {
    entries.forEach(e => { if(e.isIntersecting && !done){ done=true; nums.forEach(el=>count(el,+el.dataset.target,el.dataset.target>1000?2000:1200)); }});
  }, { threshold:0.5 }).observe(document.getElementById("hero"));
})();

/* ── SCROLL REVEAL ── */
(function () {
  const els = document.querySelectorAll(".reveal-up, .reveal-fade");
  if (!els.length) return;
  new IntersectionObserver((entries) => {
    entries.forEach(e => { if(e.isIntersecting){ e.target.classList.add("in-view"); } });
  }, { threshold:0.1, rootMargin:"0px 0px -40px 0px" }).observe.bind(
    new IntersectionObserver((entries) => {
      entries.forEach(e => { if(e.isIntersecting){ e.target.classList.add("in-view"); } });
    }, { threshold:0.1, rootMargin:"0px 0px -40px 0px" })
  );
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if(e.isIntersecting){ e.target.classList.add("in-view"); obs.unobserve(e.target); } });
  }, { threshold:0.1, rootMargin:"0px 0px -40px 0px" });
  els.forEach(el => obs.observe(el));
})();

/* ── FEATURE BUTTONS ── */
(function () {
  document.querySelectorAll(".feat-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".feat-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      document.querySelectorAll(".feat-pane").forEach(p => p.classList.remove("active"));
      const pane = document.getElementById("pane-"+btn.dataset.target);
      if (pane) pane.classList.add("active");
    });
  });
})();

/* ── EDA FILTERING ── */
(function () {
  const filters  = document.querySelectorAll(".eda-filter");
  const cards    = document.querySelectorAll(".vcard[data-cat]");
  const countEl  = document.getElementById("chartCount");
  const emptyEl  = document.getElementById("edaEmpty");
  const grid     = document.getElementById("vizGrid");

  filters.forEach(f => {
    f.addEventListener("click", () => {
      filters.forEach(x => x.classList.remove("active"));
      f.classList.add("active");
      const cat = f.dataset.cat;
      let visible = 0;
      cards.forEach(card => {
        const match = cat === "all" || card.dataset.cat === cat;
        card.classList.toggle("hidden", !match);
        if (match) visible++;
      });
      if (countEl) countEl.textContent = visible;
      if (emptyEl) emptyEl.style.display = visible === 0 ? "block" : "none";
      // Span2 only works in grid view
      if (cat !== "all") {
        cards.forEach(card => { if (!card.classList.contains("hidden")) card.classList.remove("span2"); });
      } else {
        // Restore original span2 (re-read from HTML is complicated — just reload classes)
        document.querySelectorAll(".vcard[data-cat]").forEach((card, i) => {
          if ([0, 6, 7].includes(i)) card.classList.add("span2");
        });
      }
    });
  });
})();

/* ── VIEW TOGGLE (Grid / List) ── */
(function () {
  const btnGrid = document.getElementById("viewGrid");
  const btnList = document.getElementById("viewList");
  const grid    = document.getElementById("vizGrid");
  if (!btnGrid || !btnList || !grid) return;
  btnGrid.addEventListener("click", () => {
    btnGrid.classList.add("active"); btnList.classList.remove("active");
    grid.classList.remove("list-view");
    // Re-apply span2 for grid view
    document.querySelectorAll(".vcard[data-cat]").forEach((card, i) => {
      if ([0, 6, 7].includes(i)) card.classList.add("span2");
    });
  });
  btnList.addEventListener("click", () => {
    btnList.classList.add("active"); btnGrid.classList.remove("active");
    grid.classList.add("list-view");
    document.querySelectorAll(".vcard").forEach(c => c.classList.remove("span2"));
  });
})();

/* ── LIGHTBOX WITH PREV / NEXT ── */
(function () {
  const lightbox   = document.getElementById("lightbox");
  const lbImg      = document.getElementById("lbImg");
  const lbCaption  = document.getElementById("lbCaption");
  const lbClose    = document.getElementById("lbClose");
  const lbBackdrop = document.getElementById("lbBackdrop");
  const lbPrev     = document.getElementById("lbPrev");
  const lbNext     = document.getElementById("lbNext");
  if (!lightbox) return;

  let currentIndex = 0;
  let visibleCards = [];

  function getVisibleCards() {
    return Array.from(document.querySelectorAll(".vcard[data-cat]:not(.hidden)"));
  }

  function open(idx) {
    visibleCards = getVisibleCards();
    currentIndex = idx;
    const card = visibleCards[currentIndex];
    if (!card) return;
    const img  = card.querySelector(".vcard-img img");
    const h4   = card.querySelector(".vcard-foot h4");
    lbImg.src  = img ? img.src : "";
    lbImg.alt  = img ? img.alt : "";
    if (lbCaption) lbCaption.textContent = h4 ? h4.textContent : "";
    lightbox.classList.add("open");
    document.body.style.overflow = "hidden";
    updateNav();
  }

  function close() {
    lightbox.classList.remove("open");
    document.body.style.overflow = "";
  }

  function updateNav() {
    if (lbPrev) lbPrev.style.opacity = currentIndex === 0 ? "0.3" : "1";
    if (lbNext) lbNext.style.opacity = currentIndex === visibleCards.length-1 ? "0.3" : "1";
  }

  document.querySelectorAll(".vcard-img").forEach((imgWrap, i) => {
    imgWrap.addEventListener("click", () => {
      const all = Array.from(document.querySelectorAll(".vcard[data-cat]:not(.hidden)"));
      const parent = imgWrap.closest(".vcard");
      const idx = all.indexOf(parent);
      open(idx >= 0 ? idx : 0);
    });
  });

  lbClose.addEventListener("click", close);
  lbBackdrop.addEventListener("click", close);
  lbPrev.addEventListener("click", () => { if(currentIndex>0){currentIndex--;open(currentIndex);} });
  lbNext.addEventListener("click", () => { if(currentIndex<visibleCards.length-1){currentIndex++;open(currentIndex);} });

  document.addEventListener("keydown", e => {
    if (!lightbox.classList.contains("open")) return;
    if (e.key === "Escape")    close();
    if (e.key === "ArrowLeft"  && currentIndex>0)                     { currentIndex--; open(currentIndex); }
    if (e.key === "ArrowRight" && currentIndex<visibleCards.length-1) { currentIndex++; open(currentIndex); }
  });
})();

/* ── MAGNETIC BUTTONS ── */
(function () {
  document.querySelectorAll(".magnetic").forEach(el => {
    el.addEventListener("mousemove", e => {
      const r = el.getBoundingClientRect();
      const dx = e.clientX - r.left - r.width/2;
      const dy = e.clientY - r.top  - r.height/2;
      el.style.transform = `translate(${dx*0.18}px,${dy*0.18}px)`;
    });
    el.addEventListener("mouseleave", () => { el.style.transform = ""; });
  });
})();

/* ── SMOOTH ANCHOR SCROLL ── */
(function () {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener("click", e => {
      const id = a.getAttribute("href").slice(1);
      const t  = document.getElementById(id);
      if (!t) return;
      e.preventDefault();
      window.scrollTo({ top: t.getBoundingClientRect().top + window.scrollY - 80, behavior:"smooth" });
    });
  });
})();

/* ── CARD TILT ── */
(function () {
  document.querySelectorAll(".ins-card").forEach(card => {
    card.addEventListener("mousemove", e => {
      const r = card.getBoundingClientRect();
      const x = (e.clientX-r.left)/r.width-0.5;
      const y = (e.clientY-r.top)/r.height-0.5;
      card.style.transform = `perspective(800px) rotateX(${-y*6}deg) rotateY(${x*6}deg) translateY(-5px)`;
    });
    card.addEventListener("mouseleave", () => { card.style.transform = ""; });
  });
})();

/* ── CROP BAR ANIMATION ── */
(function () {
  const bars = document.querySelectorAll(".ct-bar-fill");
  const obs  = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.style.transition="width 1.4s cubic-bezier(0.22,1,0.36,1)"; obs.unobserve(e.target); } });
  }, { threshold:0.4 });
  bars.forEach(b => {
    const w = b.style.width; b.style.width="0%"; obs.observe(b);
    setTimeout(() => { b.style.width=w; }, 100);
  });
})();

/* ── CUSTOM LANGUAGE SWITCHER ── */
(function () {
  const switcher  = document.getElementById("langSwitcher");
  const btn       = document.getElementById("langBtn");
  const dropdown  = document.getElementById("langDropdown");
  const currentEl = document.getElementById("langCurrent");
  if (!switcher || !btn || !dropdown) return;

  /* Toggle open/close */
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    switcher.classList.toggle("open");
  });

  /* Close when clicking outside */
  document.addEventListener("click", (e) => {
    if (!switcher.contains(e.target)) {
      switcher.classList.remove("open");
    }
  });

  /* On load: read googtrans cookie and highlight the active language */
  (function () {
    const match = document.cookie.match(/googtrans=\/en\/([a-z]+)/);
    if (match) {
      const activeLang = match[1];
      dropdown.querySelectorAll(".lang-opt").forEach(o => {
        o.classList.toggle("active", o.dataset.lang === activeLang);
        if (o.dataset.lang === activeLang) currentEl.textContent = o.dataset.label;
      });
    }
  })();

  /* Helper: write googtrans cookie on both path and domain variants */
  function setGoogCookie(value) {
    const host = location.hostname;
    document.cookie = "googtrans=" + value + "; path=/;";
    document.cookie = "googtrans=" + value + "; path=/; domain=" + host + ";";
    const bare = host.replace(/^www\./, "");
    if (bare !== host) {
      document.cookie = "googtrans=" + value + "; path=/; domain=." + bare + ";";
    }
  }

  /* Select a language */
  dropdown.querySelectorAll(".lang-opt").forEach(opt => {
    opt.addEventListener("click", () => {
      const lang  = opt.dataset.lang;
      const label = opt.dataset.label;

      /* Update UI immediately so user sees feedback before reload */
      dropdown.querySelectorAll(".lang-opt").forEach(o => o.classList.remove("active"));
      opt.classList.add("active");
      currentEl.textContent = label;
      switcher.classList.remove("open");

      if (lang === "en") {
        /* Clear the cookie to restore English, then reload */
        setGoogCookie("");
        document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=" + location.hostname + ";";
      } else {
        /* Set /en/<lang> — this is exactly the cookie Google Translate reads on init */
        setGoogCookie("/en/" + lang);
      }

      /* Reload so Google Translate picks up the new cookie on page init */
      location.reload();
    });
  });

  /* Sync chatbot dropdown on page load based on current language */
  (function() {
    var cookieMatch = document.cookie.match(/googtrans=\/en\/([a-z]+)/);
    var activeLang = cookieMatch ? cookieMatch[1] : "en";
    var chatLangMap = { "en": "English", "hi": "Hindi", "mr": "Marathi" };
    var chatSelect = document.getElementById("ph-language-select");
    if (chatSelect && chatLangMap[activeLang]) chatSelect.value = chatLangMap[activeLang];
    var initMsgMap = { "hi": "नमस्ते! मैं PriceHarvest AI हूँ 🌾", "mr": "नमस्कार! मी PriceHarvest AI आहे 🌾" };
    var initMsg = document.getElementById("ph-initial-msg");
    if (initMsg && initMsgMap[activeLang]) initMsg.textContent = initMsgMap[activeLang];
  })();
})();/* ── BI DASHBOARD CAROUSEL (FULLY FIXED, NO OPTIONAL CHAINING) ── */
(function() {
    var track = document.getElementById("biTrack");
    if (!track) return;
    var slides = Array.from(track.querySelectorAll(".bi-slide"));
    if (!slides.length) return;

    var dotsWrap = document.getElementById("biDots");
    var thumbsWrap = document.getElementById("biThumbs");
    var prevBtn = document.querySelector(".bi-prev");
    var nextBtn = document.querySelector(".bi-next");

    var current = 0;
    var autoTimer = null;

    // Build dots
    if (dotsWrap) {
        for (var i = 0; i < slides.length; i++) {
            var dot = document.createElement("button");
            dot.className = "bi-dot" + (i === 0 ? " active" : "");
            dot.setAttribute("aria-label", "Slide " + (i + 1));
            dot.addEventListener("click", (function(idx) { return function() { goTo(idx); }; })(i));
            dotsWrap.appendChild(dot);
        }
    }

    // Build thumbnails
    if (thumbsWrap) {
        for (var i = 0; i < slides.length; i++) {
            var slideImg = slides[i].querySelector(".bi-img");
            var wrapDiv = document.createElement("div");
            wrapDiv.className = "bi-thumb" + (i === 0 ? " active" : "");
            var thumbImg = document.createElement("img");
            thumbImg.src = slideImg ? (slideImg.src || "") : "";
            thumbImg.alt = slideImg ? (slideImg.alt || "") : "";
            wrapDiv.appendChild(thumbImg);
            wrapDiv.addEventListener("click", (function(idx) { return function() { goTo(idx); }; })(i));
            thumbsWrap.appendChild(wrapDiv);
        }
    }

    function goTo(n) {
        current = (n + slides.length) % slides.length;
        track.style.transform = "translateX(-" + (current * 100) + "%)";
        if (dotsWrap) {
            var dots = dotsWrap.querySelectorAll(".bi-dot");
            for (var i = 0; i < dots.length; i++) {
                dots[i].classList.toggle("active", i === current);
            }
        }
        if (thumbsWrap) {
            var thumbs = thumbsWrap.querySelectorAll(".bi-thumb");
            for (var i = 0; i < thumbs.length; i++) {
                thumbs[i].classList.toggle("active", i === current);
            }
        }
        resetAuto();
    }

    function next() { goTo(current + 1); }

    function prev() { goTo(current - 1); }
    if (prevBtn) prevBtn.addEventListener("click", prev);
    if (nextBtn) nextBtn.addEventListener("click", next);

    function startAuto() {
        if (autoTimer) clearInterval(autoTimer);
        autoTimer = setInterval(next, 5000);
    }

    function resetAuto() {
        if (autoTimer) clearInterval(autoTimer);
        startAuto();
    }
    startAuto();

    // ----- BI Lightbox (IDs exactly as in your HTML) -----
    var lb = document.getElementById("biLightbox");
    var lbOverlay = document.getElementById("biLbOverlay");
    var lbCloseBi = document.getElementById("biLbClose");
    var lbPrev = document.getElementById("biLbPrev");
    var lbNext = document.getElementById("biLbNext");
    var lbImg = document.getElementById("biLbImg");
    var lbCaptionBi = document.getElementById("biLbCaption");

    if (lb) {
        var slideData = [];
        for (var i = 0; i < slides.length; i++) {
            var imgEl = slides[i].querySelector(".bi-img");
            var capEl = slides[i].querySelector(".bi-caption");
            slideData.push({
                src: imgEl ? (imgEl.src || "") : "",
                alt: imgEl ? (imgEl.alt || "") : "",
                caption: capEl ? (capEl.textContent || "").trim() : ""
            });
        }
        var lbCurrent = 0;

        function showLbSlide(i) {
            lbCurrent = (i + slideData.length) % slideData.length;
            if (lbImg) {
                lbImg.src = slideData[lbCurrent].src;
                lbImg.alt = slideData[lbCurrent].alt;
            }
            if (lbCaptionBi) lbCaptionBi.textContent = slideData[lbCurrent].caption;
        }

        function openLb(index) {
            showLbSlide(index);
            if (lb) lb.classList.add("open");
            if (lbOverlay) lbOverlay.classList.add("open");
            document.body.style.overflow = "hidden";
        }

        function closeLb() {
            if (lb) lb.classList.remove("open");
            if (lbOverlay) lbOverlay.classList.remove("open");
            document.body.style.overflow = "";
        }

        for (var i = 0; i < slides.length; i++) {
            var imgInSlide = slides[i].querySelector(".bi-img");
            if (imgInSlide) {
                imgInSlide.addEventListener("click", (function(idx) { return function() { openLb(idx); }; })(i));
            }
        }

        if (lbCloseBi) lbCloseBi.addEventListener("click", closeLb);
        if (lbOverlay) lbOverlay.addEventListener("click", closeLb);
        if (lbPrev) lbPrev.addEventListener("click", function() { showLbSlide(lbCurrent - 1); });
        if (lbNext) lbNext.addEventListener("click", function() { showLbSlide(lbCurrent + 1); });

        document.addEventListener("keydown", function(e) {
            if (!lb || !lb.classList.contains("open")) return;
            if (e.key === "Escape") closeLb();
            if (e.key === "ArrowLeft") showLbSlide(lbCurrent - 1);
            if (e.key === "ArrowRight") showLbSlide(lbCurrent + 1);
        });
    }
})();



