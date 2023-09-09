import { getCargoData } from "./script.js";
import * as THREE from "three";

function create3DModel() {
	// Создаем сцену
	var scene = new THREE.Scene();

	// Создаем камеру
	var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
	camera.position.z = 5;

	// Создаем рендерер
	var renderer = new THREE.WebGLRenderer();
	renderer.setSize(window.innerWidth, window.innerHeight);
	document.getElementById("scene-container").appendChild(renderer.domElement);

	// Загружаем STL модель
	var loader = new THREE.STLLoader();

	let data = getCargoData();
	fetch("/get_stl", {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(data)
	})
		.then(response => response.blob())
		.then(blob => {
			const url = URL.createObjectURL(blob);
			loader.load(url, function (geometry) {
				var material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
				var mesh = new THREE.Mesh(geometry, material);
				scene.add(mesh);
				renderer.render(scene, camera);
			});

			function animate() {
				requestAnimationFrame(animate);
				mesh.rotation.x += 0.01;
				mesh.rotation.y += 0.01;
				renderer.render(scene, camera);
			}
			animate();

		})
		.catch(error => {
			// Handle error
			console.error(error);
		});
}

create3DModel();