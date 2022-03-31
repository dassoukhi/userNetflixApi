const express = require('express')
const morgan = require('morgan')

const db = require('./db')

const PORT = process.env.PORT || 5000
const app = express()


app.use(morgan('dev'))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

app.get('/', (req, res) => res.send('Hello World!'))

app.get('/users', async (req, res) => {
  const users = await db.select().from('users')
  res.json(users)
})
app.get('/users/:id', async (req, res) => {
  const id = req.params.id
  const user = await db.select().from('users').where('id', id).first()
  res.json(user)
})

app.put('/users/edit/:id', async (req, res) => {
  const id = req.params.id
  const body = { nom: req.body.nom, adresse: req.body.adresse, email: req.body.email, pays: req.body.pays, status: req.body.status, role: req.body.role }
  const user = await db.select().from('users').where('id', req.body.id).update(body).returning(['id','nom', 'adresse','email', 'pays', 'status', 'role'])
  res.json(user)
})

app.delete('/users/delete', async (req, res) => {
  const id = req.body.id
  const user = await db.select().from('users').del()
  .where('id', id)
  .then((result) => {
    console.log(result);
   res.status(200).send({ 'status': 'ok' });
  })
   .catch((err) => {
    res.status(500).send(err);
   })
  res.json(user)
})

app.post('/users/add', async (req, res) => {
  const user = await db('users').insert({ nom: req.body.nom, adresse: req.body.adresse, email: req.body.email, pays: req.body.pays, status: req.body.status, role: req.body.role }).returning('*')
  res.json(user)
})

app.listen(PORT, () => console.log(`Server up at http://localhost:${PORT}`))
