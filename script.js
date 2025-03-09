// ✅ Theme Toggling
document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.querySelector('.theme-toggle');
    const moonIcon = document.querySelector('.moon-icon');
    const sunIcon = document.querySelector('.sun-icon');
    const savedTheme = localStorage.getItem('theme') || 'light';

    function setTheme(isDark) {
        document.documentElement.classList.toggle('dark', isDark);
        moonIcon.classList.toggle('hidden', isDark);
        sunIcon.classList.toggle('hidden', !isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

    setTheme(savedTheme === 'dark');

    themeToggle.addEventListener('click', () => {
        setTheme(!document.documentElement.classList.contains('dark'));
    });
});



// ✅ Handle window resizing
function onWindowResize() {
    const container = document.querySelector('.brain-container');
    if (!renderer || !container) return;

    camera.aspect = container.offsetWidth / container.offsetHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.offsetWidth, container.offsetHeight);
}
window.addEventListener('resize', onWindowResize);

// ✅ Smooth Scroll for Navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({ behavior: 'smooth' });
    });
});

// ✅ Initialize Three.js when DOM is ready
document.addEventListener("DOMContentLoaded", initBrain);
