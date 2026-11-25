/* =====================================================
   PARTZONE — scripts.js
   Interacciones de diseño (vanilla JS) y validación de formularios.
   El registro e inicio de sesión se envían a las rutas de Flask.
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {
  inicializarMenuMovil();
  inicializarNavAlScroll();
  inicializarScrollSuave();
  inicializarScrollReveal();
  inicializarRippleBotones();
  inicializarVolverArriba();
  inicializarAlternarClave();
  inicializarValidacionFormularios();
  inicializarBusquedaCatalogo();
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

/* ---------- 5. Efecto ripple en botones propios (.boton) ---------- */
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

/* ---------- 7. Mostrar / ocultar contraseña en los modales ---------- */
function inicializarAlternarClave() {
  document.querySelectorAll('.alternar-clave').forEach((boton) => {
    boton.addEventListener('click', () => {
      const idObjetivo = boton.getAttribute('data-objetivo');
      const campo = document.getElementById(idObjetivo);
      if (!campo) return;

      const icono = boton.querySelector('i');
      const visible = campo.type === 'text';

      campo.type = visible ? 'password' : 'text';
      icono.classList.toggle('fa-eye', visible);
      icono.classList.toggle('fa-eye-slash', !visible);
      boton.setAttribute('aria-label', visible ? 'Mostrar contraseña' : 'Ocultar contraseña');
    });
  });
}

/* ---------- 8. Validación de los formularios de sesión / registro ----------
   Valida en el cliente (patrón "needs-validation" de Bootstrap).
   Login y registro: si el formulario es válido, se envía a Flask. */
function inicializarValidacionFormularios() {
  const formularioLogin = document.getElementById('formularioLogin');
  const formularioRegistro = document.getElementById('formularioRegistro');

  if (formularioLogin) {
    formularioLogin.addEventListener('submit', (evento) => {
      evento.preventDefault();
      evento.stopPropagation();

      if (!formularioLogin.checkValidity()) {
        formularioLogin.classList.add('was-validated');
        evento.preventDefault();
        evento.stopPropagation();
      } else {
        formularioLogin.classList.add('was-validated');
      }
    });
  }

  if (formularioRegistro) {
    const clave = document.getElementById('registroClave');
    const confirmar = document.getElementById('registroConfirmar');

    function validarCoincidencia() {
      if (clave.value !== confirmar.value) {
        confirmar.setCustomValidity('no-coincide');
      } else {
        confirmar.setCustomValidity('');
      }
    }
    clave.addEventListener('input', validarCoincidencia);
    confirmar.addEventListener('input', validarCoincidencia);

    formularioRegistro.addEventListener('submit', (evento) => {
      evento.preventDefault();
      evento.stopPropagation();

      validarCoincidencia();

      if (!formularioRegistro.checkValidity()) {
        formularioRegistro.classList.add('was-validated');
        return;
      }

      // Formulario válido: ahora SÍ se envía a Flask (POST /signup)
      formularioRegistro.submit();
    });
  }
}

/* ---------- 9. Búsqueda de las tarjetas del catálogo ---------- */
function inicializarBusquedaCatalogo() {
  const formulario = document.getElementById('buscador-nav');
  const campo = document.getElementById('buscar-nav');
  const tarjetas = Array.from(document.querySelectorAll('.tarjeta-producto'));
  const mensaje = document.getElementById('mensaje-busqueda');
  if (!formulario || !campo || !tarjetas.length) return;

  function filtrarTarjetas(evento) {
    if (evento) evento.preventDefault();
    const termino = campo.value.trim().toLocaleLowerCase('es-MX');
    let visibles = 0;

    tarjetas.forEach((tarjeta) => {
      const coincide = tarjeta.textContent.toLocaleLowerCase('es-MX').includes(termino);
      tarjeta.classList.toggle('d-none', !coincide);
      if (coincide) visibles += 1;
    });

    if (mensaje) mensaje.hidden = !termino || visibles > 0;
  }

  campo.addEventListener('input', filtrarTarjetas);
  formulario.addEventListener('submit', filtrarTarjetas);
}
