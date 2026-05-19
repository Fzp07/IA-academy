document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (el) {
        return new bootstrap.Tooltip(el);
    });

    // ============================================
    // PARTÍCULAS DE INTELIGENCIA ARTIFICIAL
    // ============================================

    function createAIParticles() {
        var container = document.createElement('div');
        container.className = 'ai-particle-container';
        document.body.appendChild(container);

        var colors = ['#6C3CE1', '#00D4FF', '#00FF88', '#8B5CF6'];
        var count = 30;

        for (var i = 0; i < count; i++) {
            var particle = document.createElement('div');
            particle.className = 'ai-particle';
            var size = Math.random() * 4 + 2;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.background = colors[Math.floor(Math.random() * colors.length)];
            particle.style.boxShadow = '0 0 ' + (size * 3) + 'px ' + particle.style.background;
            particle.style.setProperty('--duration', (Math.random() * 10 + 6) + 's');
            particle.style.setProperty('--delay', (Math.random() * 10) + 's');
            container.appendChild(particle);
        }
    }

    // ============================================
    // DATA RAIN (efecto de lluvia de datos)
    // ============================================

    function createDataRain() {
        var container = document.createElement('div');
        container.className = 'ai-data-rain';
        document.body.appendChild(container);

        var chars = '0110100100101001101001001010010110100101101001';
        for (var i = 0; i < 20; i++) {
            var span = document.createElement('span');
            span.textContent = chars[Math.floor(Math.random() * chars.length)];
            span.style.left = Math.random() * 100 + '%';
            span.style.fontSize = (Math.random() * 8 + 8) + 'px';
            span.style.opacity = Math.random() * 0.3 + 0.05;
            span.style.setProperty('--duration', (Math.random() * 8 + 4) + 's');
            span.style.setProperty('--delay', (Math.random() * 10) + 's');
            container.appendChild(span);
        }
    }

    // ============================================
    // INICIAR EFECTOS
    // ============================================

    createAIParticles();
    createDataRain();
});
