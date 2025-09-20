import express from "express";

const app = express();
app.use(express.json());

const PORT = 9001;

// Endpoint 
app.get("/ping", (req, res) => {
  res.json({ ok: true, service: "service-a (Node)" });
});

// Endpoint principal
app.post("/stepA", (req, res) => {
  try {
    let { message, trace } = req.body;
    if (!message) {
      return res.status(400).json({ error: "campo 'message' é obrigatório" });
    }

    // Transformar em maiúsculas
    const upperMessage = message.toUpperCase();

    // Criar registro no trace
    const entry = {
      service: "service-a",
      language: "JavaScript",
      info: { uppercased: true },
      timestamp: new Date().toISOString()
    };

    const newTrace = Array.isArray(trace) ? [...trace, entry] : [entry];

    res.json({
      message: upperMessage,
      trace: newTrace
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Service A rodando em http://127.0.0.1:${PORT}`);
});
