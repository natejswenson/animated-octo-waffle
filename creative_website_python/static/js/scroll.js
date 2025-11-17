/**
 * Minimal JavaScript - Only essential browser interactions
 * All configuration and rendering done in Python
 */

(function() {
    'use strict';

    // State
    let isScrolling = false;
    let ticking = false;
    let rafId = null;
    let currentSectionIndex = 0;

    // Cache DOM elements
    const sections = document.querySelectorAll('.content-section');
    const dots = document.querySelectorAll('.progress-dot');

    // Initialize
    function init() {
        // Ensure page starts at top
        window.scrollTo(0, 0);

        // Set up event listeners
        window.addEventListener('scroll', onScroll, { passive: true });

        // Progress dot click handlers
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => scrollToSection(index));
        });

        // Initial animation calculation
        handleScroll();
    }

    // Scroll event handler with requestAnimationFrame throttling
    function onScroll() {
        if (!ticking) {
            rafId = requestAnimationFrame(() => {
                handleInfiniteScroll();
                handleScroll();
                ticking = false;
            });
            ticking = true;
        }
    }

    // Handle infinite scroll loop
    function handleInfiniteScroll() {
        if (isScrolling) return;

        const scrollHeight = document.documentElement.scrollHeight;
        const clientHeight = document.documentElement.clientHeight;
        const scrollTop = window.scrollY;
        const sectionHeight = (scrollHeight - clientHeight) / (SECTION_COUNT + 2);

        // Loop to top when near bottom
        if (scrollTop + clientHeight >= scrollHeight - SCROLL_CONFIG.THRESHOLD) {
            isScrolling = true;
            window.scrollTo({
                top: sectionHeight,
                behavior: 'instant'
            });
            setTimeout(() => { isScrolling = false; }, SCROLL_CONFIG.TRANSITION_DELAY);
        }

        // Loop to bottom when near top
        if (scrollTop <= SCROLL_CONFIG.THRESHOLD) {
            isScrolling = true;
            window.scrollTo({
                top: scrollHeight - clientHeight - sectionHeight,
                behavior: 'instant'
            });
            setTimeout(() => { isScrolling = false; }, SCROLL_CONFIG.TRANSITION_DELAY);
        }
    }

    // Handle scroll animations (proximity-based scale/opacity)
    function handleScroll() {
        const clientHeight = document.documentElement.clientHeight;
        let closestSection = 0;
        let minDistance = Infinity;

        sections.forEach((section, index) => {
            const rect = section.getBoundingClientRect();

            // Calculate proximity effect
            const sectionCenter = rect.top + rect.height / 2;
            const viewportCenter = clientHeight / 2;
            const distance = Math.abs(sectionCenter - viewportCenter);
            const maxDistance = clientHeight / 2;
            const proximity = Math.max(0, 1 - distance / maxDistance);

            // Calculate scale and opacity
            const scale = ANIMATION.SCALE_MIN + proximity * (ANIMATION.SCALE_MAX - ANIMATION.SCALE_MIN);
            const opacity = ANIMATION.OPACITY_MIN + proximity * (ANIMATION.OPACITY_MAX - ANIMATION.OPACITY_MIN);

            // Apply to section wrapper
            const wrapper = section.querySelector('.section-wrapper');
            if (wrapper) {
                wrapper.style.transform = `scale(${scale}) translateZ(0)`;
                wrapper.style.opacity = opacity;
            }

            // Track closest section
            if (distance < minDistance) {
                minDistance = distance;
                closestSection = index;
            }
        });

        // Update current section (accounting for looped array)
        const actualIndex = closestSection === 0
            ? SECTION_COUNT - 1
            : closestSection === sections.length - 1
            ? 0
            : closestSection - 1;

        currentSectionIndex = actualIndex;
        updateProgressIndicator(actualIndex);
    }

    // Update progress dots
    function updateProgressIndicator(index) {
        dots.forEach((dot, i) => {
            if (i === index) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    // Scroll to specific section
    function scrollToSection(index) {
        const targetSection = sections[index + 1]; // +1 for looped array
        if (targetSection) {
            targetSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
