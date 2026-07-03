const express = require("express");
const os = require("os");

const app = express();

app.get("/", (req, res) => {
    res.json({
        application: "app2-localhost",
        hostname: os.hostname(),
        time: new Date().toISOString()
    });
});

app.listen(3000, () => {
    console.log("Running on port 3000");
});