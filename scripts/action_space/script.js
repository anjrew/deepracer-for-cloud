function addPoint(event) {
    // Get the bounding rectangle of the coordinate system
    const rect = document.getElementById('coordinateSystem').getBoundingClientRect();

    // Calculate the x and y position relative to the coordinate system
    const x = event.clientX - rect.left - rect.width / 2;
    const y = -(event.clientY - rect.top - rect.height / 2);

    console.log("x:", x, "y:", y); // Debugging

    // Fetch rounding factors
    const speedRoundingFactor = parseFloat(document.getElementById('speedPrecision').value, 10);
    const steeringRoundingFactor = parseFloat(document.getElementById('steeringPrecision').value, 10);

    console.log("Speed Rounding Factor:", speedRoundingFactor, "Steering Rounding Factor:", steeringRoundingFactor); // Debugging

    // Calculate the speed and steering angle
    let rawSpeed = Math.sqrt(x * x + y * y); // Assuming speed is the radius
    console.log("Raw Speed:", rawSpeed); // Debugging

    let speed = scaleSpeedValue(rawSpeed, [0, 150], [0, 4]);
    console.log("Scaled Speed:", speed); // Debugging

    speed = roundToNearest(speed, speedRoundingFactor); // Round to nearest factor
    console.log("Rounded Speed:", speed); // Debugging

    let rawSteeringAngle = Math.atan2(y, x) * (180 / Math.PI) - 90; // Adjusting the angle
    console.log("Raw Steering Angle:", rawSteeringAngle); // Debugging

    let steering_angle = roundToNearest(rawSteeringAngle, steeringRoundingFactor); // Round to nearest factor
    console.log("Rounded Steering Angle:", steering_angle); // Debugging

    // Create a JSON object
    const data = {
        "steering_angle": steering_angle,
        "speed": speed
    };
    
    // Adding a visual point
    const point = document.createElement("div");
    point.classList.add("point");
    point.style.left = `${x + rect.width / 2 - 2.5}px`;
    point.style.top = `${-y + rect.height / 2 - 2.5}px`;
    document.getElementById("coordinateSystem").appendChild(point);

    // Adding to list as JSON string
    const listItem = document.createElement("li");
    listItem.textContent = JSON.stringify(data, null, 2);
    document.getElementById("list").appendChild(listItem);
}


function scaleSpeedValue(value, fromRange, toRange) {
    const scale = (toRange[1] - toRange[0]) / (fromRange[1] - fromRange[0]);
    return toRange[0] + scale * (value - fromRange[0]);
}


function roundToNearest(value, nearest) {
    if (nearest === 0) {
        return value; // Return value as is if nearest is 0
    }

    // Use the countDecimals function to determine the number of decimal places in the rounding factor
    console.log("nearest:", nearest); // Debugging

    const factorDecimalPlaces = countDecimals(nearest);
    console.log("Factor Decimal Places:", factorDecimalPlaces); // Debugging

    // Scale up both value and nearest to avoid floating point issues
    const scaledUpNearest = nearest * Math.pow(10, factorDecimalPlaces);
    const scaledUpValue = value * Math.pow(10, factorDecimalPlaces);

    // Perform rounding on scaled values and scale down
    const roundedValue = Math.round(scaledUpValue / scaledUpNearest) * scaledUpNearest;
    return roundedValue / Math.pow(10, factorDecimalPlaces);
}


function countDecimals(value) {
    if (Math.floor(value) === value) return 0;
    return value.toString().split(".")[1].length || 0;
}