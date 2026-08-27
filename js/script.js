/* =====================================================
   RADEC AUTOPARTES — Interacciones frontend
   Solo animación / UX. Sin lógica de formularios,
   sin llamadas a API, sin almacenamiento de datos.
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {
  inicializarMenuMovil();
  inicializarNavAlScroll();
  inicializarScrollSuave();
  inicializarScrollReveal();
  inicializarRippleBotones();
  inicializarVolverArriba();
});

/* ---------- 1. Menú móvil (hamburguesa) ---------- */
function inicializarMenuMovil() {
  const boton = document.getElementById('hamburguesa');
  const menu = document.getElementById('menu-movil');
  if (!boton || !menu) return;

  boton.addEventListener('click', () => {
    const abierto = menu.classList.toggle('activo');
    boton.classList.toggle('activo', abierto);
    boton.setAttribute('aria-expanded', String(abierto));
    boton.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
  });

  // Cierra el menú al elegir un enlace
  menu.querySelectorAll('a').forEach((enlace) => {
    enlace.addEventListener('click', () => {
      menu.classList.remove('activo');
      boton.classList.remove('activo');
      boton.setAttribute('aria-expanded', 'false');
    });
  });
}

/* ---------- 2. Nav que se compacta al hacer scroll ---------- */
function inicializarNavAlScroll() {
  const nav = document.getElementById('nav');
  if (!nav) return;

  let ultimoEstado = false;
  let ticking = false;

  function actualizar() {
    const comprimido = window.scrollY > 24;
    if (comprimido !== ultimoEstado) {
      nav.classList.toggle('nav--compacta', comprimido);
      ultimoEstado = comprimido;
    }
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(actualizar);
      ticking = true;
    }
  }, { passive: true });
}

/* ---------- 3. Scroll suave para enlaces internos ---------- */
function inicializarScrollSuave() {
  document.querySelectorAll('a[href^="#"]').forEach((enlace) => {
    enlace.addEventListener('click', (evento) => {
      const destinoId = enlace.getAttribute('href');
      if (!destinoId || destinoId === '#') return;
      const destino = document.querySelector(destinoId);
      if (!destino) return;

      evento.preventDefault();
      destino.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
}

/* ---------- 4. Scroll Reveal (IntersectionObserver) ---------- */
function inicializarScrollReveal() {
  const elementos = document.querySelectorAll('.revelar');
  if (!elementos.length) return;

  if (!('IntersectionObserver' in window)) {
    elementos.forEach((el) => el.classList.add('visible'));
    return;
  }

  const observador = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((entrada) => {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('visible');
          observador.unobserve(entrada.target);
        }
      });
    },
    { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
  );

  elementos.forEach((el) => observador.observe(el));
}

/* ---------- 5. Efecto ripple en botones ---------- */
function inicializarRippleBotones() {
  document.querySelectorAll('.boton').forEach((boton) => {
    boton.addEventListener('click', function (evento) {
      const rect = boton.getBoundingClientRect();
      const ondulacion = document.createElement('span');
      const tamano = Math.max(rect.width, rect.height);

      ondulacion.className = 'ripple';
      ondulacion.style.width = ondulacion.style.height = `${tamano}px`;
      ondulacion.style.left = `${evento.clientX - rect.left - tamano / 2}px`;
      ondulacion.style.top = `${evento.clientY - rect.top - tamano / 2}px`;

      boton.appendChild(ondulacion);
      ondulacion.addEventListener('animationend', () => ondulacion.remove());
    });
  });
}

/* ---------- 6. Botón "volver arriba" ---------- */
function inicializarVolverArriba() {
  const boton = document.getElementById('volver-arriba');
  if (!boton) return;

  let ticking = false;

  function actualizarVisibilidad() {
    boton.classList.toggle('visible', window.scrollY > 480);
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(actualizarVisibilidad);
      ticking = true;
    }
  }, { passive: true });

  boton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}
