/*  Lets add a little js */
function scrollToSection(sectionId) {
    const section = document.getElementById('tools');
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

function highlightSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.add('highlight');
        setTimeout(() => {
            section.classList.remove('highlight');
        }, 1500);
    }
}

// Toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

// Show/hide a modal
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Copy text to clipboard
function copyText(elementId) {
    const el = document.getElementById(elementId);
    if (el) {
        const text = el.innerText || el.value;
        navigator.clipboard.writeText(text);
    }
}

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

const text = "Welcome to OG's AI Health Assistant";
let index = 0;


function typeEffect() {
    const target = document.getElementById("typing-text");
    if (target && index < text.length) {
        target.innerHTML += text.charAt(index);
        index++;
        setTimeout(typeEffect, 70);
    } else {
        // Remove the blinking cursor after typing is done
        target.classList.remove("typing");
    }
}

window.onload = function () {
    const target = document.getElementById("typing-text");
    if (target) {
        target.classList.add("typing");
        typeEffect();
    }
};


window.onload = function () {
    typeEffect();
};


// Example usage:
// scrollToSection('tools'); highlightSection('tools');
// toggleDarkMode();
// showModal('myModal'); hideModal('myModal');
// copyText('copyTarget');
// scrollToTop();