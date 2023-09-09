export function getFile(link, file_name) {
	const data = getCargoData();
	fetch(link, {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(data)
	})
		.then(response => response.blob())
		.then(blob => {
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = file_name;
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
			URL.revokeObjectURL(url);
		})
		.catch(error => {
			// Handle error
			console.error(error);
		});
}

export function getCargoData() {
	const table = document.querySelector("#cargo_table");
	const rows = table.rows;
	const data = [];

	for (let i = 0; i < rows.length; i++) {
		const row = rows[i];
		const cells = row.cells;
		const rowData = [];
		let offset = 0;
		if (i > 0) {
			offset = 1;
		}

		for (let j = 0; j < cells.length - offset; j++) {
			const cell = cells[j];
			let value = "";
			if (cell.querySelector("input")) {
				value = cell.querySelector("input").value;
			}
			else if (cell.querySelector("select")) {
				value = cell.querySelector("select").value;
			}
			else {
				value = cell.innerHTML;
			}
			rowData.push(value);
		}

		data.push(rowData);
	}
	return data;
}

document.getElementById("download_scheme_btn").onclick = function () {
	getFile('/download/download_scheme', 'Схема.pdf');
};

document.getElementById("download_RPZ_btn").onclick = function () {
	getFile('/download/download_RPZ', 'РПЗ-вагонов.zip');
};

document.getElementById("download_stl_btn").onclick = function () {
	getFile('/get_stl', '3D модель.stl');
};