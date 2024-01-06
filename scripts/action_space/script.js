function addPoint(event) {
    // Get the bounding rectangle of the coordinate system
    const rect = document.getElementById('coordinateSystem').getBoundingClientRect();

    // Calculate the x and y position relative to the coordinate system
    const x = event.clientX - rect.left - rect.width / 2;
    const y = -(event.clientY - rect.top - rect.height / 2);

    // Calculate the radius and angle
    const r = Math.sqrt(x * x + y * y);
    const theta = Math.atan2(y, x) * (180 / Math.PI);

    // Adding a visual point
    const point = document.createElement("div");
    point.classList.add("point");
    point.style.left = `${x + rect.width / 2 - 2.5}px`;
    point.style.top = `${-y + rect.height / 2 - 2.5}px`;
    document.getElementById("coordinateSystem").appendChild(point);

    // Adding to list
    const listItem = document.createElement("li");
    listItem.textContent = `Radius: ${Math.round(r.toFixed(2))}, Angle: ${Math.round(theta.toFixed(2) - 90)}`;
    document.getElementById("list").appendChild(listItem);
}
