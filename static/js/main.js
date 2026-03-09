/**
 * Professional Night Sky Starfield Background
 */

const canvas = document.getElementById('stars-canvas');
const ctx = canvas.getContext('2d');

let width, height;
let stars = [];
const STAR_COUNT = window.innerWidth < 768 ? 100 : 250;

function init() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    stars = [];

    for (let i = 0; i < STAR_COUNT; i++) {
        stars.push({
            x: Math.random() * width,
            y: Math.random() * height,
            size: Math.random() * 2 + 0.5,
            opacity: Math.random(),
            twinkleSpeed: Math.random() * 0.02 + 0.005,
            parallax: Math.random() * 0.5 + 0.1
        });
    }
}

// Shooting Star setup
let shootingStars = [];

function createShootingStar() {
    shootingStars.push({
        x: Math.random() * width,
        y: Math.random() * (height / 2),
        length: Math.random() * 80 + 20,
        speed: Math.random() * 10 + 5,
        opacity: 1
    });
}

function draw() {
    ctx.clearRect(0, 0, width, height);
    const scrollY = window.scrollY;

    // Draw static stars
    stars.forEach(star => {
        const yOffset = (scrollY * star.parallax) % height;
        let starY = (star.y - yOffset);
        if (starY < 0) starY += height;

        star.opacity += star.twinkleSpeed;
        if (star.opacity > 1 || star.opacity < 0.2) {
            star.twinkleSpeed = -star.twinkleSpeed;
        }

        ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`;
        ctx.beginPath();
        ctx.arc(star.x, starY, star.size, 0, Math.PI * 2);
        ctx.fill();
    });

    // Draw shooting stars
    shootingStars.forEach((ss, index) => {
        ctx.strokeStyle = `rgba(255, 255, 255, ${ss.opacity})`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(ss.x, ss.y);
        ctx.lineTo(ss.x + ss.length, ss.y + ss.length);
        ctx.stroke();

        ss.x += ss.speed;
        ss.y += ss.speed;
        ss.opacity -= 0.02;

        if (ss.opacity <= 0) {
            shootingStars.splice(index, 1);
        }
    });

    if (Math.random() < 0.015) createShootingStar(); // 1.5% chance per frame

    requestAnimationFrame(draw);
}

window.addEventListener('resize', init);
window.addEventListener('load', () => {
    init();
    draw();
});