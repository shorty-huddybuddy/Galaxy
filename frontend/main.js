/**
 * Hand Gesture Controlled Solar System - Main JavaScript
 * Uses Three.js for 3D rendering and Socket.IO for real-time gesture data
 */

// Global variables
let scene, camera, renderer, controls;
let solarSystem;
let gestureData = { zoom: 50, rotate_x: 0, rotate_y: 0 };
// Tuning constants
const MODEL_INITIAL_SCALE = 6.0; // Increase to make the model appear larger initially
const INITIAL_ZOOM = 85; // 0-100; higher = closer camera

let targetZoom = INITIAL_ZOOM;
let targetRotation = { x: 0, y: 0 };
let socket;

// Smoothing parameters
const LERP_FACTOR = 0.1; // Smoothing factor (0-1, lower = smoother)

/**
 * Initialize Three.js scene
 */
function initThreeJS() {
    const container = document.getElementById('canvas-container');
    
    // Create scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);
    
    // Create camera
    camera = new THREE.PerspectiveCamera(
        75, // Field of view
        window.innerWidth / window.innerHeight, // Aspect ratio
        0.1, // Near clipping plane
        1000 // Far clipping plane
    );
    camera.position.set(0, 5, 10);
    
    // Create renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);
    
    // Add orbit controls (will be overridden by gestures)
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.enableZoom = true;
    controls.enablePan = false;
    
    // Add lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 3, 5);
    scene.add(directionalLight);
    
    const pointLight = new THREE.PointLight(0xffffff, 1, 100);
    pointLight.position.set(0, 0, 0);
    scene.add(pointLight);
    
    // Handle window resize
    window.addEventListener('resize', onWindowResize, false);
}

/**
 * Load 3D solar system model
 */
function loadSolarSystem() {
    const loader = new THREE.GLTFLoader();
    console.log('Attempting to load HORNET.glb...');
    loader.load(
        '/solar_system.glb',
        function (gltf) {
            // Model loaded successfully
            console.log('Model loaded successfully!');
            solarSystem = gltf.scene;
            solarSystem.scale.set(MODEL_INITIAL_SCALE, MODEL_INITIAL_SCALE, MODEL_INITIAL_SCALE);
            scene.add(solarSystem);
            const box = new THREE.Box3().setFromObject(solarSystem);
            const center = box.getCenter(new THREE.Vector3());
            solarSystem.position.sub(center);
            hideLoading();
        },
        function (xhr) {
            console.log((xhr.loaded / xhr.total * 100) + '% loaded');
        },
        function (error) {
            // Error loading model - show minimal fallback (sun + stars)
            console.warn('Could not load HORNET.glb, showing minimal fallback');
            console.error('Error:', error);
            createMinimalProceduralSolarSystem();
            hideLoading();
        }
    );
}

// Minimal fallback if .glb fails: Sun + stars only
function createMinimalProceduralSolarSystem() {
    solarSystem = new THREE.Group();
    const sunGeometry = new THREE.SphereGeometry(1, 32, 32);
    const sunMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00, emissive: 0xffff00, emissiveIntensity: 0.5 });
    const sun = new THREE.Mesh(sunGeometry, sunMaterial);
    solarSystem.add(sun);
    const starsGeometry = new THREE.BufferGeometry();
    const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.1, transparent: true });
    const starsVertices = [];
    for (let i = 0; i < 500; i++) {
        const x = (Math.random() - 0.5) * 100;
        const y = (Math.random() - 0.5) * 100;
        const z = (Math.random() - 0.5) * 100;
        starsVertices.push(x, y, z);
    }
    starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
    const stars = new THREE.Points(starsGeometry, starsMaterial);
    scene.add(stars);
    solarSystem.scale.set(MODEL_INITIAL_SCALE, MODEL_INITIAL_SCALE, MODEL_INITIAL_SCALE);
    scene.add(solarSystem);
}

/**
 * Hide loading screen
 */
function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = 'none';
    }
}

/**
 * Initialize Socket.IO connection
 */
function initSocketIO() {
    console.log('Initializing Socket.IO connection to http://localhost:5000');
    socket = io('http://localhost:5000', {
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionAttempts: 5
    });
    
    socket.on('connect', function() {
        console.log('✅ Connected to gesture server - Socket ID:', socket.id);
        updateConnectionStatus(true);
    });
    
    socket.on('disconnect', function() {
        console.log('❌ Disconnected from gesture server');
        updateConnectionStatus(false);
    });
    
    socket.on('connect_error', function(error) {
        console.error('Connection Error:', error);
        updateConnectionStatus(false);
    });
    
    socket.on('gesture_update', function(data) {
        // Receive gesture data from Python backend
        console.log('Received gesture data:', data);
        gestureData = data;
        updateUI(data);
        
        // Set target values for smooth interpolation
        targetZoom = data.zoom;
        targetRotation.x = data.rotate_x;
        targetRotation.y = data.rotate_y;
    });
}

/**
 * Update connection status in UI
 */
function updateConnectionStatus(connected) {
    const statusElement = document.getElementById('connection-status');
    const textElement = document.getElementById('connection-text');
    
    if (connected) {
        statusElement.classList.remove('disconnected');
        statusElement.classList.add('connected');
        textElement.textContent = 'Connected';
    } else {
        statusElement.classList.remove('connected');
        statusElement.classList.add('disconnected');
        textElement.textContent = 'Disconnected';
    }
}

/**
 * Update UI with gesture data
 */
function updateUI(data) {
    document.getElementById('zoom-value').textContent = data.zoom.toFixed(1);
    document.getElementById('zoom-bar').style.width = data.zoom + '%';
    document.getElementById('rotate-x-value').textContent = data.rotate_x.toFixed(1) + '°';
    document.getElementById('rotate-y-value').textContent = data.rotate_y.toFixed(1) + '°';
}

/**
 * Apply gesture data to camera with smooth interpolation
 */
function applyGestureToCamera() {
    if (!solarSystem) return;
    
    // Smooth zoom interpolation
    const currentDistance = camera.position.length();
    const targetDistance = THREE.MathUtils.lerp(5, 30, 1 - (targetZoom / 100));
    const newDistance = THREE.MathUtils.lerp(currentDistance, targetDistance, LERP_FACTOR);
    
    // Update camera position (zoom)
    const direction = camera.position.clone().normalize();
    camera.position.copy(direction.multiplyScalar(newDistance));
    
    // Smooth rotation interpolation
    const currentRotationY = solarSystem.rotation.y;
    const currentRotationX = solarSystem.rotation.x;
    
    const newRotationY = THREE.MathUtils.lerp(
        currentRotationY, 
        targetRotation.y * Math.PI / 180, 
        LERP_FACTOR
    );
    const newRotationX = THREE.MathUtils.lerp(
        currentRotationX, 
        targetRotation.x * Math.PI / 180, 
        LERP_FACTOR
    );
    
    solarSystem.rotation.y = newRotationY;
    solarSystem.rotation.x = newRotationX;
}

// ...existing code...

/**
 * Handle window resize
 */
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

/**
 * Animation loop
 */
function animate() {
    requestAnimationFrame(animate);
    // Apply gesture controls with smooth interpolation
    applyGestureToCamera();
    // Update controls
    controls.update();
    // Render scene
    renderer.render(scene, camera);
}

/**
 * Initialize everything when page loads
 */
window.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing Hand Gesture Controlled Solar System...');
    
    // Initialize Three.js
    initThreeJS();
    
    // Load solar system model
    loadSolarSystem();
    
    // Initialize Socket.IO
    initSocketIO();
    
    // Start animation loop
    animate();
    
    console.log('Initialization complete!');
});
