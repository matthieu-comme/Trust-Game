require("dotenv").config();
const express = require("express");
const cors = require("cors");
const { OpenAI } = require("openai");

const app = express();
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

app.use(cors());
app.use(express.json());
app.use(express.static("public")); // ← pour servir index.html

app.post("/chat", async (req, res) => {
    const { message } = req.body;

    try {
        const completion = await openai.chat.completions.create({
            model: "gpt-4",
            messages: [{ role: "user", content: message }],
        });

        res.json({ reply: completion.choices[0].message.content });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "Erreur OpenAI" });
    }
});

app.listen(3000, () => console.log("Serveur en écoute sur http://localhost:3000"));
