const db = require('../db')

;(async () => {
  try {
    await db.schema.dropTableIfExists('users')
    await db.schema.withSchema('public').createTable('users', (table) => {
      table.increments()
      table.string('nom')
      table.string('adresse')
      table.string('email')
      table.string('pays')
      table.string('status')
      table.string('role')
    })
    console.log('Created users table!')
    process.exit(0)
  } catch (err) {
    console.log(err)
    process.exit(1)
  }
})()
