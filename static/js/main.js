import * as THREE from 'https://cdn.skypack.dev/three@0.136.0';

/**
 * Professional 3D Portfolio Scene
 */

const canvas = document.querySelector('#three-canvas');
const scene = new THREE.Scene();

// Camera setup
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

// Renderer setup
const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    alpha: true,
    antialias: true
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

// Lights
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0x00f2fe, 2);
pointLight.position.set(2, 3, 4);
scene.add(pointLight);

// Central Geometric Object (The "Core")
const geometry = new THREE.TorusKnotGeometry(1.5, 0.4, 128, 16);
const material = new THREE.MeshStandardMaterial({
    color: 0x4facfe,
    wireframe: true,
    transparent: true,
    opacity: 0.3,
});
const torusKnot = new THREE.Mesh(geometry, material);
scene.add(torusKnot);

// Particle Nebula
const particlesGeometry = new THREE.BufferGeometry();
const count = 5000;
const positions = new Float32Array(count * 3);
const colors = new Float32Array(count * 3);

for (let i = 0; i < count * 3; i++) {
    positions[i] = (Math.random() - 0.5) * 15;
    colors[i] = Math.random();
}

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

const particlesMaterial = new THREE.PointsMaterial({
    size: 0.012,
    sizeAttenuation: true,
    transparent: true,
    alphaTest: 0.001,
    blending: THREE.AdditiveBlending,
    vertexColors: true
});

const particles = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particles);

// Mouse Interaction
let mouseX = 0;
let mouseY = 0;

document.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX / window.innerWidth) - 0.5;
    mouseY = (event.clientY / window.innerHeight) - 0.5;
});

// Animation Loop
const clock = new THREE.Clock();

const animate = () => {
    const elapsedTime = clock.getElapsedTime();

    // Rotate Torus Knot
    torusKnot.rotation.y = elapsedTime * 0.2;
    torusKnot.rotation.z = elapsedTime * 0.1;

    // Smooth interaction with mouse
    const targetX = mouseX * 2;
    const targetY = -mouseY * 2;

    torusKnot.position.x += (targetX - torusKnot.position.x) * 0.05;
    torusKnot.position.y += (targetY - torusKnot.position.y) * 0.05;

    // Nebula rotation
    particles.rotation.y = elapsedTime * 0.05;
    particles.rotation.x = elapsedTime * 0.02;

    // Render
    renderer.render(scene, camera);
    window.requestAnimationFrame(animate);
};

// Resize Handler
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
});

animate();
