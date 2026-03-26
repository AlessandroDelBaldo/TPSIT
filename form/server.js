const express = require('express');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const DATA_FILE = path.join(__dirname, 'library.json');

app.use(express.json());
app.use(express.static(__dirname));

async function readData() {
  try {
    const txt = await fs.readFile(DATA_FILE, 'utf8');
    return JSON.parse(txt || '{"books":[]}');
  } catch (e) {
    return { books: [] };
  }
}

app.get('/books', async (req, res) => {
  const json = await readData();
  res.json(json);
});

app.post('/books', async (req, res) => {
  const newBook = req.body || {};
  const json = await readData();
  json.books.push(newBook);
  try {
    await fs.writeFile(DATA_FILE, JSON.stringify(json, null, 2), 'utf8');
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ error: 'write_failed' });
  }
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Server avviato su http://localhost:${PORT}`));